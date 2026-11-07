"""OpenDART acquisition with explicit accounting context and provenance.

No LLM selects accounts or calculates amounts here.  Ambiguous accounts remain
available in ``raw_accounts`` and are deliberately not promoted to facts.
"""

from __future__ import annotations

from calendar import monthrange
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation, localcontext
from io import BytesIO
import json
from pathlib import PurePosixPath
import re
import stat
from zipfile import BadZipFile, ZipFile

from defusedxml import ElementTree
from defusedxml.common import DefusedXmlException
import httpx

from .dart_notes import parse_note_topics
from .models import Dataset, Fact, Period
from .xbrl import DART_IDENTIFIER_SCHEME, XbrlError, XbrlFact, read_xbrl_archive


BASE_URL = "https://opendart.fss.or.kr/api/"
_MAX_RESPONSE = 32 * 1024 * 1024
_MAX_INDEX_XML = 96 * 1024 * 1024
_REPORT_CODES = {3: "11013", 6: "11012", 9: "11014", 12: "11011"}
_REPORT_PATTERN = re.compile(r"(사업|반기|분기)보고서\s*\((\d{4})\.(\d{2})\)")
_XBRL_ENDPOINT = "fnlttXbrl.xml"
INTERIM_CF_HOLD = "재무 API 응답에 현금흐름표의 시작·종료일이 없어 중간보고서 누적 기간을 검증할 수 없으므로 보류했습니다."


class DartError(RuntimeError):
    """A sanitized error: request URLs and authentication keys are never echoed."""

    def __init__(self, message: str, code: str = "") -> None:
        super().__init__(message)
        self.code = code


_ERRORS = {
    "010": "등록되지 않은 OpenDART 인증키입니다.",
    "011": "현재 사용할 수 없는 OpenDART 인증키입니다.",
    "012": "OpenDART에서 요청 IP의 접근을 허용하지 않았습니다.",
    "013": "요청한 공시 데이터가 없습니다.",
    "014": "요청한 공시 원본 파일이 없습니다.",
    "020": "OpenDART 요청 한도를 초과했습니다. 잠시 후 다시 시도하세요.",
    "021": "OpenDART 조회 회사 수 한도를 초과했습니다.",
    "100": "OpenDART 요청 인자가 유효하지 않습니다.",
    "101": "OpenDART에서 요청을 허용하지 않았습니다.",
    "800": "OpenDART 시스템 점검 중입니다.",
    "901": "OpenDART 인증키의 개인정보 보유기간이 만료되었습니다.",
}


def parse_amount(value: object) -> Decimal | None:
    """Read financial amount strings without binary floating point or guessing."""
    if value is None:
        return None
    if isinstance(value, bool) or isinstance(value, float):
        raise ValueError("금액은 원본 숫자 문자열 또는 정수여야 합니다.")
    text = str(value).strip().replace("\u2212", "-")
    if text in ("", "-", "—", "–"):
        return None
    if text.startswith("(") and text.endswith(")"):
        text = "-" + text[1:-1].strip()
    if not re.fullmatch(r"[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?", text):
        raise ValueError("금액 형식을 해석하지 못했습니다.")
    try:
        amount = Decimal(text.replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError("금액 형식을 해석하지 못했습니다.") from exc
    if not amount.is_finite():
        raise ValueError("금액은 유한한 숫자여야 합니다.")
    return amount


@dataclass(frozen=True)
class _Spec:
    statements: tuple[str, ...]
    ids: tuple[str, ...]
    aliases: tuple[str, ...]
    attribution: str = "total"
    cash_outflow: bool = False


def _ifrs(*names: str) -> tuple[str, ...]:
    return tuple(prefix + name for name in names for prefix in ("ifrs-full_", "ifrs_"))


# Aliases are reviewed exact names, not substring or fuzzy matches.  Broad
# categories such as '매출채권및기타채권' are not relabelled as trade receivables.
_SPECS: dict[str, _Spec] = {
    "revenue": _Spec(("IS", "CIS"), _ifrs("Revenue", "RevenueFromContractsWithCustomers"), ("매출액", "수익(매출액)", "매출")),
    "cost_of_sales": _Spec(("IS", "CIS"), _ifrs("CostOfSales"), ("매출원가",)),
    "gross_profit": _Spec(("IS", "CIS"), _ifrs("GrossProfit"), ("매출총이익", "매출총이익(손실)")),
    "operating_profit": _Spec(("IS", "CIS"), ("dart_OperatingIncomeLoss",) + _ifrs("ProfitLossFromOperatingActivities"), ("영업이익", "영업이익(손실)", "영업손익")),
    "net_income": _Spec(("IS", "CIS"), _ifrs("ProfitLoss"), ("당기순이익", "당기순이익(손실)", "당기순손익", "분기순이익", "분기순이익(손실)", "반기순이익", "반기순이익(손실)")),
    "comprehensive_income": _Spec(("CIS",), _ifrs("ComprehensiveIncome"), ("총포괄손익",)),
    "parent_net_income": _Spec(("IS", "CIS"), _ifrs("ProfitLossAttributableToOwnersOfParent"), ("지배기업의 소유주에게 귀속되는 당기순이익(손실)", "지배기업소유주지분순이익", "지배기업 소유주지분 순이익", "지배기업 소유주 귀속 당기순이익"), "parent"),
    "assets": _Spec(("BS",), _ifrs("Assets"), ("자산총계", "자산 총계")),
    "liabilities": _Spec(("BS",), _ifrs("Liabilities"), ("부채총계", "부채 총계")),
    "equity": _Spec(("BS",), _ifrs("Equity"), ("자본총계", "자본 총계")),
    "parent_equity": _Spec(("BS",), _ifrs("EquityAttributableToOwnersOfParent"), ("지배기업의 소유주에게 귀속되는 자본", "지배기업 소유주지분", "지배기업의 소유지분"), "parent"),
    "current_assets": _Spec(("BS",), _ifrs("CurrentAssets"), ("유동자산",)),
    "current_liabilities": _Spec(("BS",), _ifrs("CurrentLiabilities"), ("유동부채",)),
    "cash": _Spec(("BS",), _ifrs("CashAndCashEquivalents"), ("현금및현금성자산", "현금 및 현금성자산")),
    "receivables": _Spec(("BS",), _ifrs("TradeReceivables", "CurrentTradeReceivables") + ("dart_ShortTermTradeReceivable", "dart_TradeReceivables"), ("매출채권", "유동매출채권")),
    "inventory": _Spec(("BS",), _ifrs("Inventories"), ("재고자산",)),
    "cfo": _Spec(("CF",), _ifrs("CashFlowsFromUsedInOperatingActivities"), ("영업활동현금흐름", "영업활동으로 인한 현금흐름", "영업활동으로부터의 현금흐름", "영업활동으로 인한 순현금흐름")),
    "cash_change": _Spec(("CF",), _ifrs("IncreaseDecreaseInCashAndCashEquivalents"), ("현금및현금성자산의 순증감",)),
    "cash_change_before_fx": _Spec(("CF",), _ifrs("IncreaseDecreaseInCashAndCashEquivalentsBeforeEffectOfExchangeRateChanges"), ("환율효과 전 현금 순증감",)),
    "cfi": _Spec(("CF",), _ifrs("CashFlowsFromUsedInInvestingActivities"), ("투자활동현금흐름", "투자활동으로 인한 현금흐름", "투자활동으로부터의 현금흐름", "투자활동으로 인한 순현금흐름")),
    "cff": _Spec(("CF",), _ifrs("CashFlowsFromUsedInFinancingActivities"), ("재무활동현금흐름", "재무활동으로 인한 현금흐름", "재무활동으로부터의 현금흐름", "재무활동으로 인한 순현금흐름")),
    "fx_effect": _Spec(("CF",), _ifrs("EffectOfExchangeRateChangesOnCashAndCashEquivalents"), ("현금및현금성자산에 대한 환율변동효과", "환율변동효과", "환율변동으로 인한 현금및현금성자산의 변동")),
    "other_cash_effects": _Spec(("CF",), ("dart_OtherChangesInCashAndCashEquivalents",), ("현금및현금성자산의 기타변동", "현금및현금성자산의 기타 증감")),
    "cash_disposal_transfer": _Spec(("CF",), (), (
        "처분집단으로 분류된 현금및현금성자산", "매각예정자산 분류 현금및현금성자산",
        "매각예정의 일부로 분류된 현금및현금성자산", "매각예정자산으로의 대체", "매각예정자산으로부터의 대체")),
    "cash_disposal_change": _Spec(("CF",), (), ("처분집단으로 분류된 현금및현금성자산의 순증감",)),
    "cash_beginning": _Spec(("CF",), ("dart_CashAndCashEquivalentsAtBeginningOfPeriodCf",), ("기초현금및현금성자산", "기초의 현금및현금성자산", "기초의현금및현금성자산", "기초 현금및현금성자산")),
    "cash_end": _Spec(("CF",), ("dart_CashAndCashEquivalentsAtEndOfPeriodCf",), ("현금흐름표 기말 현금",)),
    "capex_ppe": _Spec(("CF",), _ifrs("PurchaseOfPropertyPlantAndEquipment", "PaymentsToAcquirePropertyPlantAndEquipment", "PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities") + ("dart_PurchaseOfPropertyPlantAndEquipment",), ("유형자산의 취득", "유형자산 취득", "유형자산의취득"), cash_outflow=True),
    "capex_intangible": _Spec(("CF",), _ifrs("PurchaseOfIntangibleAssets", "PaymentsToAcquireIntangibleAssets", "PurchaseOfIntangibleAssetsClassifiedAsInvestingActivities") + ("dart_PurchaseOfIntangibleAssets",), ("무형자산의 취득", "무형자산 취득", "무형자산의취득"), cash_outflow=True),
    "borrowings": _Spec(("BS",), _ifrs("Borrowings") + ("dart_Borrowings",), ("차입금", "총차입금")),
    "lease_liabilities": _Spec(("BS",), _ifrs("LeaseLiabilities"), ("리스부채",)),
    "interest_expense": _Spec(("IS", "CIS"), _ifrs("InterestExpense") + ("dart_InterestExpense",), ("이자비용",)),
    "oci": _Spec(("CIS",), _ifrs("OtherComprehensiveIncome", "OtherComprehensiveIncomeNetOfTax"), ("기타포괄손익", "기타포괄손익(세후)", "법인세차감후기타포괄손익")),
    "dividends_paid": _Spec(("CF",), _ifrs("DividendsPaid", "DividendsPaidClassifiedAsFinancingActivities"), ("배당금의 지급", "배당금 지급", "배당금지급"), cash_outflow=True),
    "equity_dividends": _Spec(("SCE",), _ifrs("DividendsRecognisedAsDistributionsToOwners", "DividendsPaid") + ("dart_Dividends",), ("배당금의 지급", "배당금", "연차배당", "소유주에 대한 배분으로 인식된 배당금"), cash_outflow=True),
    "equity_beginning": _Spec(("SCE",), ("dart_EquityAtBeginningOfPeriod",), ("기초자본", "기초 자본", "기초자본총계")),
    "equity_other_changes": _Spec(("SCE",), ("dart_OtherChangesInEquity",), ("기타자본변동", "기타 자본변동")),
    "equity_owner_transactions": _Spec(("SCE",), (), (
        "소유주와의 거래", "소유주와의 거래 합계", "자본에 직접 반영된 소유주와의 거래",
        "소유주와의 거래 총액", "소유주와의 거래 총계")),
}


def _viewer(receipt: str) -> str:
    return f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={receipt}"


def _text(value: object) -> str:
    return str(value or "").strip()


def _safe_index(payload: bytes) -> list[dict[str, str]]:
    if len(payload) > _MAX_RESPONSE:
        raise DartError("회사 고유번호 압축파일이 허용 크기를 넘었습니다.")
    try:
        with ZipFile(BytesIO(payload)) as archive:
            members = archive.infolist()
            if len(members) > 32 or sum(item.file_size for item in members) > _MAX_INDEX_XML:
                raise DartError("회사 고유번호 압축파일이 허용 한도를 넘었습니다.")
            files = []
            for member in members:
                path = PurePosixPath(member.filename.replace("\\", "/"))
                if path.is_absolute() or ".." in path.parts or re.match(r"^[A-Za-z]:", str(path)):
                    raise DartError("회사 고유번호 압축파일 경로가 올바르지 않습니다.")
                if member.flag_bits & 1 or stat.S_IFMT(member.external_attr >> 16) == stat.S_IFLNK:
                    raise DartError("회사 고유번호 압축파일 형식이 허용되지 않습니다.")
                if member.file_size > _MAX_INDEX_XML:
                    raise DartError("회사 고유번호 XML이 허용 크기를 넘었습니다.")
                if not member.is_dir() and member.filename.lower().endswith(".xml"):
                    files.append(archive.read(member))
            if len(files) != 1:
                raise DartError("회사 고유번호 XML을 하나로 식별하지 못했습니다.")
            root = ElementTree.fromstring(files[0], forbid_dtd=True, forbid_entities=True, forbid_external=True)
    except DartError:
        raise
    except (BadZipFile, OSError, ValueError, RuntimeError, ElementTree.ParseError, DefusedXmlException) as exc:
        raise DartError("회사 고유번호 ZIP/XML을 안전하게 해석하지 못했습니다.") from exc
    companies = []
    for row in root.findall("list"):
        code, name = _text(row.findtext("corp_code")), _text(row.findtext("corp_name"))
        stock = _text(row.findtext("stock_code"))
        if re.fullmatch(r"\d{8}", code) and name and (not stock or re.fullmatch(r"\d{6}", stock)):
            companies.append({"corp_code": code, "corp_name": name, "stock_code": stock})
    return companies


class DartClient:
    def __init__(self, api_key: str, client: httpx.Client | None = None, *, transport: httpx.BaseTransport | None = None, http_client: httpx.Client | None = None, today: date | None = None) -> None:
        if not isinstance(api_key, str) or not api_key.strip():
            raise DartError("OpenDART 인증키를 먼저 입력하세요.")
        if client is not None and http_client is not None:
            raise ValueError("HTTP 클라이언트는 하나만 전달하세요.")
        selected = client if client is not None else http_client
        if selected is not None and transport is not None:
            raise ValueError("클라이언트와 transport는 동시에 전달하지 마세요.")
        self._api_key = api_key.strip()
        self._owns_client = selected is None
        self._client = selected or httpx.Client(transport=transport, timeout=25, follow_redirects=False)
        self._today = today or date.today()
        self._companies: list[dict[str, str]] | None = None

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> DartClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _get(self, endpoint: str, **params: str | int) -> bytes:
        content = bytearray()
        try:
            with self._client.stream("GET", BASE_URL + endpoint, params={"crtfc_key": self._api_key, **params}) as response:
                response.raise_for_status()
                for chunk in response.iter_bytes(chunk_size=64 * 1024):
                    if len(content) + len(chunk) > _MAX_RESPONSE:
                        raise DartError("OpenDART 응답 크기가 허용 한도를 넘었습니다.")
                    content.extend(chunk)
        except httpx.HTTPStatusError as exc:
            raise DartError(f"OpenDART HTTP 응답 오류({exc.response.status_code})입니다.") from None
        except httpx.HTTPError:
            raise DartError("OpenDART와 통신하지 못했습니다. 연결 상태를 확인하세요.") from None
        return bytes(content)

    @staticmethod
    def _check_status(status: str) -> None:
        if status not in ("000", "013"):
            raise DartError(_ERRORS.get(status, "OpenDART에서 데이터를 처리하지 못했습니다."), status)

    def _json(self, endpoint: str, **params: str | int) -> dict:
        response = self._get(endpoint, **params)
        try:
            payload = json.loads(response)
        except ValueError:
            raise DartError("OpenDART JSON 응답을 해석하지 못했습니다.") from None
        if not isinstance(payload, dict) or not isinstance(payload.get("status"), str):
            raise DartError("OpenDART 응답 형식이 예상과 다릅니다.")
        self._check_status(payload["status"])
        if payload["status"] == "013":
            return {**payload, "list": []}
        return payload

    def _binary(self, endpoint: str, **params: str | int) -> bytes:
        content = self._get(endpoint, **params)
        if content[:2] == b"PK":
            return content
        try:
            root = ElementTree.fromstring(content, forbid_dtd=True, forbid_entities=True, forbid_external=True)
            status = _text(root.findtext("status"))
        except (ElementTree.ParseError, DefusedXmlException, ValueError):
            raise DartError("OpenDART 원본 응답이 ZIP 형식이 아닙니다.") from None
        if status == "013":
            raise DartError(_ERRORS[status], status)
        self._check_status(status)
        raise DartError("OpenDART 응답에서 원본 ZIP을 찾지 못했습니다.")

    def search_companies(self, query: str) -> list[dict[str, str]]:
        needle = query.strip().casefold()
        if not needle:
            return []
        if self._companies is None:
            self._companies = _safe_index(self._binary("corpCode.xml"))
        matches = [row.copy() for row in self._companies if needle in row["corp_name"].casefold() or needle in (row["stock_code"], row["corp_code"])]
        return sorted(matches, key=lambda row: (row["corp_name"].casefold() != needle, not bool(row["stock_code"]), row["corp_name"]))[:100]

    def _filings(self, corp_code: str) -> list[dict]:
        filings = []
        for page in range(1, 11):
            payload = self._json("list.json", corp_code=corp_code, bgn_de="20150101", end_de=self._today.strftime("%Y%m%d"), last_reprt_at="Y", pblntf_ty="A", page_count=100, page_no=page, sort="date", sort_mth="desc")
            rows = payload.get("list", [])
            if not isinstance(rows, list):
                raise DartError("공시 목록 형식을 해석하지 못했습니다.")
            filings.extend(row for row in rows if isinstance(row, dict))
            try:
                pages = int(payload.get("total_page", 1))
            except (ValueError, TypeError):
                raise DartError("공시 목록 페이지 수를 해석하지 못했습니다.") from None
            if page >= pages or not rows:
                return filings
        raise DartError("공시 목록이 처리 한도를 넘었습니다. 회사와 기간을 확인하세요.")

    def load_company(self, corp_code: str, name: str, stock_code: str = "", years: int = 5, scope: str = "CFS", include_interim: bool = True) -> Dataset:
        if not re.fullmatch(r"\d{8}", corp_code):
            raise ValueError("DART 고유번호는 8자리 숫자여야 합니다.")
        if scope not in ("CFS", "OFS"):
            raise ValueError("재무제표 기준은 CFS 또는 OFS여야 합니다.")
        if isinstance(years, bool) or not isinstance(years, int) or not 1 <= years <= 10:
            raise ValueError("분석 연수는 1~10년이어야 합니다.")
        dataset = Dataset(company=name, corp_code=corp_code, stock_code=stock_code, scope=scope, source_mode="live")
        dataset.metadata = {"as_of": self._today.isoformat(), "retrieved_at": datetime.now(timezone.utc).isoformat(), "requested_years": years, "scope": scope, "source": "금융감독원 OpenDART", "support": "전업종, 12월 결산 원화 재무제표. 미확인 항목은 보류.", "notes_are_risk_assessments": False}
        overview = self._json("company.json", corp_code=corp_code)
        month, industry = _text(overview.get("acc_mt")), _text(overview.get("induty_code"))
        dataset.metadata.update({"accounting_month": month, "industry_code": industry})
        dataset.metadata['period_context'] = '전체계정은 12월 결산 정규 사업연도 가정. XBRL 적용 계정은 원본의 시작·종료일 검증.'
        dataset.issues.append('기간 확인: 12월 결산의 정규 사업연도(1월~12월)를 가정합니다. 단기 사업연도·결산기 변경은 원문 기간을 확인해야 하며 현재 자동 지원하지 않습니다.')
        if month and month not in ("12", "012"):
            dataset.issues.append("현재 버전은 12월 결산만 지원합니다. 해당 기업의 결산월이 지원 범위와 다릅니다.")
            return dataset
        if dataset.has_financial_industry_code:
            dataset.issues.append(f"업종 코드 {industry} · 공시 계정 비교와 대조는 제공하며, 금융·보험 분류에서 해석 기준이 다른 일반기업용 지표는 보류합니다.")
        if not month:
            dataset.issues.append("기업개황에서 결산월을 확인하지 못했습니다. 12월 사업보고서만 분석합니다.")
        if not industry:
            dataset.issues.append("기업개황에서 업종을 확인하지 못했습니다. 금융업 해당 여부를 원문에서 확인하세요.")
        filings = self._filings(corp_code)
        selected: dict[tuple[int, int], dict] = {}
        for filing in filings:
            if "철" in _text(filing.get("rm")):
                continue
            match = _REPORT_PATTERN.search(_text(filing.get("report_nm")))
            receipt = _text(filing.get("rcept_no"))
            if not match or not re.fullmatch(r"\d{14}", receipt):
                continue
            report, year_text, month_text = match.groups()
            year, end_month = int(year_text), int(month_text)
            if year < 2015 or end_month not in _REPORT_CODES:
                continue
            if (report == "사업" and end_month != 12) or (report == "반기" and end_month != 6) or (report == "분기" and end_month not in (3, 9)):
                continue
            end = date(year, end_month, monthrange(year, end_month)[1])
            if end > self._today:
                continue
            group = (year, end_month)
            previous = selected.get(group)
            if previous is None or (_text(filing.get("rcept_dt")), receipt) > (_text(previous.get("rcept_dt")), _text(previous.get("rcept_no"))):
                selected[group] = filing
        annuals = sorted((group for group in selected if group[1] == 12), reverse=True)[:years]
        groups = list(annuals)
        if include_interim:
            interim = [group for group in selected if group[1] != 12 and (not annuals or group > annuals[0])]
            if interim:
                groups.append(max(interim))
        dataset.metadata["available_annual_years"] = [group[0] for group in sorted(selected, reverse=True) if group[1] == 12]
        if not groups:
            dataset.issues.append("지원 범위의 사업·분기보고서를 찾지 못했습니다. 데이터 없음은 0을 뜻하지 않습니다.")
            return dataset
        for year, end_month in sorted(groups):
            filing = selected[(year, end_month)]
            payload = self._json("fnlttSinglAcntAll.json", corp_code=corp_code, bsns_year=year, reprt_code=_REPORT_CODES[end_month], fs_div=scope)
            rows = payload.get("list", [])
            if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
                dataset.issues.append(f"{year}.{end_month:02d}: 계정 응답 형식이 올바르지 않아 보류했습니다.")
                continue
            receipt = _text(filing["rcept_no"])
            source_gap = ""
            if not rows:
                source_gap = f"{year}.{end_month:02d}: {scope} 전체계정 API 재무제표가 없습니다."
            if any(_text(row.get("rcept_no")) != receipt for row in rows):
                receipts = sorted({_text(row.get("rcept_no")) for row in rows})
                received = ", ".join(number if re.fullmatch(r"\d{14}", number) else "미확인" for number in receipts[:5])
                source_gap = f"{year}.{end_month:02d}: 선택한 최종 공시와 재무 API의 접수번호가 달라 전체계정 자료를 제외했습니다. 최종 공시 {receipt} · 재무 API {received}"
            if any(_text(row.get("corp_code", corp_code)) != corp_code or _text(row.get("fs_div", scope)) != scope or _text(row.get("bsns_year", year)) != str(year) or _text(row.get("reprt_code", _REPORT_CODES[end_month])) != _REPORT_CODES[end_month] for row in rows):
                dataset.issues.append(f"{year}.{end_month:02d}: 기간·연결/별도 기준이 다른 응답을 보류했습니다.")
                continue
            period = self._normalize([] if source_gap else rows, year, end_month, scope, receipt)
            recovered = False
            if month in ("12", "012"):
                recovered = self._apply_xbrl(period, corp_code, _REPORT_CODES[end_month])
            if source_gap:
                if not recovered:
                    detail = " · ".join(period.issues)
                    dataset.issues.append(source_gap + " · 동일 공시 XBRL 복구 실패로 해당 기간을 보류했습니다." + (f" {detail}" if detail else ""))
                    dataset.metadata.setdefault("filing_gaps", []).append({
                        "period": period.label, "selected_receipt": receipt,
                        "api_receipts": sorted({_text(row.get("rcept_no")) for row in rows
                                                if re.fullmatch(r"\d{14}", _text(row.get("rcept_no")))}),
                        "reason": detail or source_gap,
                    })
                    continue
                period.issues.append(source_gap + " · 선택한 최종 공시 XBRL에서 확인된 계정만 복구했습니다.")
            if "정" in _text(filing.get("rm")):
                period.issues.append("공시 목록에 후속 정정 안내가 남아 있습니다. 최종 접수번호와 원문을 확인하세요.")
            dataset.periods.append(period)
        dataset.metadata["loaded_annual_count"] = sum(period.kind == "FY" for period in dataset.periods)
        dataset.metadata["loaded_period_count"] = len(dataset.periods)
        if dataset.metadata["loaded_annual_count"] < years:
            dataset.issues.append("요청한 연수보다 유효한 연간 재무제표가 적습니다. 이용 가능한 기간만 표시합니다.")
        if dataset.periods:
            latest = max(dataset.periods, key=lambda period: period.end)
            dataset.metadata["latest_filing_id"] = latest.filing_id
            try:
                original = self._binary("document.xml", rcept_no=latest.filing_id)
                dataset.notes = parse_note_topics(original, latest.filing_id, _viewer(latest.filing_id), include_operating_context=True)
            except DartError as exc:
                dataset.issues.append(f"원문 주석을 가져오지 못했습니다: {exc}")
                dataset.notes = [{"topic": topic, "status": "추출 실패", "excerpt": "", "source_id": latest.filing_id, "source_url": _viewer(latest.filing_id), "location": "원문을 내려받지 못함"} for topic in ("회계정책", "차입금·유동성", "우발채무·약정", "특수관계자", "감사의견")]
            else:
                if dataset.notes and all(note["status"] == "추출 실패" for note in dataset.notes):
                    dataset.issues.append(f"{latest.label} 원문 주석 추출 보류 · {dataset.notes[0]['location']}")
        return dataset

    def _apply_xbrl(self, period: Period, corp_code: str, report_code: str) -> bool:
        receipt = period.filing_id
        try:
            payload = self._binary(_XBRL_ENDPOINT, rcept_no=receipt, reprt_code=report_code)
            instance = read_xbrl_archive(payload)
        except (DartError, XbrlError) as exc:
            period.issues.append(f"{period.label} 원본 XBRL 검증 보류 ({receipt}) · {exc}")
            return False

        by_concept: dict[str, list[XbrlFact]] = {}
        extension_ids: dict[str, set[str]] = {}
        if instance.label_error:
            period.issues.append(f"확장 계정의 라벨 검증 보류 · {instance.label_error}")
        for fact in instance.facts:
            context = fact.context
            concept = fact.standard_account_id
            if concept is None and re.fullmatch(
                    r"\{https?://dart\.fss\.or\.kr/taxonomy/\d{4}-\d{2}-\d{2}/entity" + corp_code + r"\}.+",
                    fact.concept):
                labels = instance.labels.get(fact.concept, ())
                if len(labels) == 1:
                    for key, spec in _SPECS.items():
                        if not spec.ids and labels[0] in spec.aliases:
                            concept = fact.concept
                            extension_ids.setdefault(key, set()).add(concept)
            if (concept and context.identifier == corp_code and context.identifier_scheme == DART_IDENTIFIER_SCHEME
                    and context.scope == period.scope and len(context.dimensions) == 1
                    and not context.has_other_content and fact.currency == "KRW"):
                by_concept.setdefault(concept, []).append(fact)

        for key, spec in _SPECS.items():
            ids = {account.replace("ifrs_", "ifrs-full_", 1) if account.startswith("ifrs_") else account
                   for account in spec.ids}
            ids.update(extension_ids.get(key, ()))
            matching_rows = [
                row for row in period.raw_accounts
                if row.get("sj_div") in spec.statements and row.get("currency") == "KRW"
                and row.get("account_id") in spec.ids
                and (row.get("sj_div") != "SCE" or _text(row.get("account_detail")) in {
                    "자본 [member]", "자본총계", "자본 합계",
                    "연결재무제표 [member]" if period.scope == "CFS" else "별도재무제표 [member]",
                })
            ]
            # Prefer the presented CF dividend classification over a broader
            # dividend concept also reported in the notes.
            if key == "dividends_paid" and any(
                    row.get("account_id") == "ifrs-full_DividendsPaidClassifiedAsFinancingActivities"
                    for row in matching_rows):
                ids = {"ifrs-full_DividendsPaidClassifiedAsFinancingActivities"}
                matching_rows = [row for row in matching_rows if row["account_id"] in ids]
            presented = {str(row["account_id"]).replace("ifrs_", "ifrs-full_", 1)
                         if str(row["account_id"]).startswith("ifrs_") else str(row["account_id"])
                         for row in matching_rows}
            if presented:
                ids &= presented
            original_facts = [fact for account in ids for fact in by_concept.get(account, [])]
            if not original_facts:
                continue
            needs_statement_row = key in ("cash_beginning", "cash_end", "dividends_paid", "equity_dividends")
            if needs_statement_row and not matching_rows:
                continue
            statement = str(matching_rows[0]["sj_div"]) if matching_rows else spec.statements[0]
            label = _text(matching_rows[0].get("account_nm")) if matching_rows else spec.aliases[0]
            for collection, offset, column_label in (
                (period.facts, 0, "당기"), (period.comparatives, 1, "전기 비교"),
            ):
                year = period.year - offset
                end_month = 12 if statement == "BS" and offset else date.fromisoformat(period.end).month
                end = date(year, end_month, monthrange(year, end_month)[1])
                start = end if statement == "BS" else date(year, 1, 1)
                field_name = ("frmtrm_" if offset else "thstrm_") + (
                    "add_amount" if period.kind == "YTD" and statement in ("IS", "CIS", "SCE") else "amount")
                candidates = [
                    fact for fact in original_facts
                    if (fact.context.instant == end if key in ("cash_beginning", "cash_end") or statement == "BS"
                        else (fact.context.start, fact.context.end) == (start, end))
                ]
                existing = collection.get(key)
                if (key in {"borrowings", "lease_liabilities"} and existing is not None
                        and not matching_rows and " + " in existing.account_id
                        and self._verify_debt_components(existing, period, by_concept, end, field_name)):
                    existing.source_details.update({
                        "report_code": report_code, "member": instance.member_name,
                        "unselected_total_values": [str(item.value) for item in candidates],
                    })
                    continue
                if not candidates and existing is not None and existing.amount is not None:
                    continue
                if not candidates and offset == 0:
                    continue
                values = {fact.value for fact in candidates}
                json_values = self._source_amounts(matching_rows, field_name)
                if spec.cash_outflow:
                    values = {abs(value) for value in values}
                    json_values = {abs(value) for value in json_values}
                if existing is not None and existing.amount is not None:
                    json_values.add(existing.amount * existing.unit)
                amount = None
                rounding_unit = Decimal(0)
                api_value_used = False
                with localcontext() as context:
                    context.prec = 256
                    reported = [(abs(f.value) if spec.cash_outflow else f.value, f.rounding_unit) for f in candidates]
                    lower = max((value - unit / 2 for value, unit in reported), default=Decimal(0))
                    upper = min((value + unit / 2 for value, unit in reported), default=Decimal(0))
                    representative = min(reported, key=lambda item: item[1], default=(Decimal(0), Decimal(0)))
                if not values:
                    reason = "회사·기간·범위·통화 조건을 충족하는 원본 XBRL 비교값 미확보"
                elif needs_statement_row and not json_values:
                    reason = ("자본변동표의 누적 비교값을 재무 API에서 확인하지 못함" if statement == "SCE"
                              else "현금흐름표 계정의 전체계정 API 비교값 미확보")
                elif lower > upper or (not json_values and not lower <= representative[0] <= upper):
                    reason = "동일한 범위의 원본 XBRL 금액이 서로 다름"
                elif len(json_values) > 1 or any(value < lower or value > upper for value in json_values):
                    reason = "원본 XBRL과 전체계정 API의 금액이 서로 다름"
                else:
                    value, rounding_unit = representative
                    if json_values and next(iter(json_values)) != value:
                        value = next(iter(json_values))
                        rounding_unit = Decimal(1)
                        api_value_used = True
                    digits = value.as_tuple()
                    if len(digits.digits) > 50 or abs(int(digits.exponent)) > 20:
                        reason = "분석 자료가 지원하는 금액 정밀도 범위 초과"
                    else:
                        amount = value
                        reason = "원본 XBRL의 회사·기간·연결 범위·통화 확인"
                if amount is None:
                    period.issues.append(f"{label} {column_label} ({receipt}) · {reason}. 분석을 보류했습니다.")
                elif offset == 0:
                    period.issues[:] = [issue for issue in period.issues if not issue.startswith(f"{key}: ")]
                account_ids = sorted({fact.standard_account_id for fact in candidates if fact.standard_account_id})
                collection[key] = Fact(
                    key=key, name=label, amount=amount, statement=statement, start=start.isoformat(),
                    end=end.isoformat(), scope=period.scope, currency="KRW", source_id=receipt,
                    source_url=_viewer(receipt), account_id=account_ids[0] if account_ids else sorted(ids)[0],
                    source_field="xbrl_verified_api" if api_value_used else "xbrl_fact", attribution=spec.attribution,
                    period_kind="POINT" if statement == "BS" else period.kind, reason=reason,
                    source_details={
                        "api": _XBRL_ENDPOINT, "report_code": report_code, "member": instance.member_name,
                        "value_api": "fnlttSinglAcntAll.json" if api_value_used else _XBRL_ENDPOINT,
                        "rounding_unit": str(rounding_unit),
                        "concept_labels": {item.concept: instance.labels[item.concept]
                                           for item in candidates if item.concept in instance.labels},
                        "label_sources": instance.label_sources if key in extension_ids else (),
                        "candidates": [
                            {"concept": fact.concept, "context_id": fact.context_id,
                             "identifier": fact.context.identifier, "identifier_scheme": fact.context.identifier_scheme,
                             "axis": fact.context.dimensions[0].axis, "member": fact.context.dimensions[0].member,
                             "dimension_location": fact.context.dimensions[0].location, "unit": fact.unit,
                             "start": fact.context.start.isoformat() if fact.context.start else None,
                             "end": fact.context.end.isoformat() if fact.context.end else None,
                             "instant": fact.context.instant.isoformat() if fact.context.instant else None,
                             "amount": str(fact.value), "decimals": fact.decimals, "precision": fact.precision}
                            for fact in candidates
                        ],
                        "all_account_api_amounts": [str(value) for value in sorted(json_values)],
                    },
                )
        return any(fact.source_field in {"xbrl_fact", "xbrl_verified_api"} and fact.amount is not None for fact in period.facts.values())

    @staticmethod
    def _verify_debt_components(fact: Fact, period: Period, by_concept: dict[str, list[XbrlFact]],
                                end: date, field_name: str) -> bool:
        proof = []
        accounts = fact.account_id.split(" + ")
        if len(accounts) != 2:
            return False
        with localcontext() as context:
            context.prec = 256
            total = Decimal(0)
            for account in accounts:
                rows = [row for row in period.raw_accounts if row.get("account_id") == account
                        and row.get("sj_div") == "BS" and row.get("currency") == "KRW"]
                if len(rows) != 1:
                    return False
                try:
                    value = parse_amount(rows[0].get(field_name))
                except ValueError:
                    return False
                concept = account.replace("ifrs_", "ifrs-full_", 1) if account.startswith("ifrs_") else account
                candidates = [item for item in by_concept.get(concept, []) if item.context.instant == end]
                if value is None or not candidates or any(
                        abs(value - item.value) > item.rounding_unit / 2 for item in candidates):
                    return False
                total += value
                proof.extend({"concept": item.concept, "context_id": item.context_id, "amount": str(item.value),
                              "instant": end.isoformat(), "decimals": item.decimals, "unit": item.unit,
                              "identifier": item.context.identifier, "axis": item.context.dimensions[0].axis,
                              "member": item.context.dimensions[0].member} for item in candidates)
            if total != fact.amount:
                return False
        fact.source_field = "xbrl_verified_api"
        fact.reason += "; 유동·비유동 구성 계정을 XBRL에서 각각 검증"
        fact.source_details = {
            "api": _XBRL_ENDPOINT, "value_api": "fnlttSinglAcntAll.json", "aggregation": "sum_explicit_components",
            "candidates": proof, "rounding_unit": "1",
        }
        return True

    @staticmethod
    def _source_amounts(rows: list[dict], field_name: str) -> set[Decimal]:
        amounts = set()
        for row in rows:
            try:
                value = parse_amount(row.get(field_name))
            except ValueError:
                continue
            if value is not None:
                amounts.add(value)
        return amounts

    @staticmethod
    def _normalize(rows: list[dict], year: int, end_month: int, scope: str, receipt: str) -> Period:
        start = f"{year}-01-01"
        end = f"{year}-{end_month:02d}-{monthrange(year, end_month)[1]}"
        annual = end_month == 12
        kind = "FY" if annual else "YTD"
        label = str(year) if annual else f"{year} {end_month // 3}분기 누적"
        period = Period(label=label, year=year, start=start, end=end, scope=scope, kind=kind, filing_id=receipt, raw_accounts=[dict(row) for row in rows])
        for key, spec in _SPECS.items():
            candidates = []
            for row in rows:
                if _text(row.get("sj_div")) not in spec.statements:
                    continue
                account_id, account_name = _text(row.get("account_id")), _text(row.get("account_nm"))
                exact = account_id in spec.ids
                # An exact Korean name cannot override a contradictory known
                # taxonomy ID (e.g. CurrentBorrowings named merely '차입금').
                # Aliases are only a fallback for absent/custom identifiers.
                alias = account_name in spec.aliases and not account_id.startswith(("ifrs-full_", "ifrs_", "dart_"))
                if not (exact or alias):
                    continue
                if _text(row.get("sj_div")) == "SCE" and _text(row.get("account_detail")) not in (
                    "자본 [member]", "자본총계", "자본 합계",
                    "연결재무제표 [member]" if scope == "CFS" else "별도재무제표 [member]",
                ):
                    continue
                candidates.append(row)
            mirrored_rows = []
            if (len(candidates) == 2 and {row.get("sj_div") for row in candidates} == {"IS", "CIS"}
                    and candidates[0].get("account_id") in spec.ids
                    and all(_text(candidates[0].get(field)) == _text(candidates[1].get(field))
                            for field in ("account_id", "account_detail", "currency", "unit"))):
                fields = ("thstrm_amount", "frmtrm_amount", "thstrm_add_amount", "frmtrm_add_amount")
                try:
                    same = all((field in candidates[0]) == (field in candidates[1])
                               and parse_amount(candidates[0].get(field)) == parse_amount(candidates[1].get(field))
                               for field in fields)
                except ValueError:
                    same = False
                if same:
                    mirrored_rows = candidates
                    candidates = [next(row for row in candidates if row["sj_div"] == "IS")]
            if len(candidates) > 1:
                period.issues.append(f"{key}: 일치 후보가 여러 개여서 자동 선택하지 않았습니다.")
                continue
            if not candidates:
                continue
            row = candidates[0]
            currency = _text(row.get("currency"))
            if currency != "KRW":
                period.issues.append(f"{key}: 통화가 KRW로 확인되지 않아 정규화를 보류했습니다.")
                continue
            statement = _text(row.get("sj_div"))
            if not annual and statement in ("CF", "SCE"):
                # All-account responses do not provide machine-readable duration
                # for these statements. Do not turn an assumed YTD into a fact.
                hold = INTERIM_CF_HOLD if statement == "CF" else "재무 API 응답에서 자본변동표의 누적 기간을 검증할 수 없어 원본 XBRL 확인 전까지 보류했습니다."
                period.issues.append(f"{key}: {hold}")
                continue
            current_field = "thstrm_add_amount" if not annual and statement in ("IS", "CIS") else "thstrm_amount"
            prior_field = "frmtrm_add_amount" if not annual and statement in ("IS", "CIS") else "frmtrm_amount"
            for collection, field_name, target_year in ((period.facts, current_field, year), (period.comparatives, prior_field, year - 1)):
                reason = "정확한 XBRL ID" if _text(row.get("account_id")) in spec.ids else "승인된 정확 계정명"
                try:
                    amount = parse_amount(row.get(field_name))
                except ValueError:
                    period.issues.append(f"{key}: {field_name} 금액 형식이 올바르지 않습니다.")
                    if collection is period.facts:
                        continue
                    amount = None
                    reason += "; 최신 공시 비교열의 금액 형식 오류: 과거 공시로 대체하지 않음"
                if amount is None:
                    if collection is period.facts or field_name not in row:
                        continue
                    # A blank or malformed comparative in the selected filing
                    # is an explicit gap, not permission to reuse stale data
                    # from a previous filing with a potentially different basis.
                    if "금액 형식 오류" not in reason:
                        reason += "; 최신 공시 비교열 미확보: 과거 공시로 대체하지 않음"
                if spec.cash_outflow and amount is not None:
                    amount = abs(amount)
                # BS comparative columns are previous fiscal year-end, even in
                # interim filings; they are not last year's same-quarter BS.
                fact_end_month = 12 if statement == "BS" and collection is period.comparatives else end_month
                fact_end = f"{target_year}-{fact_end_month:02d}-{monthrange(target_year, fact_end_month)[1]}"
                fact_start = fact_end if statement == "BS" else f"{target_year}-01-01"
                collection[key] = Fact(key=key, name=_text(row.get("account_nm")), amount=amount, statement=statement, start=fact_start, end=fact_end, scope=scope, currency=currency, source_id=receipt, source_url=_viewer(receipt), account_id=_text(row.get("account_id")), source_field=field_name, attribution=spec.attribution, period_kind="POINT" if statement == "BS" else kind, reason=reason)
                if mirrored_rows:
                    collection[key].source_details = {
                        "api": "fnlttSinglAcntAll.json", "mirrored_rows": [dict(item) for item in mirrored_rows],
                    }
        # No residual calculations or partial sums are used to invent missing
        # debt totals. Only both explicit current/noncurrent categories qualify.
        for key, component_ids in {
            "borrowings": (_ifrs("CurrentBorrowings"), _ifrs("NoncurrentBorrowings")),
            "lease_liabilities": (_ifrs("CurrentLeaseLiabilities"), _ifrs("NoncurrentLeaseLiabilities")),
        }.items():
            if key in period.facts:
                continue
            components = [[row for row in rows if _text(row.get("sj_div")) == "BS" and _text(row.get("account_id")) in ids and _text(row.get("currency")) == "KRW"] for ids in component_ids]
            if not all(len(items) == 1 for items in components):
                continue
            for collection, field_name, target_year in ((period.facts, "thstrm_amount", year), (period.comparatives, "frmtrm_amount", year - 1)):
                try:
                    amounts = [parse_amount(items[0].get(field_name)) for items in components]
                except ValueError:
                    continue
                present = [amount for amount in amounts if amount is not None]
                if len(present) != len(amounts):
                    continue
                with localcontext() as context:
                    context.prec = max(50, *(len(amount.as_tuple().digits) + abs(int(amount.as_tuple().exponent)) + 5 for amount in present))
                    total = sum(present, Decimal(0))
                point_month = end_month if target_year == year else 12
                point = f"{target_year}-{point_month:02d}-{monthrange(target_year, point_month)[1]}"
                collection[key] = Fact(key=key, name="유동·비유동 분류 합계", amount=total, statement="BS", start=point, end=point, scope=scope, source_id=receipt, source_url=_viewer(receipt), account_id=" + ".join(_text(items[0].get("account_id")) for items in components), source_field=field_name, period_kind="POINT", reason="유동·비유동 차입/리스 분류가 모두 확인된 경우에만 합산")
        if "borrowings" in period.facts or "borrowings" in period.comparatives:
            for collection in (period.facts, period.comparatives):
                if "borrowings" in collection:
                    collection["borrowings"].reason += "; 리스 포함 여부 미확인"
            period.issues.append("공시 차입금의 리스 포함 여부 미확인: 리스부채를 다시 더하기 전에 원문 분류를 확인해야 합니다.")
        return period

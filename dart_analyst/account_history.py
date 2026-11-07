"""Conservative history comparisons for the full OpenDART account response.

This preserves account dimensions and does not sum accounts into a new ledger.
An exact, known taxonomy concept is a candidate identity; neither line order nor
similar account names establish continuity.  Unverified custom concepts and
interim CF/SCE duration stay visible as uncomparable rows.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import re

from .models import Dataset, Period


_STATEMENTS = {"BS", "IS", "CIS", "CF", "SCE"}
_KNOWN_PREFIXES = ("ifrs-full_", "ifrs_", "dart_", "ifrs-full:", "dart:")
_PLACEHOLDERS = {"", "-", "N/A", "NA", "-표준계정코드미사용-", "표준계정코드미사용"}
_REPORT_CODES = {3: "11013", 6: "11012", 9: "11014", 12: "11011"}


def _text(value: object) -> str:
    return "" if value is None else str(value).strip()


def _s(value: Decimal | None) -> str | None:
    return None if value is None else format(value, "f")


def _number(value: object) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, (bool, float)):
        raise ValueError("원본 숫자 문자열/정수/Decimal만 허용합니다")
    text = str(value).strip().replace("\u2212", "-")
    if text in {"", "-", "—", "–"}:
        return None
    if text.startswith("(") and text.endswith(")"):
        text = "-" + text[1:-1].strip()
    if not re.fullmatch(r"[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?", text):
        raise ValueError("금액 형식 오류")
    result = Decimal(text.replace(",", ""))
    if not result.is_finite():
        raise ValueError("유한하지 않은 금액")
    return result


def _previous_date(value: str) -> str:
    d = date.fromisoformat(value)
    try:
        return d.replace(year=d.year - 1).isoformat()
    except ValueError:
        return d.replace(year=d.year - 1, day=28).isoformat()


def _identity(row: dict) -> tuple[str, str, str]:
    return (_text(row.get("sj_div")), _text(row.get("account_id")), _text(row.get("account_detail")))


def _group(period: Period | None) -> dict[tuple[str, str, str], list[dict]]:
    groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    if period is not None:
        for index, raw in enumerate(period.raw_accounts):
            if isinstance(raw, dict):
                row = dict(raw)
                row["_raw_row_index"] = index
                groups[_identity(row)].append(row)
    return dict(groups)


def _valid_period(dataset: Dataset, p: Period) -> str:
    try:
        start, end = date.fromisoformat(p.start), date.fromisoformat(p.end)
    except ValueError:
        return "기간 메타데이터 해석 실패"
    if p.scope != dataset.scope or p.scope not in {"CFS", "OFS"}:
        return "연결/별도 분석 범위 불일치"
    if start.year != p.year or end.year != p.year or start > end:
        return "사업연도와 기간 불일치"
    if start.month != 1 or start.day != 1:
        return "현재 전체계정 비교는 1월 시작 회계기간만 지원"
    if p.kind == "FY":
        if (end.month, end.day) != (12, 31):
            return "연간 회계기간 불일치"
    elif p.kind == "YTD":
        if end.month not in {3, 6, 9} or (end.month, end.day) not in {(3, 31), (6, 30), (9, 30)}:
            return "누적 중간 회계기간 불일치"
    else:
        return "단독 분기 등 미지원 기간 종류"
    return ""


def _metadata(dataset: Dataset, p: Period, row: dict) -> tuple[str, Decimal, str]:
    """Return currency, normalized source multiplier, error.

    OpenDART all-account API amounts are in the currency returned by the API.
    The optional numeric `unit` is an explicit, known multiplier for imported
    fixtures. Missing currency may only be recovered from an unambiguous
    validated canonical Fact for the exact same raw source concept.
    """
    error = _valid_period(dataset, p)
    if error:
        return "", Decimal(1), error
    statement, account_id, detail = _identity(row)
    if statement not in _STATEMENTS:
        return "", Decimal(1), "재무제표 종류 미확인"
    if row.get("fs_div") is not None and _text(row["fs_div"]) != p.scope:
        return "", Decimal(1), "원천 행의 연결/별도 범위 불일치"
    if row.get("corp_code") is not None and dataset.corp_code and _text(row["corp_code"]) != dataset.corp_code:
        return "", Decimal(1), "원천 행의 회사 고유번호 불일치"
    if row.get("rcept_no") is not None and _text(row["rcept_no"]) != p.filing_id:
        return "", Decimal(1), "원천 행과 선택 공시 접수번호 불일치"
    if row.get("bsns_year") is not None and _text(row["bsns_year"]) != str(p.year):
        return "", Decimal(1), "원천 행의 사업연도 불일치"
    if row.get("reprt_code") is not None and _text(row["reprt_code"]) != _REPORT_CODES[date.fromisoformat(p.end).month]:
        return "", Decimal(1), "원천 행의 보고서 종류 불일치"
    currency = _text(row.get("currency"))
    try:
        unit = _number(row.get("unit", "1"))
        if unit is None or unit <= 0:
            raise ValueError("단위 오류")
    except (ValueError, InvalidOperation):
        return "", Decimal(1), "확인되지 않은 원천 표시 단위"
    if not currency:
        candidates = [f for f in p.facts.values() if f.account_id == account_id
                      and f.statement == statement and f.scope == p.scope
                      and f.source_id == p.filing_id and f.amount is not None]
        # Only an exact source identity can fill demonstrational metadata.
        if len(candidates) == 1:
            f = candidates[0]
            expected_start = p.end if statement == "BS" else p.start
            if f.start == expected_start and f.end == p.end and (statement == "BS" or f.period_kind == p.kind):
                currency, unit = f.currency, f.unit
        if not currency:
            return "", Decimal(1), "원천 통화 미확인"
    try:
        unit = _number(unit)
        if unit is None or unit <= 0:
            raise ValueError("단위 오류")
    except (ValueError, InvalidOperation):
        return "", Decimal(1), "확인되지 않은 원천 표시 단위"
    if not re.fullmatch(r"[A-Z]{3}", currency):
        return "", Decimal(1), "통화 코드 해석 실패"
    if statement == "SCE" and not detail:
        return currency, unit, "자본변동표 자본 구성원(account_detail) 미확인"
    if p.kind == "YTD" and statement in {"CF", "SCE"}:
        if statement != "CF" or not _verified_xbrl_row(p, row, currency, unit):
            return currency, unit, "중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인"
    return currency, unit, ""


def _verified_xbrl_row(period: Period, row: dict, currency: str, unit: Decimal) -> bool:
    account_id = _text(row.get("account_id"))
    if account_id.startswith("ifrs_"):
        account_id = account_id.replace("ifrs_", "ifrs-full_", 1)
    matches = [fact for fact in period.facts.values()
               if fact.account_id == account_id and fact.statement == "CF"]
    if len(matches) != 1 or unit != 1:
        return False
    current = matches[0]
    previous = period.comparatives.get(current.key)
    if previous is None:
        return False
    for fact, offset, field in ((current, 0, "thstrm_amount"), (previous, 1, "frmtrm_amount")):
        if (fact.source_id != period.filing_id or fact.source_field not in {"xbrl_fact", "xbrl_verified_api"}
                or fact.scope != period.scope or fact.currency != currency or fact.unit != unit
                or fact.period_kind != period.kind or fact.amount is None
                or fact.start != (period.start if offset == 0 else _previous_date(period.start))
                or fact.end != (period.end if offset == 0 else _previous_date(period.end))
                or fact.source_details.get("api") != "fnlttXbrl.xml"
                or not fact.source_details.get("candidates")):
            return False
        try:
            raw = _number(row.get(field))
        except ValueError:
            return False
        if raw != fact.amount:
            return False
    return True


def _supported_identity(dataset: Dataset, row: dict) -> bool:
    account_id = _text(row.get("account_id"))
    if account_id in _PLACEHOLDERS:
        return False
    if account_id.startswith(_KNOWN_PREFIXES):
        return True
    demo_source = dataset.source_mode == 'demo' or (dataset.source_mode == 'import' and dataset.metadata.get('original_source_mode') == 'demo')
    return demo_source and account_id.startswith("demo:")


def _fields(p: Period, statement: str) -> tuple[str, str]:
    if p.kind == "YTD" and statement in {"IS", "CIS"}:
        return "thstrm_add_amount", "frmtrm_add_amount"
    return "thstrm_amount", "frmtrm_amount"


def _target(p: Period, statement: str) -> tuple[str, str, str]:
    if statement == "BS":
        return _previous_date(p.start)[:4] + "-01-01", f"{p.year - 1}-12-31", "전기말 잔액"
    return _previous_date(p.start), _previous_date(p.end), "전년 동일 기간"


def _historical_period(dataset: Dataset, p: Period, statement: str) -> tuple[Period | None, str]:
    start, end, _ = _target(p, statement)
    wanted_kind = "FY" if statement == "BS" else p.kind
    matches = [prior for prior in dataset.periods if prior is not p
               and prior.start == start and prior.end == end and prior.kind == wanted_kind]
    if len(matches) > 1:
        return None, "전기 기간 후보 중복"
    if matches:
        return matches[0], ""
    return None, "전기 원본 기간 미확보"


def compare_raw_accounts(dataset: Dataset) -> list[dict]:
    """Compare each exact full-account identity without semantic fuzzy matches."""
    output: list[dict] = []
    with localcontext() as ctx:
        ctx.prec = 34
        for p in sorted(dataset.periods, key=lambda x: (x.end, x.start, x.label)):
            current_groups = _group(p)
            identities = set(current_groups)
            histories: dict[str, tuple[Period | None, str, dict]] = {}
            for statement in _STATEMENTS:
                try:
                    prior, error = _historical_period(dataset, p, statement)
                except ValueError:
                    prior, error = None, "기간 메타데이터 해석 실패"
                historical_groups = _group(prior)
                histories[statement] = (prior, error, historical_groups)
                identities.update(identity for identity in historical_groups if identity[0] == statement)
            for identity in sorted(identities):
                statement, account_id, detail = identity
                current_rows = current_groups.get(identity, [])
                prior, prior_error, prior_groups = histories.get(statement, (None, "재무제표 종류 미확인", {}))
                historical_rows = prior_groups.get(identity, [])
                representative = (current_rows or historical_rows)[0]
                digest = hashlib.sha256("\x1f".join(identity).encode()).hexdigest()[:16]
                row = {"key": "raw:" + digest, "account_id": account_id,
                       "account_name": _text(representative.get("account_nm")),
                       "account_detail": detail, "sj_div": statement, "scope": p.scope,
                       "currency": None, "unit": None, "to_period": p.label,
                       "from_period": None, "current": None, "previous": None,
                       "delta": None, "pct": None, "status": "missing_source", "reason": "",
                       "comparison_basis": "", "source_ids": [], "source_urls": [],
                       "current_field": "", "previous_field": "", "restated": False,
                       "raw_row_indexes": [r["_raw_row_index"] for r in current_rows]}
                output.append(row)
                error = _valid_period(dataset, p)
                if error:
                    row.update(status="not_comparable", reason=error)
                    continue
                if not _supported_identity(dataset, representative):
                    row.update(status="mapping_pending", reason="비표준·회사 확장·미사용 계정코드는 승인 매핑 없이 자동 연결하지 않음")
                    continue
                if len(current_rows) > 1:
                    row.update(status="duplicate", reason="같은 재무제표·계정 ID·구성원에 원천 행이 여러 개임")
                    continue
                if not current_rows:
                    # A vanished presentation line is not a zero balance.
                    related = any(ident[1] == account_id for ident in current_groups)
                    row.update(status="context_changed" if related else "missing_current",
                               reason="당기 재무제표/구성원 표시 문맥 변경 가능; 자동 재분류하지 않음" if related else "당기 계정 미노출·미확보; 0으로 간주하지 않음")
                    if len(historical_rows) == 1 and prior is not None:
                        currency, unit, error = _metadata(dataset, prior, historical_rows[0])
                        if not error:
                            try:
                                value = _number(historical_rows[0].get(_fields(prior, statement)[0]))
                                row.update(previous=_s(value * unit) if value is not None else None,
                                           from_period=prior.label, currency=currency)
                            except ValueError:
                                pass
                    continue
                current_row = current_rows[0]
                currency, multiplier, error = _metadata(dataset, p, current_row)
                if error:
                    row.update(status="not_comparable", reason=error)
                    continue
                row.update(currency=currency, unit=currency, source_ids=[p.filing_id] if p.filing_id else [])
                source_url = _text(current_row.get("source_url"))
                if not source_url and dataset.source_mode in {"dart", "live", "import"} and re.fullmatch(r"\d{14}", p.filing_id):
                    source_url = f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={p.filing_id}"
                if source_url:
                    row["source_urls"] = [source_url]
                current_field, comparative_field = _fields(p, statement)
                row["current_field"] = current_field
                try:
                    amount = _number(current_row.get(current_field))
                except ValueError:
                    row.update(status="invalid_amount", reason="당기 금액 형식 오류")
                    continue
                if amount is None:
                    row.update(status="missing_current", reason="당기 금액 미확보; 0으로 간주하지 않음")
                    continue
                row["current"] = _s(amount * multiplier)
                target_start, target_end, description = _target(p, statement)
                row["from_period"] = target_end if statement == "BS" else f"{target_start}~{target_end}"
                row["comparison_basis"] = description
                before: Decimal | None = None
                if comparative_field in current_row:
                    # An explicitly blank/invalid comparative must not silently
                    # fall back to an older, possibly unrevised filing.
                    row["previous_field"] = comparative_field
                    row["comparison_basis"] += " · 당기 공시 비교열 우선"
                    try:
                        raw_before = _number(current_row[comparative_field])
                    except ValueError:
                        row.update(status="invalid_amount", reason="당기 공시 비교열 금액 형식 오류")
                        continue
                    if raw_before is None:
                        row.update(status="missing_previous", reason="당기 공시 비교열 미확보; 과거 공시로 대체하지 않음")
                        continue
                    before = raw_before * multiplier
                else:
                    if len(historical_rows) > 1:
                        row.update(status="duplicate", reason="전기 동일 계정·문맥 행 중복")
                        continue
                    if not historical_rows or prior is None:
                        related = any(ident[1] == account_id for ident in prior_groups)
                        row.update(status="context_changed" if related else "missing_previous",
                                   reason="전기 재무제표/구성원 표시 문맥 변경 가능; 자동 재분류하지 않음" if related else prior_error or "전기 동일 계정 미확보")
                        continue
                    previous_row = historical_rows[0]
                    previous_currency, previous_multiplier, error = _metadata(dataset, prior, previous_row)
                    if error or previous_currency != currency or prior.scope != p.scope:
                        row.update(status="not_comparable", reason=error or "전기 통화·연결범위 불일치")
                        continue
                    previous_field = _fields(prior, statement)[0]
                    row["previous_field"] = previous_field
                    row["comparison_basis"] += " · 검증된 전기 공시"
                    try:
                        raw_before = _number(previous_row.get(previous_field))
                    except ValueError:
                        row.update(status="invalid_amount", reason="전기 금액 형식 오류")
                        continue
                    if raw_before is None:
                        row.update(status="missing_previous", reason="전기 금액 미확보")
                        continue
                    before = raw_before * previous_multiplier
                    if prior.filing_id and prior.filing_id not in row["source_ids"]:
                        row["source_ids"].append(prior.filing_id)
                    previous_url = _text(previous_row.get("source_url"))
                    if not previous_url and dataset.source_mode in {"dart", "live", "import"} and re.fullmatch(r"\d{14}", prior.filing_id):
                        previous_url = f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={prior.filing_id}"
                    if previous_url and previous_url not in row["source_urls"]:
                        row["source_urls"].append(previous_url)
                after = amount * multiplier
                row.update(previous=_s(before), delta=_s(after - before),
                           pct=_s((after - before) / before * 100) if before > 0 else None,
                           status="calculated", reason="" if before > 0 else "비교기≤0: 증감률 대신 금액 차이 표시")
                if len(historical_rows) == 1 and prior is not None and comparative_field in current_row:
                    historical_currency, historical_multiplier, history_error = _metadata(dataset, prior, historical_rows[0])
                    if not history_error and historical_currency == currency and prior.scope == p.scope:
                        try:
                            historical = _number(historical_rows[0].get(_fields(prior, statement)[0]))
                            if historical is not None:
                                historical *= historical_multiplier
                                row["historical_previous"] = _s(historical)
                                row["historical_source_id"] = prior.filing_id
                                if historical != before:
                                    row["restated"] = True
                                    row["reason"] = "후속 공시 비교열과 과거 공시 당기값이 다름: 재작성/버전 확인 필요"
                        except ValueError:
                            pass
                if historical_rows:
                    old_name = _text(historical_rows[0].get("account_nm"))
                    if old_name != row["account_name"]:
                        row["previous_account_name"] = old_name
                        row["name_changed"] = True
    return output


def build_account_history(dataset: Dataset) -> dict:
    rows = compare_raw_accounts(dataset)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    return {"rows": rows,
            "coverage": {"raw_rows": sum(len(p.raw_accounts) for p in dataset.periods),
                         "comparison_rows": len(rows), "statuses": counts,
                         "compared": counts.get("calculated", 0),
                         "restatement_differences": sum(row["restated"] for row in rows),
                         "status": "complete_for_supported_identities" if rows and all(r["status"] == "calculated" for r in rows) else "partial"},
            "limitations": [
                "수집된 전체 계정 행 중 동일한 표준 계정·재무제표·구성원·기간을 확인한 항목만 비교합니다.",
                "비표준·회사 확장 계정, 재분류, 중복, 누락과 중간 현금흐름의 기간 불명 항목은 보류합니다.",
                "재무제표 전체의 의미상 재분류·분개·주석 완전성을 검증했다는 보증이 아닙니다.",
            ]}

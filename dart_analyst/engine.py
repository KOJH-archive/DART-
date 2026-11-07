"""Deterministic, source-preserving accounting analysis.

Missing lines are never balancing plugs.  All monetary inputs are Decimal and
their explicit source units are converted before arithmetic.  This module does
not infer accounting causes from movements in reported numbers.
"""
from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, localcontext
from typing import Callable

from .models import Dataset, Fact, Period


LABELS = {
    "revenue": "매출액", "cost_of_sales": "매출원가",
    "gross_profit": "매출총이익", "operating_profit": "영업이익",
    "net_income": "전체 순이익", "parent_net_income": "지배주주 순이익",
    "comprehensive_income": "총포괄손익",
    "assets": "총자산", "liabilities": "총부채", "equity": "총자본",
    "parent_equity": "지배주주지분", "current_assets": "유동자산",
    "current_liabilities": "유동부채", "cash": "현금및현금성자산",
    "receivables": "순매출채권", "inventory": "재고자산",
    "cfo": "영업현금흐름", "cfi": "투자현금흐름", "cff": "재무현금흐름",
    "fx_effect": "현금 환율효과", "other_cash_effects": "기타 현금 조정",
    "cash_disposal_transfer": "매각예정 분류 현금 대체",
    "cash_disposal_change": "처분집단 현금 순증감",
    "cash_change": "공시 현금 순증감", "cash_change_before_fx": "공시 현금 순증감(환율 기준 검증)",
    "cash_beginning": "기초 현금", "capex_ppe": "유형자산 현금 취득",
    "cash_end": "현금흐름표 기말 현금",
    "capex_intangible": "무형자산 현금 취득", "borrowings": "공시 차입금",
    "lease_liabilities": "리스부채", "interest_expense": "총이자비용",
    "oci": "기타포괄손익", "dividends_paid": "현금 지급 배당",
    "equity_beginning": "기초 자본", "equity_dividends": "자본 인식 배당",
    "equity_other_changes": "기타 자본 변동",
    "equity_owner_transactions": "공시 소유주 거래 합계",
}
BALANCES = {
    "assets", "liabilities", "equity", "parent_equity", "current_assets",
    "current_liabilities", "cash", "receivables", "inventory", "borrowings",
    "lease_liabilities",
}
INCOME = {
    "revenue", "cost_of_sales", "gross_profit", "operating_profit",
    "net_income", "parent_net_income", "interest_expense", "comprehensive_income",
}
CASH_FLOWS = {
    "cfo", "cfi", "cff", "fx_effect", "other_cash_effects", "cash_beginning",
    "capex_ppe", "capex_intangible", "dividends_paid",
    "cash_change", "cash_change_before_fx",
    "cash_end",
    "cash_disposal_transfer", "cash_disposal_change",
}
EQUITY_FLOWS = {"equity_beginning", "equity_dividends", "equity_other_changes", "equity_owner_transactions"}
HUNDRED = Decimal("100")
_FINANCIAL_BASIS_METRICS = {
    "current_ratio", "cfo_to_net_income", "interest_coverage", "net_debt",
    "fcf", "fcf_proxy", "dso", "dio", "cash_accruals",
}


def _s(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return format(value, "f")


def _year_before(value: str) -> str:
    d = date.fromisoformat(value)
    try:
        return d.replace(year=d.year - 1).isoformat()
    except ValueError:  # 29 February
        return d.replace(year=d.year - 1, day=28).isoformat()


def _decimal(value: object) -> Decimal:
    result = value if isinstance(value, Decimal) else Decimal(str(value))
    if not result.is_finite():
        raise ValueError("유한한 값이 아닙니다")
    return result


def profit_transition(comparison: dict | None) -> str | None:
    """Name a sign change only for a comparable profit account."""
    if not comparison or comparison.get("status") != "calculated":
        return None
    if comparison.get("key") not in ("operating_profit", "net_income", "parent_net_income"):
        return None
    try:
        previous = _decimal(comparison.get("previous"))
        current = _decimal(comparison.get("current"))
    except (InvalidOperation, ValueError):
        return None
    if previous > 0 > current:
        return "적자 전환"
    if previous < 0 < current:
        return "흑자 전환"
    return None


class _Unavailable(Exception):
    def __init__(self, status: str, reason: str):
        self.status = status
        self.reason = reason
        super().__init__(reason)


class _Engine:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset
        self.metrics: list[dict] = []
        self.checks: list[dict] = []
        self.comparisons: list[dict] = []
        self.observations: list[dict] = []

    def _validate(
        self, fact: Fact | None, key: str, period: Period,
        *, start: str | None = None, end: str | None = None,
        opening: bool = False,
    ) -> Fact:
        if fact is None or fact.amount is None:
            reason = fact.reason if fact is not None and fact.reason else "원천 계정 미확보"
            raise _Unavailable("missing_source", f"{LABELS.get(key, key)}: {reason}")
        if fact.key != key:
            raise _Unavailable("mapping_pending", f"계정 매핑 불일치: {key}/{fact.key}")
        if period.scope != self.dataset.scope or fact.scope != period.scope:
            raise _Unavailable("not_comparable", f"{key}: 연결/별도 범위 불일치")
        if not fact.currency:
            raise _Unavailable("not_comparable", f"{key}: 통화 미확인")
        try:
            amount, unit = _decimal(fact.amount), _decimal(fact.unit)
            if unit <= 0:
                raise ValueError("잘못된 단위")
            date.fromisoformat(fact.start)
            date.fromisoformat(fact.end)
        except (InvalidOperation, ValueError, TypeError):
            raise _Unavailable("not_comparable", f"{key}: 금액·단위·기간 메타데이터 오류")
        del amount
        expected_start, expected_end = start or period.start, end or period.end
        if key == "equity_beginning" and fact.statement == "BS" and start is None and end is None:
            expected_end = (date.fromisoformat(period.start) - timedelta(days=1)).isoformat()
            opening = True
        if key in BALANCES or (opening and fact.statement == "BS"):
            if fact.start != expected_end or fact.end != expected_end:
                raise _Unavailable("not_comparable", f"{key}: 재무상태표 시점 불일치")
            if fact.statement != "BS":
                raise _Unavailable("not_comparable", f"{key}: BS 계정이 아님")
        else:
            if fact.start != expected_start or fact.end != expected_end:
                raise _Unavailable("not_comparable", f"{key}: 흐름 기간 불일치")
            if fact.period_kind != period.kind:
                raise _Unavailable("not_comparable", f"{key}: FY/YTD/단독 분기 불일치")
            allowed = (
                {"IS", "CIS"} if key in INCOME else
                {"CF"} if key in CASH_FLOWS else
                {"SCE", "CE"} if key in EQUITY_FLOWS else
                {"IS", "CIS", "SCE", "CE"} if key == "oci" else set()
            )
            if fact.statement not in allowed:
                raise _Unavailable("not_comparable", f"{key}: 재무제표 종류 불일치")
        attribution = "parent" if key in {"parent_net_income", "parent_equity"} else "total"
        if fact.attribution != attribution:
            raise _Unavailable("not_comparable", f"{key}: 전체/지배주주 귀속 불일치")
        return fact

    def _current(self, period: Period, key: str) -> Fact:
        return self._validate(period.facts.get(key), key, period)

    @staticmethod
    def _amount(fact: Fact) -> Decimal:
        return _decimal(fact.amount) * _decimal(fact.unit)

    @staticmethod
    def _rounding_unit(fact: Fact) -> Decimal:
        raw = fact.source_details.get("rounding_unit", fact.unit)
        try:
            unit = _decimal(raw)
            if unit < 0 or unit > Decimal("1e20"):
                raise ValueError
        except (ValueError, InvalidOperation):
            raise _Unavailable("not_comparable", "원천 반올림 정밀도 미확인") from None
        return unit

    @staticmethod
    def _compatible(facts: list[Fact]) -> None:
        if len({f.currency for f in facts}) > 1:
            raise _Unavailable("not_comparable", "입력 통화가 다릅니다")
        identities = []
        for f in facts:
            # Empty account IDs cannot establish that two different lines are
            # the same source account.  Do not guess from a shared filing ID.
            if f.account_id:
                identities.append((f.source_id, f.account_id, f.statement,
                                   f.start, f.end, f.scope, f.attribution))
        if len(identities) != len(set(identities)):
            raise _Unavailable("mapping_pending", "여러 입력이 동일 원천 계정을 중복 사용합니다")

    @staticmethod
    def _sources(facts: list[Fact]) -> list[str]:
        return list(dict.fromkeys(f.source_id for f in facts if f.source_id))

    def _inputs(self, period: Period, keys: list[str]) -> list[Fact]:
        result = [self._current(period, key) for key in keys]
        self._compatible(result)
        return result

    def _check_metric_industry(self, key: str) -> None:
        if self.dataset.has_financial_industry_code and key in _FINANCIAL_BASIS_METRICS:
            raise _Unavailable("not_applicable", "금융·보험 업종 분류에서는 이 일반기업용 지표의 해석 기준이 다릅니다.")

    def _metric(
        self, period: Period, key: str, label: str, keys: list[str],
        fn: Callable[[list[Decimal]], Decimal], formula: str, unit: str = "%",
        *, positive: tuple[int, ...] = (), facts: list[Fact] | None = None,
        force_status: str | None = None,
    ) -> None:
        row = {"key": key, "label": label, "period": period.label, "value": None,
               "unit": unit, "status": "missing_source", "formula": formula,
               "input_keys": keys, "source_ids": [], "reason": ""}
        try:
            self._check_metric_industry(key)
            fs = facts if facts is not None else self._inputs(period, keys)
            self._compatible(fs)
            row["source_ids"] = self._sources(fs)
            vals = [self._amount(f) for f in fs]
            if any(vals[index] <= 0 for index in positive):
                raise _Unavailable("invalid_denominator", "비율 분모가 0 또는 음수입니다")
            result = fn(vals)
            if not result.is_finite():
                raise _Unavailable("invalid_denominator", "비율 결과가 유한하지 않습니다")
            row["value"] = _s(result)
            row["status"] = force_status or "calculated"
            if unit == "currency":
                row["unit"] = fs[0].currency
        except _Unavailable as exc:
            row["status"], row["reason"] = exc.status, exc.reason
        except (InvalidOperation, ZeroDivisionError):
            row["status"], row["reason"] = "invalid_denominator", "계산 가능한 분모가 아닙니다"
        self.metrics.append(row)

    def _opening(self, period: Period, key: str) -> Fact:
        """Select a comparable beginning balance, never a stale restatement.

        A current filing's comparative at the exact opening instant wins.  A
        previous-year interim comparative is useful for YoY, but is NOT the
        opening balance of the current YTD period.
        """
        expected = (date.fromisoformat(period.start) - timedelta(days=1)).isoformat()
        comp = period.comparatives.get(key)
        if comp is not None and comp.end == expected:
            return self._validate(comp, key, period, end=expected)
        candidates: list[Fact] = []
        for prior in self.dataset.periods:
            if prior is period or prior.end != expected or key not in prior.facts:
                continue
            candidate = self._validate(prior.facts[key], key, prior)
            if prior.scope != period.scope:
                raise _Unavailable("not_comparable", "기초잔액의 연결범위 불일치")
            candidates.append(candidate)
        if not candidates:
            raise _Unavailable("missing_source", f"{key}: 비교 가능한 기초잔액 미확보")
        self._compatible(candidates[:1])
        signatures = {(self._amount(f), f.currency, f.scope, f.attribution) for f in candidates}
        if len(signatures) != 1:
            raise _Unavailable("not_comparable", f"{key}: 과거 기초잔액 후보가 서로 다릅니다")
        return candidates[0]

    def _average_metric(
        self, period: Period, key: str, label: str,
        flow_key: str, balance_key: str, *, days: bool = False,
    ) -> None:
        keys = [flow_key, f"opening:{balance_key}", balance_key]
        formula = (
            f"평균 {LABELS[balance_key]} / {LABELS[flow_key]} × 기간 일수"
            if days else f"{LABELS[flow_key]} / 평균 {LABELS[balance_key]} × 100"
        )
        try:
            self._check_metric_industry(key)
            if not days and period.kind != "FY":
                raise _Unavailable("not_applicable", "중간 ROE·ROA는 연율화하지 않고 보류합니다")
            flow = self._current(period, flow_key)
            closing = self._current(period, balance_key)
            opening = self._opening(period, balance_key)
            fs = [flow, opening, closing]
            self._compatible(fs)
            avg = (self._amount(opening) + self._amount(closing)) / Decimal(2)
            denominator = self._amount(flow) if days else avg
            if denominator <= 0:
                raise _Unavailable("invalid_denominator", "평균잔액 또는 기간 매출/원가가 0 이하입니다")
            if days and avg < 0:
                raise _Unavailable("not_applicable", "평균 채권·재고 잔액이 음수여서 회전일수 해석을 보류합니다")
            count = Decimal((date.fromisoformat(period.end) - date.fromisoformat(period.start)).days + 1)
            fn = (lambda v: ((v[1] + v[2]) / 2) / v[0] * count) if days else (
                lambda v: v[0] / ((v[1] + v[2]) / 2) * HUNDRED
            )
            self._metric(period, key, label, keys, fn, formula, "일" if days else "%", facts=fs)
        except _Unavailable as exc:
            self.metrics.append({"key": key, "label": label, "period": period.label,
                "value": None, "unit": "일" if days else "%", "status": exc.status,
                "formula": formula, "input_keys": keys, "source_ids": [], "reason": exc.reason})

    def _check(
        self, period: Period, key: str, label: str, keys: list[str],
        left_fn: Callable[[list[Decimal]], Decimal], right_fn: Callable[[list[Decimal]], Decimal],
    ) -> None:
        row = {"key": key, "label": label, "period": period.label, "status": "incomplete",
               "left": None, "right": None, "difference": None, "tolerance": None,
               "reason": "", "input_keys": keys}
        try:
            fs = self._inputs(period, keys)
            values = [self._amount(f) for f in fs]
            # A reported rounded line can differ by up to half its display unit.
            tolerance = sum((self._rounding_unit(f) / 2 for f in fs), Decimal(0))
            left, right = left_fn(values), right_fn(values)
            difference = left - right
            row.update(left=_s(left), right=_s(right), difference=_s(difference),
                       tolerance=_s(tolerance), status="pass" if abs(difference) <= tolerance else "fail")
            row["reason"] = "원천 표시 단위 반올림 허용오차 적용"
            if row["status"] == "fail":
                self.observations.append({"text": f"{label} 연결이 일치하지 않습니다. 원천 범위·누락 항목을 확인하세요.",
                    "severity": "warning", "evidence_keys": keys, "period": period.label, "source_ids": self._sources(fs)})
        except _Unavailable as exc:
            row["status"] = "not_comparable" if exc.status == "not_comparable" else "incomplete"
            row["reason"] = exc.reason
        self.checks.append(row)

    def _cash_components_from_reported_total(self, period: Period) -> None:
        original = self.checks[-1]
        proof_key = next((key for key in ("cash_change_before_fx", "cash_change")
                          if key in period.facts and period.facts[key].amount is not None), None)
        if proof_key is None:
            return
        proof_keys = ["cfo", "cfi", "cff", "fx_effect", proof_key]
        try:
            facts = self._inputs(period, proof_keys)
            values = [self._amount(fact) for fact in facts]
            before_difference = sum(values[:3], Decimal(0)) - values[-1]
            after_difference = sum(values[:4], Decimal(0)) - values[-1]
            before_tolerance = sum((self._rounding_unit(fact) / 2 for fact in facts[:3] + facts[4:]), Decimal(0))
            after_tolerance = sum((self._rounding_unit(fact) / 2 for fact in facts), Decimal(0))
            before_matches = abs(before_difference) <= before_tolerance
            after_matches = abs(after_difference) <= after_tolerance
            before_fx = (before_matches and not after_matches) or (
                before_matches and after_matches and proof_key == "cash_change_before_fx")
            difference = before_difference if before_fx else after_difference
            tolerance = before_tolerance if before_fx else after_tolerance
            original["reported_net_change"] = {
                "key": proof_key, "value": _s(values[-1]), "difference": _s(difference),
                "tolerance": _s(tolerance), "source_ids": self._sources(facts),
                "basis": "before_fx" if before_fx else ("after_fx" if after_matches else "unverified"),
                "declared_basis": "before_fx" if proof_key == "cash_change_before_fx" else "after_fx",
                "components_match": abs(difference) <= tolerance,
            }
            if abs(difference) > tolerance:
                original["reason"] += f"; 구성 합계와 공시 순증감 차이 {_s(difference)} · 원문 조정항목 확인"
                return
        except _Unavailable:
            return
        if original["status"] != "incomplete":
            return
        cash_end = "cash_end" if "cash_end" in period.facts and period.facts["cash_end"].amount is not None else "cash"
        adjustments = [key for key in ("cash_disposal_transfer", "cash_disposal_change") if key in period.facts]
        keys = ["cash_beginning", "cfo", "cfi", "cff", "fx_effect", *adjustments, proof_key, cash_end]
        self._check(period, "cash_flow", "현금 구성 합계 = 공시 순증감; 기초 현금 + 구성 합계 + 환율 + 공시 조정 = 기말",
                    keys, lambda v: sum(v[:-2], Decimal(0)), lambda v: v[-1])
        verified = self.checks.pop()
        verified["basis"] = "components_verified_against_reported_total"
        verified["reported_net_change"] = original["reported_net_change"]
        self.checks[-1] = verified

    def _equity_from_reported_totals(self, period: Period) -> None:
        original = self.checks[-1]
        if original["status"] != "incomplete" or "equity_owner_transactions" not in period.facts:
            return
        keys = ["equity_beginning", "comprehensive_income", "equity_owner_transactions", "equity"]
        try:
            facts = self._inputs(period, keys)
            values = [self._amount(fact) for fact in facts]
            difference = sum(values[:3], Decimal(0)) - values[3]
            tolerance = sum((self._rounding_unit(fact) / 2 for fact in facts), Decimal(0))
            if abs(difference) > tolerance:
                original["reason"] += f"; 공시 총액 구성 대조 차이 {_s(difference)} · 추가 자본변동 확인"
                return
        except _Unavailable:
            return
        self._check(period, "equity_bridge", "기초 자본 + 공시 총포괄손익 + 소유주 거래 합계 = 기말 자본",
                    keys, lambda v: sum(v[:3], Decimal(0)), lambda v: v[3])
        verified = self.checks.pop()
        verified["basis"] = "reported_equity_totals"
        self.checks[-1] = verified

    def _checks(self, p: Period) -> None:
        cash_end = "cash_end" if "cash_end" in p.facts and p.facts["cash_end"].amount is not None else "cash"
        adjustments = [key for key in ("cash_disposal_transfer", "cash_disposal_change") if key in p.facts]
        self._check(p, "balance_sheet", "자산 = 부채 + 자본", ["assets", "liabilities", "equity"],
                    lambda v: v[0], lambda v: v[1] + v[2])
        self._check(p, "gross_profit", "매출 − 원가 = 총이익", ["revenue", "cost_of_sales", "gross_profit"],
                    lambda v: v[0] - v[1], lambda v: v[2])
        self._check(p, "cash_flow", "기초 현금 + 현금흐름 = 기말 현금",
                    ["cash_beginning", "cfo", "cfi", "cff", "fx_effect", "other_cash_effects", *adjustments, cash_end],
                    lambda v: sum(v[:-1], Decimal(0)), lambda v: v[-1])
        self._cash_components_from_reported_total(p)
        cash_proof = self.checks[-1].get("reported_net_change", {})
        # equity_dividends is the SCE recognition amount, NOT CF dividends_paid.
        self._check(p, "equity_bridge", "기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본",
                    ["equity_beginning", "net_income", "oci", "equity_dividends", "equity_other_changes", "equity"],
                    lambda v: v[0] + v[1] + v[2] - abs(v[3]) + v[4], lambda v: v[5])
        self._equity_from_reported_totals(p)
        reported_key = cash_proof.get("key") if cash_proof.get("components_match") else None
        if reported_key and cash_proof.get("basis") == "after_fx":
            self._check(p, "cash_reported_total", "기초 현금 + 공시 순증감 + 공시 조정 = 기말 현금",
                        ["cash_beginning", reported_key, *adjustments, cash_end],
                        lambda v: sum(v[:-1], Decimal(0)), lambda v: v[-1])
        elif reported_key:
            self._check(p, "cash_reported_total", "기초 현금 + 공시 순증감 + 환율효과 + 공시 조정 = 기말 현금",
                        ["cash_beginning", reported_key, "fx_effect", *adjustments, cash_end],
                        lambda v: sum(v[:-1], Decimal(0)), lambda v: v[-1])
        elif "cash_change" in p.facts or "cash_change_before_fx" in p.facts:
            self.checks.append({
                "key": "cash_reported_total", "label": "공시 현금 순증감의 환율 포함 범위 확인",
                "period": p.label, "status": "not_comparable",
                "left": None, "right": None, "difference": None, "tolerance": None,
                "reason": "영업·투자·재무와 환율효과를 대조해 공시 순증감의 표시 범위를 확인해야 합니다.",
                "input_keys": ["cash_beginning", cash_proof.get("key", "cash_change"), "fx_effect", cash_end],
            })
        if "comprehensive_income" in p.facts:
            self._check(p, "comprehensive_income", "순이익 + 기타포괄손익 = 총포괄손익",
                        ["net_income", "oci", "comprehensive_income"],
                        lambda v: v[0] + v[1], lambda v: v[2])

    def _metrics(self, p: Period) -> None:
        try:
            current = self._current(p, "revenue")
            previous, _ = self._previous(p, "revenue")
            self._metric(p, "revenue_growth", "전년 동기 매출 성장률", ["revenue", "previous:revenue"],
                         lambda v: (v[0] / v[1] - 1) * HUNDRED,
                         "(당기 매출 / 전년 동일 기간 매출 − 1) × 100", facts=[current, previous], positive=(1,))
        except _Unavailable as exc:
            self.metrics.append({"key": "revenue_growth", "label": "전년 동기 매출 성장률", "period": p.label,
                "value": None, "unit": "%", "status": exc.status,
                "formula": "(당기 매출 / 전년 동일 기간 매출 − 1) × 100",
                "input_keys": ["revenue", "previous:revenue"], "source_ids": [], "reason": exc.reason})
        for key, label, numerator in (
            ("gross_margin", "매출총이익률", "gross_profit"),
            ("operating_margin", "영업이익률", "operating_profit"),
            ("net_margin", "전체 순이익률", "net_income"),
        ):
            self._metric(p, key, label, [numerator, "revenue"], lambda v: v[0] / v[1] * HUNDRED,
                         f"{LABELS[numerator]} / 매출 × 100", positive=(1,))
        for key, label, numerator, denominator, percentage in (
            ("current_ratio", "유동비율", "current_assets", "current_liabilities", True),
            ("debt_ratio", "부채비율", "liabilities", "equity", True),
            ("cfo_to_net_income", "순이익 현금 전환", "cfo", "net_income", False),
            ("interest_coverage", "이자보상배율", "operating_profit", "interest_expense", False),
        ):
            multiplier = HUNDRED if percentage else Decimal(1)
            self._metric(p, key, label, [numerator, denominator],
                         lambda v, m=multiplier: v[0] / v[1] * m,
                         f"{LABELS[numerator]} / {LABELS[denominator]}" + (" × 100" if percentage else ""),
                         "%" if percentage else "배", positive=(1,))
        self._metric(p, "net_debt", "공시 차입금 − 현금 (리스 포함 여부 확인 필요)", ["borrowings", "cash"],
                     lambda v: v[0] - v[1], "공시 차입금 − 현금및현금성자산; 리스 포함 여부는 원천 정의 확인", "currency")
        capex_keys = ["capex_ppe", "capex_intangible"]
        self._metric(p, "cash_capex", "현금 CAPEX", capex_keys,
                     lambda v: abs(v[0]) + abs(v[1]), "유형·무형자산 현금 취득액 합계", "currency")
        self._metric(p, "fcf", "현금 취득액 차감 FCF", ["cfo"] + capex_keys,
                     lambda v: v[0] - abs(v[1]) - abs(v[2]), "CFO − 유형 현금 취득 − 무형 현금 취득", "currency")
        available = [k for k in capex_keys if k in p.facts and p.facts[k].amount is not None]
        if len(available) == 1:
            self._metric(p, "fcf_proxy", "확보한 일부 CAPEX만 차감한 FCF 참고값", ["cfo"] + available,
                         lambda v: v[0] - abs(v[1]), "CFO − 확보된 일부 현금 취득액 (완전 FCF 아님)",
                         "currency", force_status="partial")
        parent = p.scope == "CFS"
        self._average_metric(p, "roe", "지배주주 ROE" if parent else "별도 ROE",
                             "parent_net_income" if parent else "net_income", "parent_equity" if parent else "equity")
        self._average_metric(p, "roa", "ROA", "net_income", "assets")
        self._average_metric(p, "dso", "DSO (총매출 근사치)", "revenue", "receivables", days=True)
        self._average_metric(p, "dio", "DIO", "cost_of_sales", "inventory", days=True)
        try:
            self._check_metric_industry("cash_accruals")
            fs = [self._current(p, "net_income"), self._current(p, "cfo"), self._opening(p, "assets"), self._current(p, "assets")]
            self._compatible(fs)
            if (self._amount(fs[2]) + self._amount(fs[3])) / 2 <= 0:
                raise _Unavailable("invalid_denominator", "평균 총자산이 0 이하입니다")
            self._metric(p, "cash_accruals", "현금흐름식 발생액 지표", ["net_income", "cfo", "opening:assets", "assets"],
                         lambda v: (v[0] - v[1]) / ((v[2] + v[3]) / 2) * HUNDRED,
                         "(전체 순이익 − CFO) / 평균 총자산 × 100", facts=fs)
        except _Unavailable as exc:
            self.metrics.append({"key": "cash_accruals", "label": "현금흐름식 발생액 지표", "period": p.label,
                "value": None, "unit": "%", "status": exc.status,
                "formula": "(전체 순이익 − CFO) / 평균 총자산 × 100",
                "input_keys": ["net_income", "cfo", "opening:assets", "assets"], "source_ids": [], "reason": exc.reason})

    def _previous(self, p: Period, key: str) -> tuple[Fact, str]:
        start, end = _year_before(p.start), _year_before(p.end)
        if key in p.comparatives:
            fact = self._validate(p.comparatives[key], key, p, start=start, end=end)
            return fact, f"{start}~{end} (현재 공시 비교값)"
        candidates = [prior for prior in self.dataset.periods if prior is not p
                      and prior.start == start and prior.end == end and prior.kind == p.kind]
        if not candidates:
            raise _Unavailable("missing_source", "전년 동일 기간 비교값 미확보")
        values = []
        for prior in candidates:
            if key not in prior.facts:
                continue
            fact = self._current(prior, key)
            if prior.scope != p.scope:
                raise _Unavailable("not_comparable", "전기 연결범위 불일치")
            values.append((fact, prior.label))
        if not values:
            raise _Unavailable("missing_source", "전기 계정 미확보")
        if len({(self._amount(f), f.currency, f.scope, f.attribution) for f, _ in values}) != 1:
            raise _Unavailable("not_comparable", "전기 숫자 후보의 값·기준이 다릅니다")
        return values[0]

    def _comparisons(self, p: Period) -> None:
        for key in LABELS:
            row = {"key": key, "label": LABELS[key], "from_period": None, "to_period": p.label,
                   "previous": None, "current": None, "delta": None, "pct": None,
                   "status": "missing_source", "reason": "", "source_ids": []}
            try:
                current = self._current(p, key)
                previous, from_label = self._previous(p, key)
                self._compatible([current, previous])
                before, after = self._amount(previous), self._amount(current)
                delta = after - before
                row.update(from_period=from_label, previous=_s(before), current=_s(after), delta=_s(delta),
                           pct=_s(delta / before * HUNDRED) if before > 0 else None,
                           status="calculated", source_ids=self._sources([previous, current]))
                if before <= 0:
                    row["reason"] = "비교기≤0: 증감률 대신 금액 차이로 표시"
                # Report a revision explicitly.  Never silently substitute the
                # earlier filing's amount for the selected comparative.
                if key in p.comparatives:
                    old = [prior.facts[key] for prior in self.dataset.periods
                           if prior is not p and prior.start == _year_before(p.start)
                           and prior.end == _year_before(p.end) and prior.kind == p.kind and key in prior.facts]
                    for historical in old:
                        try:
                            self._validate(historical, key, p, start=_year_before(p.start), end=_year_before(p.end))
                            if historical.currency != previous.currency:
                                continue
                            if self._amount(historical) != before:
                                row["reason"] = (row["reason"] + "; " if row["reason"] else "") + "재작성/공시 버전 차이: 현재 공시 비교값 사용"
                                row["historical_previous"] = _s(self._amount(historical))
                                row["historical_source_ids"] = self._sources([historical])
                                break
                        except _Unavailable:
                            continue
            except _Unavailable as exc:
                row["status"], row["reason"] = exc.status, exc.reason
            self.comparisons.append(row)

    def run(self) -> dict:
        for p in sorted(self.dataset.periods, key=lambda item: (item.end, item.start, item.label)):
            try:
                if date.fromisoformat(p.start) > date.fromisoformat(p.end):
                    raise ValueError("기간 역전")
            except ValueError:
                self.observations.append({"text": "분석 기간 메타데이터가 잘못되어 해당 기간을 건너뛰었습니다.",
                    "severity": "warning", "evidence_keys": [], "period": p.label})
                continue
            self._metrics(p)
            self._checks(p)
            self._comparisons(p)
            for text in p.issues:
                self.observations.append({"text": text, "severity": "warning", "evidence_keys": [], "period": p.label})
            try:
                self._check_metric_industry("cfo_to_net_income")
                cfo, ni = self._inputs(p, ["cfo", "net_income"])
                if self._amount(ni) > 0 and self._amount(cfo) < 0:
                    self.observations.append({"text": "순이익은 양수이나 영업현금흐름은 음수입니다. 운전자본·세금·비현금손익의 공시 근거를 확인하세요.",
                        "severity": "attention", "evidence_keys": ["net_income", "cfo"], "period": p.label,
                        "source_ids": self._sources([ni, cfo])})
            except _Unavailable:
                pass
        statuses: dict[str, int] = {}
        for row in self.metrics:
            statuses[row["status"]] = statuses.get(row["status"], 0) + 1
        check_statuses = {status: sum(c["status"] == status for c in self.checks)
                          for status in ("pass", "fail", "incomplete", "not_comparable")}
        complete = bool(self.dataset.periods) and not any(c["status"] != "pass" for c in self.checks)
        complete = complete and all(m["status"] in {"calculated", "not_applicable"} for m in self.metrics)
        return {"metrics": self.metrics, "checks": self.checks, "comparisons": self.comparisons,
                "observations": self.observations,
                "coverage": {"periods": len(self.dataset.periods), "metric_statuses": statuses,
                             "check_statuses": check_statuses,
                             "status": "complete" if complete else "partial",
                             "issues": list(self.dataset.issues),
                             "note": "공시 원천 계정·주석 전체를 빠짐없이 검증했다는 보증이 아닙니다."}}


def analyze(dataset: Dataset) -> dict:
    """Return JSON-serializable accounting metrics and explicit reconciliation gaps."""
    with localcontext() as ctx:
        ctx.prec = 34
        result = _Engine(dataset).run()
        from .account_history import build_account_history
        result['account_history'] = build_account_history(dataset)
        return result

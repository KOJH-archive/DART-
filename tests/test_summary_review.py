from decimal import Decimal

from dart_analyst.demo import build_demo
from dart_analyst.engine import analyze
from dart_analyst.narrative import build_summary


def test_cash_income_review_groups_only_affected_periods_and_preserves_sources():
    data = build_demo()
    for period in data.periods:
        if period.label in {"2022", "2024"}:
            new_cash_flow = Decimal("-100000000")
            period.facts["cff"].amount += period.facts["cfo"].amount - new_cash_flow
            period.facts["cfo"].amount = new_cash_flow
    lines = build_summary(data, analyze(data))
    warnings = [line for line in lines if "순이익은 양수이나 영업현금흐름은 음수" in line]
    assert len(warnings) == 1
    assert warnings[0].startswith("2022 연간, 2024 연간:")
    assert "[근거: DEMO-2022-FY, DEMO-2024-FY · net_income, cfo]" in warnings[0]


def test_revenue_growth_warns_once_while_profit_change_is_still_highlighted():
    data = build_demo()
    interim = next(period for period in data.periods if period.kind == "YTD")
    interim.facts["revenue"].amount = Decimal("274188080000")
    interim.facts["operating_profit"].amount = Decimal("20000000000")
    lines = build_summary(data, analyze(data))
    anomaly = next(line for line in lines if line.startswith("이상치 검토 필요"))
    large_changes = next(line for line in lines if line.startswith("급격한 변동 검토 필요"))
    assert f"{interim.label} 전년 동기 매출 성장률 372.74 %" in anomaly
    assert "매출액 증감률" not in large_changes
    assert "영업이익 증감률" in large_changes

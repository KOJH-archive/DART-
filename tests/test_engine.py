from copy import deepcopy
from decimal import Decimal
import json

import pytest

from dart_analyst.engine import analyze, profit_transition
from dart_analyst.models import Dataset, Fact, Period


BALANCES = {"assets", "liabilities", "equity", "parent_equity", "current_assets",
            "current_liabilities", "cash", "receivables", "inventory", "borrowings", "lease_liabilities"}
INCOME = {"revenue", "cost_of_sales", "gross_profit", "operating_profit", "net_income",
          "parent_net_income", "interest_expense"}


@pytest.mark.parametrize("adjustment, expected", [(0, "pass"), (5, "incomplete")])
def test_cash_components_require_independent_reported_net_change(adjustment, expected):
    values = {"cash_beginning": 100, "cfo": 30, "cfi": -20, "cff": 10,
              "fx_effect": 1, "cash": 121, "cash_change_before_fx": 20 + adjustment}
    period = Period("2024", 2024, "2024-01-01", "2024-12-31",
                    facts={key: fact(key, value) for key, value in values.items()})
    dataset = Dataset("검증", periods=[period])
    result = analyze(dataset)
    check = next(row for row in result["checks"] if row["key"] == "cash_flow")
    assert check["status"] == expected
    assert "other_cash_effects" not in period.facts
    if adjustment == 0:
        assert check["reported_net_change"]["difference"] == "0"
        assert check["basis"] == "components_verified_against_reported_total"


def test_cash_net_change_uses_verified_presentation_to_avoid_double_counting_fx():
    values = {"cash_beginning": 100, "cfo": 30, "cfi": -20, "cff": 10,
              "fx_effect": 10, "cash": 130, "cash_change_before_fx": 30}
    period = Period("2024", 2024, "2024-01-01", "2024-12-31",
                    facts={key: fact(key, value) for key, value in values.items()})
    checks = {r["key"]: r for r in analyze(Dataset("검증", periods=[period]))["checks"]}
    assert checks["cash_flow"]["status"] == "pass"
    assert checks["cash_flow"]["reported_net_change"]["basis"] == "after_fx"
    assert checks["cash_flow"]["reported_net_change"]["declared_basis"] == "before_fx"
    assert checks["cash_reported_total"]["status"] == "pass"


@pytest.mark.parametrize("transfer, expected", [(-10, "pass"), (-20, "fail"), (None, "incomplete")])
def test_cash_rollforward_uses_reported_disposal_adjustment_without_a_plug(transfer, expected):
    values = {"cash_beginning": 100, "cfo": 30, "cfi": -20, "cff": 10,
              "fx_effect": 10, "cash": 120, "cash_change_before_fx": 20,
              "cash_disposal_transfer": transfer}
    p = Period("2024", 2024, "2024-01-01", "2024-12-31",
               facts={key: fact(key, value) for key, value in values.items()})
    checks = {r["key"]: r for r in analyze(Dataset("검증", periods=[p]))["checks"]}
    assert checks["cash_flow"]["status"] == expected
    assert checks["cash_reported_total"]["status"] == expected
    assert p.facts["cash_disposal_transfer"].amount == (Decimal(transfer) if transfer is not None else None)


@pytest.mark.parametrize("owner, expected", [(-5, "pass"), (-10, "incomplete")])
def test_equity_aggregate_requires_independent_owner_transaction_total(owner, expected):
    p = period()
    del p.facts["equity_other_changes"]
    p.facts["equity_beginning"].amount = Decimal(100)
    p.facts["equity"].amount = Decimal(115)
    for key, value, statement in (("comprehensive_income", 20, "CIS"),
                                  ("equity_owner_transactions", owner, "SCE")):
        p.facts[key] = fact(key, value)
        p.facts[key].statement = statement
    row = check(analyze(dataset(p)), "equity_bridge")
    assert row["status"] == expected
    assert "equity_other_changes" not in p.facts
    if expected == "pass":
        assert row["basis"] == "reported_equity_totals"
        assert "equity_owner_transactions" in row["input_keys"]


def fact(key, value, year=2024, *, kind="FY", end=None, scope="CFS", currency="KRW", unit="1"):
    end = end or f"{year}-12-31"
    start = end if key in BALANCES else f"{year}-01-01"
    statement = "BS" if key in BALANCES else "IS" if key in INCOME else (
        "SCE" if key in {"equity_beginning", "equity_dividends", "equity_other_changes", "oci"} else "CF")
    return Fact(key=key, name=key, amount=Decimal(str(value)) if value is not None else None,
                statement=statement, start=start, end=end, scope=scope, currency=currency,
                unit=Decimal(unit), source_id=f"F-{year}-{kind}", account_id=f"account:{key}",
                attribution="parent" if key in {"parent_net_income", "parent_equity"} else "total",
                period_kind=kind)


@pytest.mark.parametrize(("key", "status", "previous", "current", "expected"), [
    ("operating_profit", "calculated", "8668.32", "-944.53", "적자 전환"),
    ("net_income", "calculated", "-30", "20", "흑자 전환"),
    ("parent_net_income", "calculated", "10", "0", None),
    ("cfo", "calculated", "10", "-10", None),
    ("operating_profit", "not_comparable", "10", "-10", None),
])
def test_profit_transition_requires_comparable_profit_crossing_zero(key, status, previous, current, expected):
    assert profit_transition({
        "key": key, "status": status, "previous": previous, "current": current,
    }) == expected


def period(year=2024, *, kind="FY", end=None, scope="CFS", values=None):
    end = end or f"{year}-12-31"
    values = values or {
        "revenue": 1000, "cost_of_sales": 600, "gross_profit": 400,
        "operating_profit": 150, "net_income": 100, "parent_net_income": 90,
        "assets": 1200, "liabilities": 500, "equity": 700, "parent_equity": 600,
        "current_assets": 500, "current_liabilities": 250, "cash": 100,
        "receivables": 120, "inventory": 80, "borrowings": 300, "lease_liabilities": 50,
        "cfo": 100, "cfi": -40, "cff": -10, "fx_effect": 0,
        "other_cash_effects": 0, "cash_beginning": 50,
        "capex_ppe": 30, "capex_intangible": 5, "interest_expense": 10,
        "oci": 20, "dividends_paid": 18, "equity_beginning": 600,
        "equity_dividends": 20, "equity_other_changes": 0,
    }
    return Period(label=f"{year}-{kind}", year=year, start=f"{year}-01-01", end=end,
                  scope=scope, kind=kind, filing_id=f"F-{year}-{kind}",
                  facts={k: fact(k, v, year, kind=kind, end=end, scope=scope) for k, v in values.items()})


def dataset(*periods):
    return Dataset(company="가상 기업", scope=periods[0].scope if periods else "CFS", periods=list(periods))


def metric(result, key, label="2024-FY"):
    return next(row for row in result["metrics"] if row["key"] == key and row["period"] == label)


def check(result, key, label="2024-FY"):
    return next(row for row in result["checks"] if row["key"] == key and row["period"] == label)


def comparison(result, key, label="2024-FY"):
    return next(row for row in result["comparisons"] if row["key"] == key and row["to_period"] == label)


def test_decimal_metrics_and_complete_reconciliations_are_json_serializable():
    p = period()
    result = analyze(dataset(p))
    assert metric(result, "gross_margin")["value"] == "40.0"
    assert metric(result, "fcf")["value"] == "65"
    assert metric(result, "net_debt")["value"] == "200"
    assert metric(result, "current_ratio")["value"] == "200"
    assert all(check(result, k)["status"] == "pass"
               for k in ("balance_sheet", "gross_profit", "cash_flow", "equity_bridge"))
    json.dumps(result, ensure_ascii=False, allow_nan=False)


@pytest.mark.parametrize("key", ["revenue", "equity", "net_income", "interest_expense"])
def test_zero_denominators_are_not_infinity_or_exception(key):
    p = period()
    p.facts[key].amount = Decimal(0)
    target = {"revenue": "operating_margin", "equity": "debt_ratio",
              "net_income": "cfo_to_net_income", "interest_expense": "interest_coverage"}[key]
    row = metric(analyze(dataset(p)), target)
    assert row["status"] == "invalid_denominator"
    assert row["value"] is None


def test_negative_equity_is_not_a_positive_solvency_ratio():
    p = period()
    p.facts["equity"].amount = Decimal(-10)
    assert metric(analyze(dataset(p)), "debt_ratio")["status"] == "invalid_denominator"


def test_consolidated_cash_flow_cannot_use_separate_profit():
    p = period()
    p.facts["net_income"].scope = "OFS"
    row = metric(analyze(dataset(p)), "cfo_to_net_income")
    assert row["status"] == "not_comparable"
    assert row["value"] is None


@pytest.mark.parametrize("mutation", ["dates", "kind", "currency", "unit", "attribution"])
def test_invalid_metadata_prevents_cross_statement_calculation(mutation):
    p = period()
    target = p.facts["cfo"]
    if mutation == "dates":
        target.end = "2024-09-30"
    elif mutation == "kind":
        target.period_kind = "YTD"
    elif mutation == "currency":
        target.currency = "USD"
    elif mutation == "unit":
        target.unit = Decimal(0)
    else:
        target.attribution = "parent"
    row = metric(analyze(dataset(p)), "cfo_to_net_income")
    assert row["status"] == "not_comparable"


def test_explicit_different_display_units_are_converted_before_comparison():
    p = period()
    p.facts["cfo"].amount = Decimal("0.1")
    p.facts["cfo"].unit = Decimal("1000")
    assert metric(analyze(dataset(p)), "cfo_to_net_income")["value"] == "1.0"


def test_restatement_comparative_wins_over_old_history_for_growth_and_average():
    old, current = period(2023), period(2024)
    old.facts["revenue"].amount = Decimal(800)
    old.facts["parent_equity"].amount = Decimal(500)
    current.comparatives["revenue"] = fact("revenue", 900, 2023)
    current.comparatives["parent_equity"] = fact("parent_equity", 400, 2023)
    current.comparatives["assets"] = fact("assets", 1000, 2023)
    result = analyze(dataset(old, current))
    assert comparison(result, "revenue")["previous"] == "900"
    assert comparison(result, "revenue")["historical_previous"] == "800"
    assert "재작성" in comparison(result, "revenue")["reason"]
    assert metric(result, "roe")["value"] == "18.00"  # 90 / average(400, 600)
    assert Decimal(metric(result, "roa")["value"]).quantize(Decimal(".0001")) == Decimal("9.0909")


def test_bad_selected_comparative_cannot_fall_back_to_stale_history():
    old, current = period(2023), period(2024)
    current.comparatives["revenue"] = fact("revenue", 900, 2023, scope="OFS")
    current.comparatives["parent_equity"] = fact("parent_equity", 400, 2023, scope="OFS")
    result = analyze(dataset(old, current))
    assert comparison(result, "revenue")["status"] == "not_comparable"
    assert metric(result, "revenue_growth")["value"] is None
    assert metric(result, "roe")["status"] == "not_comparable"


def test_ytd_dso_uses_year_opening_not_last_year_interim_and_actual_days():
    closing = period(2023)
    closing.facts["receivables"].amount = Decimal(100)
    p = period(2024, kind="YTD", end="2024-06-30")
    p.comparatives["receivables"] = fact("receivables", 60, 2023, kind="YTD", end="2023-06-30")
    result = analyze(dataset(closing, p))
    assert Decimal(metric(result, "dso", p.label)["value"]) == Decimal("20.02")  # avg110 /1000 *182
    assert metric(result, "roe", p.label)["status"] == "not_applicable"


def test_ytd_cannot_compare_to_full_year_or_standalone_quarter():
    p = period(2024, kind="YTD", end="2024-09-30")
    p.comparatives["revenue"] = fact("revenue", 900, 2023, kind="Q3", end="2023-09-30")
    assert comparison(analyze(dataset(p)), "revenue", p.label)["status"] == "not_comparable"


def test_unknown_fx_is_incomplete_not_zero_and_never_used_as_a_plug():
    p = period()
    del p.facts["fx_effect"]
    result = analyze(dataset(p))
    row = check(result, "cash_flow")
    assert row["status"] == "incomplete"
    assert row["difference"] is None
    assert result["coverage"]["status"] == "partial"


def test_cash_mismatch_is_a_failure_not_balanced_by_invented_adjustment():
    p = period()
    p.facts["cash"].amount += Decimal(5)
    row = check(analyze(dataset(p)), "cash_flow")
    assert row["status"] == "fail"
    assert row["difference"] == "-5"


def test_cash_dividends_cannot_substitute_for_equity_recognition():
    p = period()
    del p.facts["equity_dividends"]
    assert check(analyze(dataset(p)), "equity_bridge")["status"] == "incomplete"
    p.facts["equity_dividends"] = deepcopy(p.facts["dividends_paid"])
    p.facts["equity_dividends"].key = "equity_dividends"
    assert check(analyze(dataset(p)), "equity_bridge")["status"] == "not_comparable"


def test_capex_none_and_partial_never_masquerade_as_complete_fcf():
    p = period()
    del p.facts["capex_intangible"]
    result = analyze(dataset(p))
    assert metric(result, "fcf")["value"] is None
    assert metric(result, "fcf_proxy")["status"] == "partial"
    assert metric(result, "fcf_proxy")["value"] == "70"
    del p.facts["capex_ppe"]
    result = analyze(dataset(p))
    assert metric(result, "fcf")["value"] is None
    assert not any(m["key"] == "fcf_proxy" for m in result["metrics"])


def test_signed_capex_is_normalized_as_outflow():
    p = period()
    p.facts["capex_ppe"].amount *= -1
    assert metric(analyze(dataset(p)), "fcf")["value"] == "65"


def test_duplicate_source_account_does_not_double_count_capex():
    p = period()
    p.facts["capex_intangible"].account_id = p.facts["capex_ppe"].account_id
    row = metric(analyze(dataset(p)), "cash_capex")
    assert row["status"] == "mapping_pending"
    assert row["value"] is None


def test_first_year_average_balance_is_not_replaced_with_ending_balance():
    result = analyze(dataset(period()))
    for key in ("roe", "roa", "dso", "dio", "cash_accruals"):
        assert metric(result, key)["status"] == "missing_source"


def test_separate_basis_roe_uses_entity_profit_and_entity_equity():
    old, current = period(2023, scope="OFS"), period(2024, scope="OFS")
    old.facts["equity"].amount = Decimal(500)
    del current.facts["parent_equity"]
    del current.facts["parent_net_income"]
    row = metric(analyze(dataset(old, current)), "roe")
    assert Decimal(row["value"]).quantize(Decimal(".0001")) == Decimal("16.6667")
    assert "parent_net_income" not in row["input_keys"]


def test_parent_and_total_attribution_cannot_mix():
    old, current = period(2023), period(2024)
    current.facts["parent_net_income"].attribution = "total"
    assert metric(analyze(dataset(old, current)), "roe")["status"] == "not_comparable"


def test_negative_prior_profit_retains_delta_without_misleading_pct():
    old, current = period(2023), period(2024)
    old.facts["net_income"].amount = Decimal(-20)
    row = comparison(analyze(dataset(old, current)), "net_income")
    assert row["delta"] == "120"
    assert row["pct"] is None


def test_reconciliation_does_not_turn_missing_other_equity_changes_into_zero():
    p = period()
    del p.facts["equity_other_changes"]
    assert check(analyze(dataset(p)), "equity_bridge")["status"] == "incomplete"


def test_equity_beginning_can_be_a_verified_bs_opening_instant():
    p = period()
    p.facts["equity_beginning"].statement = "BS"
    p.facts["equity_beginning"].start = "2023-12-31"
    p.facts["equity_beginning"].end = "2023-12-31"
    assert check(analyze(dataset(p)), "equity_bridge")["status"] == "pass"


def test_empty_dataset_is_partial_and_json_serializable():
    result = analyze(dataset())
    assert result["coverage"]["status"] == "partial"
    assert result["metrics"] == []
    json.dumps(result, allow_nan=False)

from copy import deepcopy
import json

import pytest

from dart_analyst.account_history import build_account_history, compare_raw_accounts
from dart_analyst.models import Dataset, Period


def period(year, rows, *, kind="FY", end=None, scope="CFS"):
    return Period(label=str(year) if kind == "FY" else f"{year} H1", year=year,
                  start=f"{year}-01-01", end=end or f"{year}-12-31", kind=kind, scope=scope,
                  filing_id=f"F-{year}-{kind}", raw_accounts=rows)


def raw(value, *, previous=None, account_id="ifrs-full_Revenue", statement="IS", detail="", **fields):
    row = {"account_id": account_id, "account_nm": "검증 계정", "sj_div": statement,
           "account_detail": detail, "currency": "KRW", "thstrm_amount": str(value)}
    if previous is not None:
        row["frmtrm_amount"] = str(previous)
    row.update(fields)
    return row


def data(*periods):
    return Dataset(company="검증 회사", scope="CFS", source_mode="dart", periods=list(periods))


def row_for(result, label, concept="ifrs-full_Revenue", detail=""):
    return next(row for row in result if row["to_period"] == label and row["account_id"] == concept
                and row["account_detail"] == detail)


def test_full_unmapped_standard_account_has_history_without_canonical_fact():
    concept = "ifrs-full_ResearchAndDevelopmentExpense"
    result = build_account_history(data(period(2023, [raw(100, account_id=concept)]),
                                        period(2024, [raw(150, account_id=concept)])))
    row = row_for(result["rows"], "2024", concept)
    assert row["status"] == "calculated"
    assert row["previous"] == "100"
    assert row["current"] == "150"
    assert row["delta"] == "50"
    assert row["pct"] == "50.0"
    assert row["source_ids"] == ["F-2024-FY", "F-2023-FY"]
    json.dumps(result, allow_nan=False)


def test_current_comparative_wins_and_revision_is_exposed():
    ds = data(period(2023, [raw(100)]), period(2024, [raw(150, previous=120)]))
    row = row_for(compare_raw_accounts(ds), "2024")
    assert row["previous"] == "120"
    assert row["historical_previous"] == "100"
    assert row["restated"] is True
    assert row["delta"] == "30"


@pytest.mark.parametrize("blank", ["", "-", "—"])
def test_explicit_missing_comparative_never_falls_back_to_old_filing(blank):
    ds = data(period(2023, [raw(100)]), period(2024, [raw(150, frmtrm_amount=blank)]))
    row = row_for(compare_raw_accounts(ds), "2024")
    assert row["status"] == "missing_previous"
    assert row["previous"] is None


def test_company_custom_ids_and_placeholder_are_not_guessed_by_name():
    for concept in ("entity_CustomRevenue", "-표준계정코드미사용-", ""):
        rows = compare_raw_accounts(data(period(2023, [raw(100, account_id=concept)]),
                                        period(2024, [raw(150, account_id=concept)])))
        assert row_for(rows, "2024", concept)["status"] == "mapping_pending"


def test_duplicate_context_is_not_aggregated_even_with_equal_values():
    source = raw(100, previous=90)
    rows = compare_raw_accounts(data(period(2024, [source, deepcopy(source)])))
    assert rows[0]["status"] == "duplicate"
    assert rows[0]["current"] is None


def test_statement_and_member_identity_prevents_wrong_cross_reference():
    old = period(2023, [raw(100, statement="SCE", detail="자본 [member]")])
    new = period(2024, [raw(120, statement="SCE", detail="지배주주 [member]")])
    rows = compare_raw_accounts(data(old, new))
    assert row_for(rows, "2024", detail="지배주주 [member]")["status"] == "context_changed"
    assert row_for(rows, "2024", detail="자본 [member]")["status"] == "context_changed"
    assert all(r["delta"] is None for r in rows)


def test_row_order_is_not_part_of_account_identity():
    a, b = "ifrs-full_Revenue", "ifrs-full_CostOfSales"
    ds = data(period(2023, [raw(100, account_id=a, ord="1"), raw(70, account_id=b, ord="2")]),
              period(2024, [raw(75, account_id=b, ord="1"), raw(150, account_id=a, ord="99")]))
    assert row_for(compare_raw_accounts(ds), "2024", a)["delta"] == "50"


def test_disappearing_account_is_missing_not_zero():
    ds = data(period(2023, [raw(100)]), period(2024, []))
    row = row_for(compare_raw_accounts(ds), "2024")
    assert row["status"] == "missing_current"
    assert row["current"] is None
    assert row["delta"] is None


@pytest.mark.parametrize("fields", [{"currency": "USD"}, {"fs_div": "OFS"},
                                      {"bsns_year": "2022"}, {"reprt_code": "11012"},
                                      {"rcept_no": "wrong"}, {"unit": "백만원"}])
def test_invalid_scope_currency_period_unit_or_source_blocks_comparison(fields):
    ds = data(period(2023, [raw(100)]), period(2024, [raw(120, **fields)]))
    assert row_for(compare_raw_accounts(ds), "2024")["status"] == "not_comparable"


def test_ytd_income_uses_add_amount_not_three_month_amount():
    source = raw(20, previous=10, thstrm_add_amount="110", frmtrm_add_amount="100")
    p = period(2024, [source], kind="YTD", end="2024-06-30")
    row = row_for(compare_raw_accounts(data(p)), p.label)
    assert row["current"] == "110"
    assert row["previous"] == "100"
    assert row["delta"] == "10"
    assert row["current_field"] == "thstrm_add_amount"


def test_interim_cf_and_sce_are_not_assumed_to_be_ytd():
    for statement in ("CF", "SCE"):
        p = period(2024, [raw(20, previous=10, statement=statement, detail="자본 [member]")],
                   kind="YTD", end="2024-06-30")
        row = row_for(compare_raw_accounts(data(p)), p.label, detail="자본 [member]")
        assert row["status"] == "not_comparable"
        assert row["delta"] is None


def test_interim_bs_comparative_is_previous_year_end_not_prior_half_year():
    source = raw(120, previous=100, account_id="ifrs-full_Assets", statement="BS")
    p = period(2024, [source], kind="YTD", end="2024-06-30")
    row = row_for(compare_raw_accounts(data(p)), p.label, "ifrs-full_Assets")
    assert row["from_period"] == "2023-12-31"
    assert "전기말" in row["comparison_basis"]


def test_raw_missing_currency_cannot_be_inferred_from_name_or_other_accounts():
    source = raw(120, previous=100, currency="")
    assert compare_raw_accounts(data(period(2024, [source])))[0]["status"] == "not_comparable"


def test_zero_previous_shows_movement_without_percent():
    row = compare_raw_accounts(data(period(2024, [raw(120, previous=0)])))[0]
    assert row["status"] == "calculated"
    assert row["delta"] == "120"
    assert row["pct"] is None


def test_exact_standard_id_can_preserve_name_change_without_fuzzy_matching():
    ds = data(period(2023, [raw(100, account_nm="옛 이름")]),
              period(2024, [raw(120, account_nm="새 이름")]))
    row = row_for(compare_raw_accounts(ds), "2024")
    assert row["status"] == "calculated"
    assert row["name_changed"] is True
    assert row["previous_account_name"] == "옛 이름"


def test_explicit_multiplier_conversion_preserves_decimal_precision():
    ds = data(period(2023, [raw("0.1", unit="1000")]), period(2024, [raw("100.01")]))
    row = row_for(compare_raw_accounts(ds), "2024")
    assert row["previous"] == "100.0"
    assert row["delta"] == "0.01"

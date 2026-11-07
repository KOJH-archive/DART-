from datetime import date
from decimal import Decimal
from io import BytesIO
from zipfile import ZipFile

import httpx
import pytest

from dart_analyst.dart_client import DartClient, DartError, parse_amount
from dart_analyst.engine import analyze
from dart_analyst.models import dataset_from_json, dataset_to_json


KEY = "test-key-never-log"
CORP = "00123456"
ANNUAL = "20250318000001"
CORRECTED = "20250618000002"
INTERIM = "20261105000003"


def zipped(content: str, filename: str = "CORPCODE.xml") -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w") as archive:
        archive.writestr(filename, content)
    return buffer.getvalue()


def row(account_id, name, amount="100", *, statement="BS", prior="80", receipt=ANNUAL, **extra):
    return {"account_id": account_id, "account_nm": name, "thstrm_amount": amount,
            "frmtrm_amount": prior, "rcept_no": receipt, "sj_div": statement,
            "currency": "KRW", **extra}


def filing(name="사업보고서 (2024.12)", receipt=ANNUAL, received="20250318", **extra):
    return {"report_nm": name, "rcept_no": receipt, "rcept_dt": received, "rm": "", **extra}


def fixture_client(*, rows=None, filings=None, overview=None, endpoint_payload=None):
    calls = []
    rows = rows if rows is not None else [row("ifrs-full_Assets", "자산총계")]
    filings = filings if filings is not None else [filing()]
    overview = overview if overview is not None else {"status": "000", "acc_mt": "12", "induty_code": "264"}

    def handler(request):
        endpoint = request.url.path.rsplit("/", 1)[-1]
        calls.append((endpoint, dict(request.url.params)))
        assert request.url.params["crtfc_key"] == KEY
        if endpoint_payload and endpoint in endpoint_payload:
            payload = endpoint_payload[endpoint]
            return httpx.Response(200, content=payload) if isinstance(payload, bytes) else httpx.Response(200, json=payload)
        if endpoint == "company.json":
            return httpx.Response(200, json=overview)
        if endpoint == "list.json":
            return httpx.Response(200, json={"status": "000", "total_page": 1, "list": filings})
        if endpoint == "fnlttSinglAcntAll.json":
            return httpx.Response(200, json={"status": "000", "list": rows})
        if endpoint == "document.xml":
            return httpx.Response(200, content=zipped("<DOCUMENT><TITLE>회계정책</TITLE><P>연결 기준 재무제표입니다.</P></DOCUMENT>", "document.xml"))
        if endpoint == "fnlttXbrl.xml":
            return httpx.Response(200, content=b"<result><status>014</status></result>")
        raise AssertionError(f"Unexpected mocked endpoint: {endpoint}")

    return DartClient(KEY, transport=httpx.MockTransport(handler), today=date(2026, 11, 6)), calls


def test_company_search_uses_zip_index_and_caches_without_losing_leading_zero():
    content = """<result><list><corp_code>00123456</corp_code><corp_name>테스트회사</corp_name><stock_code>001234</stock_code></list>
    <list><corp_code>00123457</corp_code><corp_name>테스트회사홀딩스</corp_name><stock_code> </stock_code></list></result>"""
    client, calls = fixture_client(endpoint_payload={"corpCode.xml": zipped(content)})
    assert client.search_companies("테스트회사")[0] == {"corp_code": CORP, "corp_name": "테스트회사", "stock_code": "001234"}
    assert client.search_companies("001234")[0]["corp_code"] == CORP
    assert len(calls) == 1


@pytest.mark.parametrize("payload", [b"not a zip", zipped("<result/>", "../escape.xml"), zipped('<!DOCTYPE result [<!ENTITY x "bad">]><result>&x;</result>')])
def test_company_index_rejects_malformed_paths_and_entities(payload):
    client, _ = fixture_client(endpoint_payload={"corpCode.xml": payload})
    with pytest.raises(DartError):
        client.search_companies("회사")


def test_missing_api_key_fails_before_creating_any_request():
    with pytest.raises(DartError, match="인증키"):
        DartClient(" ")


@pytest.mark.parametrize("payload, expected", [({"status": "010", "message": KEY}, "등록되지"), (b"<result><status>020</status></result>", "한도")])
def test_authentication_and_xml_limit_errors_are_sanitized(payload, expected):
    endpoint = "corpCode.xml" if isinstance(payload, bytes) else "company.json"
    client, _ = fixture_client(endpoint_payload={endpoint: payload})
    with pytest.raises(DartError) as caught:
        client.search_companies("회사") if isinstance(payload, bytes) else client.load_company(CORP, "회사")
    assert expected in str(caught.value)
    assert KEY not in str(caught.value)


def test_api_no_data_is_not_zero_or_fake_demo_data():
    client, _ = fixture_client(endpoint_payload={"fnlttSinglAcntAll.json": {"status": "013", "message": "조회된 데이터 없음"}})
    dataset = client.load_company(CORP, "회사", years=1)
    assert dataset.source_mode == "live"
    assert dataset.periods == []
    assert any("재무제표가 없습니다" in issue for issue in dataset.issues)


def test_latest_available_annual_is_selected_and_correction_is_verified():
    client, calls = fixture_client(filings=[filing(), filing("[기재정정]사업보고서 (2024.12)", CORRECTED, "20250618")], rows=[row("ifrs-full_Assets", "자산총계", "9007199254740993", receipt=CORRECTED)])
    dataset = client.load_company(CORP, "회사", years=1, include_interim=False)
    period = dataset.periods[0]
    assert period.year == 2024  # not today's year or an invented 2025 report
    assert period.filing_id == CORRECTED
    assert period.facts["assets"].amount == Decimal("9007199254740993")
    assert period.facts["assets"].source_url.endswith(CORRECTED)
    assert period.comparatives["assets"].end == "2023-12-31"
    assert next(params for endpoint, params in calls if endpoint == "list.json")["last_reprt_at"] == "Y"


def test_receipt_mismatch_withholds_the_whole_period():
    client, _ = fixture_client(filings=[filing(receipt=CORRECTED)], rows=[row("ifrs-full_Assets", "자산총계", receipt=ANNUAL)])
    dataset = client.load_company(CORP, "회사", years=1)
    assert not dataset.periods
    assert any("접수번호가 달라" in issue for issue in dataset.issues)


def test_final_filing_xbrl_recovers_mismatched_annual_without_old_api_rows():
    with ZipFile(BytesIO(interim_archive())) as archive:
        xml = archive.read("nested/instance.xbrl").decode()
    xml = xml.replace("2025", "2023").replace("2026", "2024").replace("06-30", "12-31")
    client, _ = fixture_client(
        filings=[filing(receipt=CORRECTED)],
        rows=[row("ifrs-full_Assets", "자산총계", "999", receipt=ANNUAL)],
        endpoint_payload={"fnlttXbrl.xml": zipped(xml, "final.xbrl")},
    )
    dataset = client.load_company(CORP, "회사", years=1)
    period, = dataset.periods
    assert period.filing_id == CORRECTED
    assert period.raw_accounts == []
    assert "assets" not in period.facts
    assert period.facts["net_income"].amount == 5472888000000
    assert period.facts["net_income"].source_id == CORRECTED
    assert period.comparatives["net_income"].end == "2023-12-31"
    assert any("공시 XBRL에서 확인된 계정만 복구" in issue for issue in period.issues)


@pytest.mark.parametrize("prior, statement, expected", [("80", "CIS", True), ("81", "CIS", False), ("80", "IS", False)])
def test_income_mirrors_require_distinct_statements_and_identical_comparative(prior, statement, expected):
    rows = [row("ifrs-full_ProfitLoss", "순이익", "100", prior="80", statement="IS"),
            row("ifrs-full_ProfitLoss", "순이익", "100", prior=prior, statement=statement)]
    period = DartClient._normalize(rows, 2024, 12, "CFS", ANNUAL)
    assert ("net_income" in period.facts) == expected
    assert len(period.raw_accounts) == 2
    if expected:
        assert len(period.facts["net_income"].source_details["mirrored_rows"]) == 2


def test_scope_mismatch_is_not_combined_or_silently_fallback():
    client, calls = fixture_client(rows=[row("ifrs-full_Assets", "자산총계", fs_div="OFS")])
    dataset = client.load_company(CORP, "회사", years=1, scope="CFS")
    assert not dataset.periods
    assert [params["fs_div"] for endpoint, params in calls if endpoint == "fnlttSinglAcntAll.json"] == ["CFS"]


def test_ambiguous_candidates_are_not_picked_and_raw_rows_remain():
    rows = [row("ifrs-full_Revenue", "매출액", statement="IS"), row("custom_Revenue", "매출액", "120", statement="IS")]
    client, _ = fixture_client(rows=rows)
    period = client.load_company(CORP, "회사", years=1).periods[0]
    assert "revenue" not in period.facts
    assert len(period.raw_accounts) == 2
    assert any("후보가 여러 개" in issue for issue in period.issues)


def test_total_and_parent_income_equity_are_distinct():
    rows = [row("ifrs-full_ProfitLoss", "당기순이익", "100", statement="IS"),
            row("ifrs-full_ProfitLossAttributableToOwnersOfParent", "지배주주순이익", "80", statement="IS"),
            row("ifrs-full_Equity", "자본총계", "500"),
            row("ifrs-full_EquityAttributableToOwnersOfParent", "지배주주지분", "400")]
    client, _ = fixture_client(rows=rows)
    facts = client.load_company(CORP, "회사", years=1).periods[0].facts
    assert facts["net_income"].amount == 100
    assert facts["parent_net_income"].amount == 80
    assert facts["equity"].amount == 500
    assert facts["parent_equity"].amount == 400
    assert facts["parent_equity"].attribution == "parent"


def test_interim_income_uses_ytd_not_single_quarter_and_cf_is_withheld():
    interim_rows = [row("ifrs-full_Revenue", "매출액", "30", statement="IS", receipt=INTERIM, thstrm_add_amount="90", frmtrm_add_amount="75"),
                    row("ifrs-full_CashFlowsFromUsedInOperatingActivities", "영업활동현금흐름", "44", statement="CF", receipt=INTERIM),
                    row("ifrs-full_Assets", "자산총계", "500", receipt=INTERIM)]

    def handler(request):
        endpoint = request.url.path.rsplit("/", 1)[-1]
        payload = {
            "company.json": {"status": "000", "acc_mt": "12", "induty_code": "264"},
            "list.json": {"status": "000", "list": [filing("분기보고서 (2026.09)", INTERIM, "20261105")], "total_page": 1},
            "fnlttSinglAcntAll.json": {"status": "000", "list": interim_rows},
        }
        if endpoint == "document.xml":
            return httpx.Response(200, content=zipped("<DOCUMENT><P>원문</P></DOCUMENT>"))
        if endpoint == "fnlttXbrl.xml":
            return httpx.Response(200, content=b"<result><status>014</status></result>")
        return httpx.Response(200, json=payload[endpoint])

    with DartClient(KEY, transport=httpx.MockTransport(handler), today=date(2026, 11, 6)) as client:
        period = client.load_company(CORP, "회사", years=1).periods[0]
    assert period.kind == "YTD"
    assert period.facts["revenue"].amount == 90
    assert period.facts["revenue"].source_field == "thstrm_add_amount"
    assert period.comparatives["revenue"].amount == 75
    assert period.comparatives["revenue"].end == "2025-09-30"
    assert period.comparatives["assets"].end == "2025-12-31"
    assert "cfo" not in period.facts
    assert any("원본 XBRL 검증 보류" in issue for issue in period.issues)


def interim_archive(extra_fact="", *, include_previous_cfo=True):
    namespace = "https://xbrl.ifrs.org/taxonomy/2024-03-27/ifrs-full"

    def context(key, year=2026, start="01-01", corp=CORP, member="ConsolidatedMember", extra="",
                scheme="http://dart.fss.or.kr/ifrs/CIK"):
        return f"""<context id="{key}">
          <entity><identifier scheme="{scheme}">{corp}</identifier></entity>
          <period><startDate>{year}-{start}</startDate><endDate>{year}-06-30</endDate></period>
          <scenario><d:explicitMember dimension="f:ConsolidatedAndSeparateFinancialStatementsAxis">f:{member}</d:explicitMember>{extra}</scenario>
        </context>"""

    def cash_flow(key, amount, unit="won"):
        return f'<f:CashFlowsFromUsedInOperatingActivities contextRef="{key}" unitRef="{unit}" decimals="-6">{amount}</f:CashFlowsFromUsedInOperatingActivities>'

    return zipped(f"""<xbrl xmlns="http://www.xbrl.org/2003/instance"
        xmlns:d="http://xbrl.org/2006/xbrldi" xmlns:f="{namespace}"
        xmlns:iso="http://www.xbrl.org/2003/iso4217"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dart="http://dart.fss.or.kr/taxonomy/2026-01-31/ifrs/dart">
        {context("current")}
        {context("previous", year=2025)}
        {context("quarter", start="04-01")}
        {context("separate", member="SeparateMember")}
        {context("other-company", corp="00999999")}
        {context("other-scheme", scheme="urn:untrusted")}
        {context("qualified", extra='<d:explicitMember dimension="f:BusinessAxis">f:SegmentMember</d:explicitMember>')}
        <unit id="won"><measure>iso:KRW</measure></unit>
        <unit id="dollar"><measure>iso:USD</measure></unit>
        {cash_flow("current", 4849653000000)}
        {cash_flow("current", 4849653000000)}
        {cash_flow("previous", 959651000000) if include_previous_cfo else ""}
        {cash_flow("quarter", 1)}
        {cash_flow("separate", 2)}
        {cash_flow("other-company", 3)}
        {cash_flow("qualified", 4)}
        {cash_flow("current", 5, unit="dollar")}
        {cash_flow("other-scheme", 6)}
        <f:CashFlowsFromUsedInOperatingActivities contextRef="current" unitRef="won" xsi:nil="true"/>
        <f:ProfitLoss contextRef="current" unitRef="won" decimals="-6">5472888000000</f:ProfitLoss>
        <f:ProfitLoss contextRef="previous" unitRef="won" decimals="-6">6632564000000</f:ProfitLoss>
        {extra_fact}
      </xbrl>""", "nested/instance.xbrl")


def load_interim_archive(payload, *, income="5472888000000", document=None, extra_rows=()):
    rows = [
        row("ifrs-full_ProfitLoss", "반기순이익", "2887962000000", statement=statement, receipt=INTERIM,
            thstrm_add_amount=income, frmtrm_add_amount="6632564000000")
        for statement in ("IS", "CIS")
    ]
    rows.append(row("ifrs-full_CashFlowsFromUsedInInvestingActivities", "투자활동현금흐름", statement="CF", receipt=INTERIM))
    rows.extend(extra_rows)
    responses = {"fnlttXbrl.xml": payload}
    if document is not None:
        responses["document.xml"] = document
    client, calls = fixture_client(rows=rows, filings=[filing("반기보고서 (2026.06)", INTERIM, "20260814")],
                                   endpoint_payload=responses)
    with client:
        dataset = client.load_company(CORP, "회사", years=1)
    return dataset, calls


def test_interim_archive_integrates_verified_accounts_with_provenance():
    dataset, calls = load_interim_archive(interim_archive(), document=zipped("<DOCUMENT>", "document.xml"))
    period, = dataset.periods
    assert [(p["rcept_no"], p["reprt_code"]) for endpoint, p in calls if endpoint == "fnlttXbrl.xml"] == [(INTERIM, "11012")]
    assert {k: f.amount for k, f in period.facts.items()} == {"cfo": 4849653000000, "net_income": 5472888000000}
    assert {k: f.amount for k, f in period.comparatives.items()} == {"cfo": 959651000000, "net_income": 6632564000000}
    assert any(issue.startswith("cfi: ") for issue in period.issues)
    assert not any(issue.startswith("net_income: ") for issue in period.issues)
    assert all(note["status"] == "추출 실패" for note in dataset.notes)
    assert any("원문 주석 추출 보류" in issue for issue in dataset.issues)
    cfo = dataset_from_json(dataset_to_json(dataset)).periods[0].facts["cfo"]
    assert cfo.unit == 1
    assert cfo.source_id == INTERIM
    assert cfo.source_details["member"] == "nested/instance.xbrl"
    assert cfo.source_details["report_code"] == "11012"
    assert {item["decimals"] for item in cfo.source_details["candidates"]} == {"-6"}
    assert all(check["status"] != "pass" for check in analyze(dataset)["checks"])


def test_interim_archive_holds_conflicting_values_and_missing_current_filing_comparison():
    conflict = '<f:CashFlowsFromUsedInOperatingActivities contextRef="current" unitRef="won">1</f:CashFlowsFromUsedInOperatingActivities>'
    dataset, _ = load_interim_archive(interim_archive(conflict, include_previous_cfo=False), income="7")
    period, = dataset.periods
    assert period.facts["cfo"].amount is None
    assert "원본 XBRL 금액이 서로 다름" in period.facts["cfo"].reason
    assert period.comparatives["cfo"].amount is None
    assert "비교값 미확보" in period.comparatives["cfo"].reason
    assert period.facts["net_income"].amount is None
    assert period.facts["net_income"].source_details["all_account_api_amounts"] == ["7"]
    assert period.comparatives["net_income"].amount == 6632564000000


def test_xbrl_disclosed_rounding_verifies_more_precise_api_value():
    dataset, _ = load_interim_archive(interim_archive(), income="5472888000001")
    fact = dataset.periods[0].facts["net_income"]
    assert fact.amount == 5472888000001
    assert fact.source_field == "xbrl_verified_api"
    assert fact.source_details["candidates"][0]["amount"] == "5472888000000"
    assert fact.source_details["rounding_unit"] == "1"


def test_explicit_debt_components_are_verified_against_their_own_xbrl_concepts():
    current, noncurrent = 2182080664669, 8744563527885
    extra = f"""<context id="point">
      <entity><identifier scheme="http://dart.fss.or.kr/ifrs/CIK">{CORP}</identifier></entity>
      <period><instant>2026-06-30</instant></period>
      <scenario><d:explicitMember dimension="f:ConsolidatedAndSeparateFinancialStatementsAxis">f:ConsolidatedMember</d:explicitMember></scenario>
      </context>
      <f:CurrentLeaseLiabilities contextRef="point" unitRef="won" decimals="0">{current}</f:CurrentLeaseLiabilities>
      <f:NoncurrentLeaseLiabilities contextRef="point" unitRef="won" decimals="0">{noncurrent}</f:NoncurrentLeaseLiabilities>
      <f:LeaseLiabilities contextRef="point" unitRef="won" decimals="-6">10926645000000</f:LeaseLiabilities>"""
    rows = [row("ifrs-full_CurrentLeaseLiabilities", "리스부채", str(current), receipt=INTERIM),
            row("ifrs-full_NoncurrentLeaseLiabilities", "리스부채", str(noncurrent), receipt=INTERIM)]
    dataset, _ = load_interim_archive(interim_archive(extra), extra_rows=rows)
    fact = dataset.periods[0].facts["lease_liabilities"]
    assert fact.amount == current + noncurrent
    assert fact.source_field == "xbrl_verified_api"
    assert fact.source_details["aggregation"] == "sum_explicit_components"
    assert len(fact.source_details["candidates"]) == 2
    assert fact.source_details["unselected_total_values"] == ["10926645000000"]


def test_interim_xbrl_verifies_cash_flow_and_opening_cash_with_separate_contexts():
    extra = """<context id="point">
        <entity><identifier scheme="http://dart.fss.or.kr/ifrs/CIK">00123456</identifier></entity>
        <period><instant>2026-06-30</instant></period>
        <scenario><d:explicitMember dimension="f:ConsolidatedAndSeparateFinancialStatementsAxis">f:ConsolidatedMember</d:explicitMember></scenario>
      </context>
      <dart:CashAndCashEquivalentsAtBeginningOfPeriodCf contextRef="point" unitRef="won">400</dart:CashAndCashEquivalentsAtBeginningOfPeriodCf>
      <dart:CashAndCashEquivalentsAtBeginningOfPeriodCf contextRef="current" unitRef="won">999</dart:CashAndCashEquivalentsAtBeginningOfPeriodCf>
      <f:CashFlowsFromUsedInInvestingActivities contextRef="current" unitRef="won">100</f:CashFlowsFromUsedInInvestingActivities>
      <f:CashFlowsFromUsedInInvestingActivities contextRef="quarter" unitRef="won">999</f:CashFlowsFromUsedInInvestingActivities>
      <f:DividendsPaidClassifiedAsFinancingActivities contextRef="current" unitRef="won">-12</f:DividendsPaidClassifiedAsFinancingActivities>
      <f:DividendsPaid contextRef="current" unitRef="won">100</f:DividendsPaid>"""
    rows = [
        row("dart_CashAndCashEquivalentsAtBeginningOfPeriodCf", "기초 현금", "400", statement="CF", receipt=INTERIM),
        row("ifrs-full_DividendsPaidClassifiedAsFinancingActivities", "배당금", "12", statement="CF", receipt=INTERIM),
    ]
    dataset, _ = load_interim_archive(interim_archive(extra), extra_rows=rows)
    period, = dataset.periods
    assert {key: period.facts[key].amount for key in ("cash_beginning", "cfi", "dividends_paid")} == {
        "cash_beginning": 400, "cfi": 100, "dividends_paid": 12,
    }
    assert period.facts["cash_beginning"].source_details["candidates"][0]["instant"] == "2026-06-30"
    assert period.comparatives["cash_beginning"].amount is None
    assert next(check for check in analyze(dataset)["checks"] if check["key"] == "cash_flow")["status"] == "incomplete"


def test_invalid_xbrl_preserves_verified_mirrored_income_from_all_account_api():
    invalid = '<f:ProfitLoss contextRef="current" unitRef="won">NaN</f:ProfitLoss>'
    dataset, _ = load_interim_archive(interim_archive(invalid))
    period, = dataset.periods
    assert period.facts["net_income"].amount == 5472888000000
    assert "cfo" not in period.facts
    assert any("원본 XBRL 검증 보류" in issue for issue in period.issues)


def test_dividends_on_cash_flow_and_equity_statement_are_not_mixed():
    rows = [row("ifrs-full_DividendsPaid", "배당금 지급", "(10)", statement="CF"),
            row("ifrs-full_DividendsPaid", "배당금", "(12)", statement="SCE", account_detail="자본 [member]"),
            row("ifrs-full_DividendsPaid", "배당금", "(11)", statement="SCE", account_detail="자본 [member]|지배기업 소유주지분 - 자본 [member]")]
    client, _ = fixture_client(rows=rows)
    facts = client.load_company(CORP, "회사", years=1).periods[0].facts
    assert facts["dividends_paid"].amount == 10
    assert facts["equity_dividends"].amount == 12
    assert facts["dividends_paid"].statement == "CF"
    assert facts["equity_dividends"].statement == "SCE"


@pytest.mark.parametrize("key, label, statement", [
    ("equity_owner_transactions", "소유주와의 거래 합계", "SCE"),
    ("cash_disposal_transfer", "매각예정자산으로의 대체", "CF"),
    ("cash_disposal_change", "처분집단으로 분류된 현금및현금성자산의 순증감", "CF"),
])
@pytest.mark.parametrize("namespace_corp, approved", [(CORP, True), ("00999999", False)])
def test_extension_mapping_requires_schema_label_and_company_namespace(monkeypatch, key, label, statement, namespace_corp, approved):
    from dataclasses import replace
    from dart_analyst.models import Period
    from dart_analyst.xbrl import XbrlInstance, read_xbrl_archive
    base = read_xbrl_archive(interim_archive())
    concept = f"{{http://dart.fss.or.kr/taxonomy/2026-01-31/entity{namespace_corp}}}Movement"
    source = next(f for f in base.facts if f.context_id == "current")
    extension = replace(source, concept=concept, value=Decimal(-10), decimals="0")
    instance = XbrlInstance("fixture.xbrl", (extension,), {concept: (label,)}, ("schema.xsd", "label_lab-ko.xml"))
    monkeypatch.setattr("dart_analyst.dart_client.read_xbrl_archive", lambda _: instance)
    client, _ = fixture_client(endpoint_payload={"fnlttXbrl.xml": interim_archive()})
    p = Period("2026 반기", 2026, "2026-01-01", "2026-06-30", kind="YTD", filing_id=INTERIM)
    assert client._apply_xbrl(p, CORP, "11012") == approved
    assert (key in p.facts) == approved
    if approved:
        assert p.facts[key].amount == -10
        assert p.facts[key].statement == statement
        assert p.facts[key].account_id == concept
        assert p.facts[key].source_details["concept_labels"][concept] == (label,)


def test_debt_requires_complete_current_and_noncurrent_categories():
    rows = [row("ifrs-full_CurrentBorrowings", "유동차입금", "30")]
    client, _ = fixture_client(rows=rows)
    assert "borrowings" not in client.load_company(CORP, "회사", years=1).periods[0].facts
    rows.append(row("ifrs-full_NoncurrentBorrowings", "비유동차입금", "70"))
    client, _ = fixture_client(rows=rows)
    period = client.load_company(CORP, "회사", years=1).periods[0]
    assert period.facts["borrowings"].amount == 100
    assert "리스 포함 여부 미확인" in period.facts["borrowings"].reason
    assert any("리스 포함 여부 미확인" in issue for issue in period.issues)


def test_debt_total_is_not_rounded_by_default_decimal_context():
    value = "123456789012345678901234567890123456789"
    client, _ = fixture_client(rows=[row("ifrs-full_CurrentBorrowings", "유동차입금", value), row("ifrs-full_NoncurrentBorrowings", "비유동차입금", "1")])
    period = client.load_company(CORP, "회사", years=1).periods[0]
    assert period.facts["borrowings"].amount == Decimal("123456789012345678901234567890123456790")


def test_korean_alias_cannot_override_a_contradictory_standard_account_id():
    client, _ = fixture_client(rows=[row("ifrs-full_CurrentBorrowings", "차입금", "30"), row("ifrs-full_EquityAttributableToOwnersOfParent", "자본총계", "80")])
    period = client.load_company(CORP, "회사", years=1).periods[0]
    assert "borrowings" not in period.facts
    assert "equity" not in period.facts
    assert period.facts["parent_equity"].amount == 80


def test_unsupported_accounting_month_stops_before_financial_calls():
    client, calls = fixture_client(overview={"status": "000", "acc_mt": "03", "induty_code": "264"})
    dataset = client.load_company(CORP, "회사", years=1)
    assert not dataset.periods
    assert len(calls) == 1
    assert dataset.issues


@pytest.mark.parametrize("industry", ["64121", "64992", "65110", "66121"])
def test_financial_industry_allows_collection_comparisons_and_checks(industry):
    overview = {"status": "000", "acc_mt": "12", "induty_code": industry}
    rows = [
        row("ifrs-full_Assets", "자산총계", "100"),
        row("ifrs-full_Liabilities", "부채총계", "60"),
        row("ifrs-full_Equity", "자본총계", "40"),
        row("ifrs-full_CurrentAssets", "유동자산", "30"),
        row("ifrs-full_CurrentLiabilities", "유동부채", "20"),
    ]
    client, calls = fixture_client(rows=rows, overview=overview)
    dataset = client.load_company(CORP, "회사", years=1)
    assert dataset.periods
    assert any(endpoint == "fnlttSinglAcntAll.json" for endpoint, _ in calls)
    analysis = analyze(dataset_from_json(dataset_to_json(dataset)))
    assert next(r for r in analysis["comparisons"] if r["key"] == "assets")["status"] == "calculated"
    assert next(r for r in analysis["checks"] if r["key"] == "balance_sheet")["status"] == "pass"
    metrics = {r["key"]: r for r in analysis["metrics"]}
    assert metrics["current_ratio"]["status"] == "not_applicable"
    assert metrics["current_ratio"]["value"] is None
    assert metrics["debt_ratio"]["status"] == "calculated"


def test_note_failures_do_not_invent_clean_audit_or_risk_absence():
    client, _ = fixture_client(endpoint_payload={"document.xml": b"<result><status>014</status></result>"})
    dataset = client.load_company(CORP, "회사", years=1)
    assert dataset.periods
    assert len(dataset.notes) == 5
    assert all(note["status"] == "추출 실패" and not note["excerpt"] for note in dataset.notes)


@pytest.mark.parametrize("text, amount", [("0", Decimal(0)), ("9,007,199,254,740,993", Decimal("9007199254740993")), ("(1,234)", Decimal(-1234)), ("−12", Decimal(-12)), ("-", None), (None, None)])
def test_amount_exactness_and_missing_values(text, amount):
    assert parse_amount(text) == amount


@pytest.mark.parametrize("text", ["NaN", "Infinity", "1,23", "₩100", "1e3", 1.2, True])
def test_bad_amounts_are_never_rounded_or_filled_with_zero(text):
    with pytest.raises(ValueError):
        parse_amount(text)

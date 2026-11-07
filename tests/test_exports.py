from decimal import Decimal
from io import BytesIO

from openpyxl import load_workbook

from dart_analyst.exporters import make_excel, make_html, make_markdown, safe_source_url
from dart_analyst.models import Dataset, Fact, Period


def sample():
    fact = Fact("revenue", "=HYPERLINK(\"https://bad\")", Decimal("99999999999999999.125"), "IS", "2025-01-01", "2025-12-31", source_id="DEMO-25", source_url="https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20250101000001")
    ds = Dataset(company='<script>alert("x")</script>', periods=[Period("2025", 2025, "2025-01-01", "2025-12-31", facts={"revenue": fact})], notes=[{"topic": "위험", "status": "parse_failed", "excerpt": '<img src=x onerror="alert(1)">', "source_url": "javascript:alert(1)"}])
    result = {"metrics": [{"key": "revenue", "label": "매출", "period": "2025", "value": "99999999999999999.125", "unit": "KRW", "status": "calculated", "source_ids": ["DEMO-25"]}], "checks": [{"label": "현금 대조", "period": "2025", "status": "incomplete", "reason": "환율 자료 없음"}], "comparisons": [], "observations": [], "coverage": {"missing": 1}}
    return ds, result


def test_excel_keeps_precision_and_never_executes_input():
    ds, result = sample()
    wb = load_workbook(BytesIO(make_excel(ds, result)), data_only=False)
    ws = wb["원천 계정·근거"]
    assert ws["D2"].data_type == "s"
    assert ws["D2"].value.startswith("=HYPERLINK")
    assert ws["E2"].value == "99999999999999999.125"
    assert all(c.data_type != "f" for sheet in wb for row in sheet for c in row)
    assert "가상 검증 데이터" in wb["보고서 정보"]["B3"].value


def test_html_escapes_content_and_preserves_trace():
    ds, result = sample()
    output = make_html(ds, result)
    assert '<script>' not in output
    assert '<img src=x' not in output
    assert 'href="javascript:' not in output
    assert 'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=' in output
    assert "환율 자료 없음" in output
    assert "가상 검증 데이터" in output


def test_markdown_reports_unfinished_work_and_source():
    ds, result = sample()
    output = make_markdown(ds, result)
    assert "완료하지 못했습니다" in output
    assert "DEMO-25" in output
    assert "99999999999999999.125" in output
    assert "<script>" not in output


def test_source_links_allow_only_dart_https():
    for bad in ("javascript:alert(1)", "http://dart.fss.or.kr/", "https://dart.fss.or.kr.evil/", "https://evil@dart.fss.or.kr/", "https://dart.fss.or.kr:8000/", "https://dart.fss.or.kr:bad/"):
        assert safe_source_url(bad) is None
    assert safe_source_url("https://opendart.fss.or.kr/guide/main.do")


def test_generated_memo_exports_only_with_the_same_dataset_and_version():
    from dart_analyst.narrative import COMMENTARY_FORMAT_VERSION, commentary_fingerprint
    ds, result = sample()
    result["ai_commentary"] = {
        "format_version": COMMENTARY_FORMAT_VERSION, "dataset_fingerprint": commentary_fingerprint(ds),
        "period": "2025", "model": "local-model",
        "industry_reviews": [{"title": "제출용 업종 검토", "observation": "검증된 비교 관찰",
                              "background": "산업 배경", "question": "추가 확인 질문", "comparisons": []}],
        "claims": [],
    }
    assert "제출용 업종 검토" in make_html(ds, result)
    assert "제출용 업종 검토" in make_markdown(ds, result)
    assert "AI 검토 메모" in load_workbook(BytesIO(make_excel(ds, result))).sheetnames
    ds.company = "다른 회사"
    assert "제출용 업종 검토" not in make_html(ds, result)
    assert "AI 검토 메모" not in load_workbook(BytesIO(make_excel(ds, result))).sheetnames


def test_actual_engine_exports_include_bridge_inputs_limits_and_source_metadata():
    from dart_analyst.demo import build_demo
    from dart_analyst.engine import analyze
    dataset = build_demo("missing")
    analysis = analyze(dataset)
    workbook = load_workbook(BytesIO(make_excel(dataset, analysis)))
    assert "대조 입력 상세" in workbook.sheetnames
    details = list(workbook["대조 입력 상세"].values)
    row = next(row for row in details if row[0] == "2026 H1" and row[3] == "fx_effect")
    assert row[2] == "incomplete"
    assert row[5] == "N/A"
    assert row[10] == "DEMO-2026-YTD"
    assert "누락" in row[12] or "미확보" in row[12]
    for report in (make_html(dataset, analysis), make_markdown(dataset, analysis)):
        assert "자료 범위·처리 현황" in report
        assert "대조 입력 상세" in report
        assert "missing_source" in report
        assert "2026-01-01" in report
        assert "fx_effect" in report
        assert "DEMO-2026-YTD" in report


def raw_history_sample():
    periods = []
    for year, value, comparative in (
        (2024, "99999999999999999.125", None),
        (2025, "100000000000000099.250", "100000000000000000.125"),
    ):
        receipt = f"{year + 1}0301000001"
        row = {
            "sj_div": "IS", "account_id": "ifrs-full_Revenue", "account_nm": '=HYPERLINK("https://bad")<script>x</script>',
            "account_detail": "", "currency": "KRW", "fs_div": "CFS", "bsns_year": str(year),
            "reprt_code": "11011", "rcept_no": receipt, "thstrm_amount": value,
            "source_url": f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={receipt}",
        }
        if comparative is not None:
            row["frmtrm_amount"] = comparative
        periods.append(Period(str(year), year, f"{year}-01-01", f"{year}-12-31", filing_id=receipt, raw_accounts=[row]))
    return Dataset(company="원천 계정 비교", source_mode="live", periods=periods)


def test_full_raw_history_export_preserves_restated_values_context_and_escaping():
    dataset = raw_history_sample()
    result = {"metrics": [], "comparisons": [], "checks": [], "observations": []}
    workbook = load_workbook(BytesIO(make_excel(dataset, result)))
    ws = workbook["원천 전체 계정 비교"]
    headers, *rows = list(ws.values)
    row = next(dict(zip(headers, values)) for values in rows if dict(zip(headers, values))["분석기간"] == "2025")
    assert row["비교금액"] == "100000000000000000.125"
    assert row["당기금액"] == "100000000000000099.250"
    assert row["차이"] == "99.125"
    assert row["기존 공시 비교금액"] == "99999999999999999.125"
    assert row["재작성 차이"] == "True"
    assert row["당기 시작일"] == "2025-01-01"
    assert "당기 공시 비교열 우선" in row["비교 기준"]
    assert row["원문 1"].startswith("https://dart.fss.or.kr/")
    assert all(cell.data_type != "f" for sheet in workbook for line in sheet for cell in line)
    for report in (make_html(dataset, result), make_markdown(dataset, result)):
        assert "원천 전체 계정 비교" in report
        assert "100000000000000099.250" in report
        assert "99999999999999999.125" in report
        assert "전년 동일 기간" in report
        assert "frmtrm_amount" in report
        assert "2025-12-31" in report
        assert "<script>" not in report
    assert 'href="https://dart.fss.or.kr/' in make_html(dataset, result)


def test_export_consumes_precomputed_history_and_drops_untrusted_source_links():
    dataset = raw_history_sample()
    result = {"account_history": {"coverage": {"compared": 1}, "limitations": ["검증된 비교만"], "rows": [{
        "account_name": "사전 계산된 행", "account_id": "ifrs-full_Revenue", "to_period": "2025",
        "current": "987654321.12345", "status": "not_comparable", "reason": "기간 검토 중",
        "source_urls": ["javascript:alert(1)", "https://dart.fss.or.kr:8000/", "https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20260301000001"],
    }]}}
    html = make_html(dataset, result)
    assert "사전 계산된 행" in html
    assert "987654321.12345" in html
    assert "검증된 비교만" in html
    assert "javascript:" not in html
    assert "dart.fss.or.kr:8000" not in html

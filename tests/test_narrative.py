import json

import httpx
import pytest

from dart_analyst.models import Dataset, Period
from dart_analyst.narrative import CommentaryError, build_summary, generate_ai_commentary, validate_commentary


METRICS = {"m0": {"label": "영업이익률", "display_value": "-0.67 %", "status": "calculated"}}


def claim(**extra):
    value = {"kind": "observation", "metric_refs": ["m0"], "evidence_refs": []}
    value.update(extra)
    return {"claims": [value]}


def test_refs_render_server_values_and_require_review():
    result = validate_commentary(claim(), METRICS, {})
    assert result["claims"][0]["rendered_text"] == "계산된 지표는 영업이익률 -0.67 %입니다."
    assert result["requires_review"] is True


def test_duplicate_metric_refs_are_normalized():
    result = validate_commentary(claim(metric_refs=["m0", "m0"]), METRICS, {})
    assert result["claims"][0]["metric_refs"] == ["m0"]


@pytest.mark.parametrize("payload", [
    claim(text="영업이익률은 90%입니다."),
    claim(evidence_refs=["invented"]),
    claim(kind="question", metric_refs=[]),
    claim(metric_refs=["wrong"]),
    {"claims": []},
])
def test_invalid_ai_claims_fail_closed(payload):
    with pytest.raises(CommentaryError):
        validate_commentary(payload, METRICS, {})


def test_unsupported_period_claim_does_not_hide_valid_sibling():
    unsupported = claim(text="영업이익률은 {{metric:m0}}로 전년 대비 개선되지 않은 상태입니다.")
    valid = claim(kind="question", evidence_refs=["n0"])
    result = validate_commentary({"claims": unsupported["claims"] + valid["claims"]}, METRICS, {
        "n0": {"topic": "회계정책"},
    })
    assert result["omitted_claims"] == 1
    assert len(result["claims"]) == 1
    assert result["claims"][0]["rendered_text"] == (
        "산식과 원천 계정을 확인하세요. ‘회계정책’ 주석의 적용 범위도 확인하세요. "
        "검토 지표는 영업이익률 -0.67 %입니다."
    )


def test_metric_only_question_leads_with_a_concrete_action():
    result = validate_commentary(claim(kind="question"), METRICS, {})
    assert result["claims"][0]["rendered_text"] == "산식과 원천 계정을 확인하세요. 검토 지표는 영업이익률 -0.67 %입니다."


def test_flagged_revenue_growth_question_identifies_what_to_verify():
    from dart_analyst.narrative import _catalog
    metrics, _ = _catalog(Dataset("검증"), {"metrics": [{
        "key": "revenue_growth", "label": "전년 동기 매출 성장률", "value": "372.74",
        "unit": "%", "status": "calculated", "source_ids": ["R1"],
    }]})
    result = validate_commentary(claim(kind="question"), metrics, {})
    assert result["claims"][0]["rendered_text"] == (
        "매출 성장률의 비교 기간이 같은지 확인하고, 계산에 쓴 전년 동기 매출액을 공시 원문과 대조하세요. "
        "검토 지표는 전년 동기 매출 성장률 372.74 %입니다."
    )


def test_catalog_never_falls_back_to_older_metrics():
    from dart_analyst.narrative import _catalog
    dataset = Dataset("검증", periods=[
        Period("2025", 2025, "2025-01-01", "2025-12-31"),
        Period("2026 H1", 2026, "2026-01-01", "2026-06-30", kind="YTD"),
    ])
    metrics, _ = _catalog(dataset, {"metrics": [{
        "period": "2025", "key": "operating_margin", "label": "영업이익률",
        "value": "10", "unit": "%", "status": "calculated",
    }]})
    assert metrics == {}


def test_summary_does_not_treat_incomplete_checks_as_pass():
    result = build_summary(Dataset("가상", source_mode="demo"), {"checks": [{"status": "incomplete"}, {"status": "fail"}]})
    assert any("가상" in line for line in result)
    assert any("차이가 발견" in line for line in result)
    assert any("완료하지 못" in line for line in result)


def test_summary_avoids_duplicate_ytd_label_and_flags_extreme_metrics():
    from dart_analyst.models import Period
    dataset = Dataset("검증", periods=[Period("2026 2분기 누적", 2026, "2026-01-01", "2026-06-30", kind="YTD")])
    analysis = {"metrics": [
        {"period": "2026 2분기 누적", "key": "revenue_growth", "label": "매출 증감률", "value": "230.8036", "unit": "%", "status": "calculated", "source_ids": ["R1"]},
        {"period": "2026 2분기 누적", "key": "net_margin", "label": "순이익률", "value": "101.7995", "unit": "%", "status": "calculated", "source_ids": ["R1"]},
    ], "checks": []}
    lines = build_summary(dataset, analysis)
    assert not any("누적 누적" in line for line in lines)
    warning = next(line for line in lines if "이상치 검토 필요" in line)
    assert "230.8 %" in warning
    assert "101.8 %" in warning


def test_summary_flags_extreme_comparison_changes():
    from dart_analyst.models import Period
    dataset = Dataset("검증", periods=[Period("2025", 2025, "2025-01-01", "2025-12-31")])
    analysis = {"metrics": [], "checks": [], "comparisons": [{
        "to_period": "2025", "key": "operating_profit", "label": "영업이익",
        "previous": "10", "current": "70", "delta": "60", "pct": "600",
        "status": "calculated", "source_ids": ["R1"],
    }]}
    warning = next(line for line in build_summary(dataset, analysis) if "급격한 변동 검토 필요" in line)
    assert "600 %" in warning


def test_catalog_marks_extreme_metrics_and_formats_values():
    from dart_analyst.models import Period
    from dart_analyst.narrative import _catalog
    dataset = Dataset("검증", periods=[Period("2026 H1", 2026, "2026-01-01", "2026-06-30", kind="YTD")])
    metrics, _ = _catalog(dataset, {"metrics": [{"period": "2026 H1", "key": "operating_margin", "label": "영업이익률", "value": "74.4174278", "unit": "%", "status": "calculated"}]})
    assert metrics["m0"]["display_value"] == "74.42 %"
    assert metrics["m0"]["review_flag"]


def test_gross_margin_is_not_flagged_without_industry_context():
    from dart_analyst.models import Period
    from dart_analyst.narrative import _catalog
    dataset = Dataset("유통", periods=[Period("2026 H1", 2026, "2026-01-01", "2026-06-30", kind="YTD")])
    metrics, _ = _catalog(dataset, {"metrics": [{"period": "2026 H1", "key": "gross_margin", "label": "매출총이익률", "value": "62.3", "unit": "%", "status": "calculated"}]})
    assert "review_flag" not in metrics["m0"]


def test_extreme_change_warning_ignores_oci_noise():
    from dart_analyst.models import Period
    dataset = Dataset("검증", periods=[Period("2025", 2025, "2025-01-01", "2025-12-31")])
    analysis = {"metrics": [], "checks": [], "comparisons": [{
        "to_period": "2025", "key": "oci", "label": "기타포괄손익",
        "previous": "1", "current": "9", "delta": "8", "pct": "800",
        "status": "calculated", "source_ids": ["R1"],
    }]}
    assert not any("급격한 변동 검토 필요" in line for line in build_summary(dataset, analysis))


def test_optional_ai_mock_request_and_validation():
    def handler(request):
        body = json.loads(request.content)
        assert request.url.path == "/api/chat"
        assert body["model"] == "test-model"
        assert body["stream"] is False
        assert body["think"] is False
        assert body["format"]["required"] == ["claims"]
        schema = body["format"]["properties"]["claims"]["items"]
        assert schema["additionalProperties"] is False
        assert "text" not in schema["properties"]
        assert schema["properties"]["metric_refs"]["items"]["enum"] == ["m0"]
        return httpx.Response(200, json={"done": True, "done_reason": "stop", "message": {"role": "assistant", "content": json.dumps(claim(), ensure_ascii=False)}, "prompt_eval_count": 100, "eval_count": 50})
    dataset = Dataset("가상", periods=[Period("2026 H1", 2026, "2026-01-01", "2026-06-30", kind="YTD")])
    result = generate_ai_commentary(dataset, {"metrics": [{
        "period": "2026 H1", "key": "revenue_growth", "label": "전년 동기 매출 성장률",
        "value": "10.45737967", "unit": "%", "status": "calculated", "source_ids": ["R1"],
    }]}, "http://127.0.0.1:11434", "test-model", client=httpx.Client(transport=httpx.MockTransport(handler)))
    assert result["usage"]["input_tokens"] == 100
    assert result["format_version"] == 7
    assert result["period"] == "2026 H1"
    assert result["metric_catalog"]["m0"]["source_ids"] == ["R1"]
    assert result["claims"][0]["rendered_text"] == "계산된 지표는 전년 동기 매출 성장률 10.46 %입니다."
    assert result["evidence_catalog"] == {}
    assert "test-secret" not in json.dumps(result)


def test_ollama_industry_review_separates_reported_change_and_sector_context():
    from dart_analyst.demo import build_demo
    from dart_analyst.engine import analyze

    dataset = build_demo()
    dataset.source_mode = "live"
    dataset.metadata["industry_code"] = "26121"

    def handler(request):
        body = json.loads(request.content)
        context = json.loads(body["messages"][1]["content"])
        lens = context["industry_reviews"]["i0"]
        assert lens["title"].startswith("반도체")
        assert {r["key"] for r in lens["comparisons"]} == {"revenue", "operating_profit"}
        assert all(r["source_ids"] for r in lens["comparisons"])
        metric_id = next(iter(context["metrics"]))
        payload = {"claims": [{"kind": "observation", "metric_refs": [metric_id], "evidence_refs": []}],
                   "industry_refs": ["i0"]}
        return httpx.Response(200, json={"done": True, "done_reason": "stop", "message": {"content": json.dumps(payload)}})

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        result = generate_ai_commentary(dataset, analyze(dataset), "http://127.0.0.1:11434", "test-model", client=client)
    review, = result["industry_reviews"]
    assert "영업이익률 차이" in review["observation"]
    assert "가동률" in review["background"]
    assert "가동률" not in review["observation"]


def test_provider_error_does_not_expose_key():
    client = httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(401, json={"error": "test-secret"})))
    with pytest.raises(CommentaryError) as error:
        generate_ai_commentary(Dataset("가상"), {"metrics": [{
            "label": "영업이익률", "value": "1", "status": "calculated",
        }]}, "http://127.0.0.1:11434", "model", client=client)
    assert "401" in str(error.value)
    assert "test-secret" not in str(error.value)


@pytest.mark.parametrize("body", [[], {"done": True, "done_reason": "stop", "message": None}])
def test_malformed_provider_response_is_reported_as_commentary_error(body):
    with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(200, json=body))) as client:
        with pytest.raises(CommentaryError, match="계산 결과는 유지"):
            generate_ai_commentary(Dataset("가상"), {"metrics": [{
                "label": "영업이익률", "value": "1", "status": "calculated",
            }]}, "http://127.0.0.1:11434", "model", client=client)


def test_summary_keeps_latest_annual_and_ytd_trends_separate():
    from dart_analyst.demo import build_demo
    from dart_analyst.engine import analyze
    dataset = build_demo()
    lines = build_summary(dataset, analyze(dataset))
    financial = [line for line in lines if "[근거:" in line]
    assert len(financial) == 8
    assert any("2025 연간" in line and "70 억 원 → 45 억 원" in line and "DEMO-2025-FY" in line for line in financial)
    assert any("2026 H1 누적" in line and "28 억 원 → 30 억 원" in line for line in financial)
    assert any("FCF 2024 20 억 원 → -35 억 원" in line for line in financial)
    assert any("DSO" in line and "54.75 일" in line for line in financial)
    assert not any("2026 H1" in line and "2025 9 % →" in line for line in financial)


def test_summary_omits_uncomputed_or_partial_numbers_and_warns_archive():
    from dart_analyst.demo import build_demo
    dataset = build_demo()
    dataset.source_mode = "import"
    analysis = {
        "metrics": [{"period": "2025", "key": "fcf", "value": "7777777777", "unit": "KRW", "status": "partial"}],
        "comparisons": [{"to_period": "2025", "key": "revenue", "previous": "7777777777", "current": "8888888888", "delta": "1111111111", "status": "not_comparable"}],
    }
    result = "\n".join(build_summary(dataset, analysis))
    assert "DART를 재조회하지 않았" in result
    assert "[근거:" not in result
    assert "7777777777" not in result


def test_summary_omits_ratio_history_when_comparatives_are_restated():
    from decimal import Decimal
    from dart_analyst.demo import build_demo
    from dart_analyst.engine import analyze
    dataset = build_demo()
    annual = next(p for p in dataset.periods if p.label == "2025")
    annual.comparatives["receivables"].amount += Decimal("100000000")
    lines = build_summary(dataset, analyze(dataset))
    line = next(line for line in lines if "2025 연간" in line and "DSO" in line)
    assert "DSO (총매출 근사치) 2024" not in line
    assert "DIO 2024" in line

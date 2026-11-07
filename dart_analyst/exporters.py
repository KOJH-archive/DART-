"""Portable financial reports with provenance and explicit data limitations."""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, localcontext
from html import escape
from io import BytesIO
import json
import re
from urllib.parse import urlparse

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from .models import Dataset
from .narrative import build_summary, commentary_matches
from .account_history import build_account_history


def safe_source_url(value: str | None) -> str | None:
    try:
        parsed = urlparse(value or "")
        if parsed.scheme == "https" and parsed.hostname in {"dart.fss.or.kr", "opendart.fss.or.kr"} and not parsed.username and not parsed.password and parsed.port in (None, 443):
            return value
    except ValueError:
        pass
    return None


def _text(value) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, default=str)
    if isinstance(value, Decimal):
        return format(value, "f")
    return str(value)


def _mode(dataset: Dataset) -> str:
    return {"demo": "가상 검증 데이터 · 실제 기업 아님", "live": "DART 수집 데이터", "import": "가져온 분석 데이터"}.get(dataset.source_mode, "사용자 데이터")


def _sections(dataset: Dataset, analysis: dict):
    yield "자료 범위·처리 현황", ["항목", "내용"], [
        ["회사", dataset.company], ["데이터 유형", _mode(dataset)], ["연결범위", dataset.scope],
        ["처리 현황", analysis.get("coverage", {})], ["자료 메타데이터", dataset.metadata],
        ["표시 단위", "비교·대조 금액은 통화 기본 단위, 변화율은 %. 요약만 소수 둘째 자리 반올림; KRW 금액은 억 원 표시."],
        *[[p.label, {"시작": p.start, "종료": p.end, "기간": p.kind, "연결범위": p.scope, "공시": p.filing_id, "이슈": p.issues}] for p in dataset.periods],
        *[["자료 이슈", issue] for issue in dataset.issues],
    ]
    yield "핵심 지표", ["기간", "지표", "값", "단위", "상태", "계산식", "출처", "계산 제한 사유", "입력 계정"], [
        [r.get(k) for k in ("period", "label", "value", "unit", "status", "formula", "source_ids", "reason", "input_keys")] for r in analysis.get("metrics", [])]
    periods = {p.label: p for p in dataset.periods}
    comparisons = []
    for row in analysis.get("comparisons", []):
        period = periods.get(row.get("to_period"))
        fact = period.facts.get(row.get("key")) if period else None
        comparisons.append([row.get(k) for k in ("label", "from_period", "to_period", "previous", "current", "delta", "pct", "status", "reason", "source_ids")] + [fact.currency if fact else "미확인"])
    yield "계정별 과거 비교", ["계정", "비교기간", "당기", "비교금액", "당기금액", "차이", "변화율 (%)", "상태", "설명", "출처", "금액 통화"], comparisons
    history = analysis.get("account_history")
    if not isinstance(history, dict):
        history = build_account_history(dataset)
    yield "원천 계정 비교 범위", ["항목", "내용"], [
        ["처리 현황", history.get("coverage", {})],
        *[["비교 제한", limitation] for limitation in history.get("limitations", [])],
    ]
    raw_comparisons = []
    for row in history.get("rows", []):
        period = periods.get(row.get("to_period"))
        urls = [url for value in row.get("source_urls", []) if (url := safe_source_url(value))]
        raw_comparisons.append([
            row.get("account_name"), row.get("account_id"), row.get("sj_div"), row.get("account_detail"),
            row.get("scope"), row.get("to_period"), period.start if period else None, period.end if period else None,
            row.get("from_period"), row.get("comparison_basis"), row.get("currency"),
            row.get("previous"), row.get("current"), row.get("delta"), row.get("pct"),
            row.get("status"), row.get("reason"), row.get("restated"),
            row.get("historical_previous"), row.get("historical_source_id"), row.get("previous_account_name"),
            row.get("current_field"), row.get("previous_field"), row.get("source_ids"),
            urls[0] if urls else None, urls[1] if len(urls) > 1 else None,
        ])
    yield "원천 전체 계정 비교", [
        "공시 계정명", "계정 ID", "재무제표", "구성원", "연결범위", "분석기간", "당기 시작일", "당기 종료일",
        "비교기", "비교 기준", "금액 통화", "비교금액", "당기금액", "차이", "변화율 (%)",
        "상태", "설명", "재작성 차이", "기존 공시 비교금액", "기존 공시번호", "기존 계정명",
        "당기 원천필드", "비교 원천필드", "출처 공시번호", "원문 1", "원문 2",
    ], raw_comparisons
    yield "회계 연결 대조", ["기간", "대조항목", "상태", "좌변", "우변", "차이", "허용오차", "설명", "입력 계정"], [
        [r.get(k) for k in ("period", "label", "status", "left", "right", "difference", "tolerance", "reason", "input_keys")] for r in analysis.get("checks", [])]
    bridge_rows = []
    for row in analysis.get("checks", []):
        period = periods.get(row.get("period"))
        for key in row.get("input_keys", []):
            fact = period.facts.get(key) if period else None
            normalized = None
            if fact and fact.amount is not None:
                with localcontext() as context:
                    context.prec = max(64, len(fact.amount.as_tuple().digits) + len(fact.unit.as_tuple().digits) + 2)
                    normalized = fact.amount * fact.unit
            bridge_rows.append([row.get("period"), row.get("label"), row.get("status"), key,
                                fact.name if fact else key, normalized, fact.currency if fact else None,
                                fact.start if fact else None, fact.end if fact else None,
                                fact.scope if fact else None, fact.source_id if fact else None,
                                safe_source_url(fact.source_url) if fact else None,
                                fact.reason if fact else "필요 원천 계정 미확보"])
    yield "대조 입력 상세", ["기간", "대조항목", "대조 상태", "입력 계정", "공시 계정명", "단위 환산 금액", "통화", "시작일", "종료일", "연결범위", "공시번호", "원문", "자료 사유"], bridge_rows
    yield "주석 점검", ["주제", "상태", "내용", "위치", "공시", "원문"], [
        [r.get("topic"), r.get("status"), r.get("excerpt"), r.get("location"), r.get("source_id"), safe_source_url(r.get("source_url"))] for r in dataset.notes]
    memo = analysis.get("ai_commentary")
    if isinstance(memo, dict) and commentary_matches(dataset, memo):
        rows = [[memo["period"], "생성 정보", f"로컬 Ollama · {memo.get('model', '')}",
                 "공시 수치의 계산은 규칙 기반이며 AI는 근거와 업종 관점을 선택합니다.", "", ""]]
        for review in memo.get("industry_reviews", []):
            sources = list(dict.fromkeys(s for row in review.get("comparisons", []) for s in row.get("source_ids", [])))
            rows.append([memo["period"], review.get("title"), review.get("observation"),
                         review.get("background"), review.get("question"), sources])
            for note in review.get("supporting_notes", []):
                rows.append([memo["period"], note.get("topic"), note.get("excerpt"),
                             "관련 사업 공시 발췌", note.get("location"), note.get("source_id")])
        for claim in memo.get("claims", []):
            rows.append([memo["period"], "계산 관찰" if claim.get("kind") == "observation" else "확인 항목",
                         claim.get("rendered_text"), "계산·발췌 근거 선택", "",
                         {"metrics": [{"ref": ref, **memo.get("metric_catalog", {}).get(ref, {})}
                                      for ref in claim.get("metric_refs", [])],
                          "notes": [{"ref": ref, **memo.get("evidence_catalog", {}).get(ref, {})}
                                    for ref in claim.get("evidence_refs", [])]}])
        yield "AI 검토 메모", ["기준 기간", "항목", "확인한 변화·내용", "업종 배경·구분", "추가 확인 질문·위치", "근거"], rows


def _source_rows(dataset: Dataset):
    for period in dataset.periods:
        for kind, facts in (("당기", period.facts), ("비교기", period.comparatives)):
            for key, fact in facts.items():
                yield [period.label, kind, key, fact.name, fact.amount, fact.unit, fact.currency, fact.statement, fact.start, fact.end, fact.period_kind, fact.scope, fact.attribution, fact.account_id, fact.source_field, fact.source_id, safe_source_url(fact.source_url), fact.reason, fact.source_details or None]


SOURCE_HEADERS = ["분석기간", "구분", "내부계정", "공시계정", "원천금액", "단위배수", "통화", "재무제표", "시작일", "종료일", "기간종류", "연결범위", "귀속", "계정ID", "원천필드", "공시번호", "원문", "결측사유", "원천 상세"]


def make_excel(dataset: Dataset, analysis: dict) -> bytes:
    wb = Workbook()
    wb.remove(wb.active)

    def sheet(name, headers, rows):
        ws = wb.create_sheet(name[:31])
        for index, row in enumerate([headers, *rows], 1):
            for col, value in enumerate(row, 1):
                # Explicit strings preserve large financial values and prevent formula injection.
                content = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", _text(value))
                if len(content) > 32767:
                    content = content[:32680] + " [Excel 셀 길이 초과: 전체 내용은 원문에서 확인]"
                cell = ws.cell(index, col)
                cell.value = content
                cell.data_type = "s"
                cell.alignment = Alignment(vertical="top", wrap_text=True)
                if index == 1:
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill("solid", fgColor="153C48")
            if index > 1 and index % 2 == 0:
                for cell in ws[index]:
                    cell.fill = PatternFill("solid", fgColor="F2F6F8")
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for col in range(1, ws.max_column + 1):
            ws.column_dimensions[get_column_letter(col)].width = 24 if col < 5 else 32
        return ws

    sheet("보고서 정보", ["항목", "내용"], [
        ["회사", dataset.company], ["데이터 유형", _mode(dataset)], ["연결범위", dataset.scope],
        ["생성 시각 UTC", datetime.now(timezone.utc).isoformat()], ["단위", "금액·비율의 단위는 각 열 참조. 원천 금액은 정확한 문자열로 저장"],
        ["검증 범위", "대조 통과는 확인 가능한 식의 일치이며 전체 공시의 완전성 보증이 아닙니다."],
        ["처리 현황", analysis.get("coverage", {})], ["메타데이터", dataset.metadata],
        *[["요약", x] for x in build_summary(dataset, analysis)],
        *[["자료 이슈", x] for x in dataset.issues],
        *[[f"{p.label} 이슈", x] for p in dataset.periods for x in p.issues],
    ])
    for title, headers, rows in _sections(dataset, analysis):
        sheet(title, headers, rows)
    sheet("원천 계정·근거", SOURCE_HEADERS, list(_source_rows(dataset)))
    raw = [[p.label, json.dumps(row, ensure_ascii=False, default=str)] for p in dataset.periods for row in p.raw_accounts]
    sheet("원본 API 행", ["기간", "원본 JSON"], raw)
    buffer = BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


_NUMERIC_HEADERS = {
    "값", "비교금액", "당기금액", "차이", "변화율 (%)", "좌변", "우변", "허용오차",
    "단위 환산 금액", "원천금액", "단위배수", "기존 공시 비교금액",
}


def _html_table(headers, rows) -> str:
    def column_class(index):
        return ' class="number"' if index < len(headers) and headers[index] in _NUMERIC_HEADERS else ''

    header = "".join(f'<th scope="col"{column_class(index)}>{escape(_text(value))}</th>'
                     for index, value in enumerate(headers))
    cells = []
    for row in rows:
        line = []
        for index, value in enumerate(row):
            display = escape(_text(value))
            url = safe_source_url(value) if isinstance(value, str) else None
            content = f'<a href="{escape(url, quote=True)}" rel="noopener noreferrer">공시 원문 ↗</a>' if url else display
            line.append(f"<td{column_class(index)}>{content}</td>")
        cells.append("<tr>" + "".join(line) + "</tr>")
    if not cells:
        cells.append(f'<tr><td colspan="{len(headers)}" class="empty">확보된 자료 없음</td></tr>')
    return '<div class="table-wrap" tabindex="0" role="region" aria-label="분석 표"><table><thead><tr>' + header + "</tr></thead><tbody>" + "".join(cells) + "</tbody></table></div>"


def make_html(dataset: Dataset, analysis: dict) -> str:
    company = escape(dataset.company)
    sections = []
    navigation = ['<a href="#summary"><span>00</span>검토 요약</a>']
    for index, (title, headers, rows) in enumerate(_sections(dataset, analysis), 1):
        anchor = f"section-{index:02d}"
        title = escape(title)
        navigation.append(f'<a href="#{anchor}"><span>{index:02d}</span>{title}</a>')
        sections.append(f'<section id="{anchor}" class="report-section"><div class="section-heading"><span class="section-index">{index:02d}</span><h2>{title}</h2></div>{_html_table(headers, rows)}</section>')
    source_index = len(sections) + 1
    navigation.append(f'<a href="#sources"><span>{source_index:02d}</span>원천 계정과 계산 근거</a>')
    source_table = _html_table(SOURCE_HEADERS, list(_source_rows(dataset)))
    summaries = []
    for text in build_summary(dataset, analysis):
        main, separator, evidence = text.partition(" [근거: ")
        reference = f'<span class="summary-reference">{escape(separator + evidence)}</span>' if separator else ''
        summaries.append(f'<p>{escape(main)}{reference}</p>')
    source_mode = escape(_mode(dataset))
    scope = {"CFS": "연결재무제표", "OFS": "별도재무제표"}.get(dataset.scope, escape(dataset.scope))
    annual_count = sum(period.kind == "FY" for period in dataset.periods)
    interim_count = sum(period.kind != "FY" for period in dataset.periods)
    generated = datetime.now(timezone.utc).strftime("%Y.%m.%d %H:%M UTC")
    badge_class = 'source-badge sample' if dataset.source_mode == 'demo' else 'source-badge'
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{company} 재무·회계 분석</title><style>
:root{{--paper:#fff;--canvas:#f8f9f6;--ink:#202725;--muted:#6c746e;--rule:#dedfd8;--accent:#244c41}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:24px}}body{{margin:0;background:var(--canvas);color:var(--ink);font:14px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI","Apple SD Gothic Neo","Malgun Gothic",sans-serif;overflow-wrap:break-word}}a{{color:var(--accent);text-underline-offset:3px}}a:focus-visible,.table-wrap:focus-visible{{outline:2px solid var(--accent);outline-offset:4px}}.topbar{{border-bottom:1px solid var(--rule);padding:17px 34px;display:flex;align-items:center;justify-content:space-between;gap:18px;font-size:12px;color:var(--muted)}}.wordmark{{font-size:15px;font-weight:750;letter-spacing:-.04em;color:var(--ink)}}.topbar-label{{padding-left:14px;margin-left:14px;border-left:1px solid var(--rule)}}.generated{{font-variant-numeric:tabular-nums;white-space:nowrap}}.layout{{display:grid;grid-template-columns:212px minmax(0,1fr);gap:44px;max-width:1570px;margin:auto;padding:38px 34px 64px}}.contents{{align-self:start;position:sticky;top:24px}}.contents-label{{margin:0 0 14px;color:var(--muted);font-size:11px;font-weight:600}}.contents a{{display:flex;gap:12px;text-decoration:none;font-size:12px;line-height:1.45;padding:9px 0;color:#58615b}}.contents a:hover{{color:var(--accent)}}.contents a span{{font-size:10px;color:#8d948d;font-variant-numeric:tabular-nums;min-width:15px;padding-top:2px}}main{{min-width:0}}.report-header{{padding:0 0 28px;border-bottom:1px solid var(--ink);margin-bottom:34px}}.document-type{{margin:0 0 13px;font-size:12px;color:var(--muted)}}h1{{margin:12px 0 12px;font-size:clamp(28px,3vw,38px);font-weight:600;line-height:1.25;letter-spacing:-.045em}}.header-meta{{display:flex;align-items:center;flex-wrap:wrap;gap:9px 18px;color:var(--muted);font-size:12px}}.source-badge{{display:inline-block;border:1px solid var(--rule);padding:3px 8px;background:var(--paper);font-size:11px;color:#4b5850}}.source-badge.sample{{background:#f4f0e3;border-color:#e4dcc4;color:#77633a}}.report-section{{min-width:0;margin:0 0 40px;scroll-margin-top:24px}}.section-heading{{display:flex;align-items:baseline;gap:12px;margin-bottom:16px}}.section-index{{font-size:11px;color:#90978e;font-variant-numeric:tabular-nums}}h2{{margin:0;font-size:18px;font-weight:600;letter-spacing:-.035em}}.summary-body{{border-top:1px solid var(--rule)}}.summary-body p{{margin:0;padding:17px 0;border-bottom:1px solid var(--rule);font-size:14px;line-height:1.8;max-width:100%}}.summary-reference{{display:block;margin-top:6px;font-size:11px;line-height:1.65;color:var(--muted)}}.note{{font-size:11px;line-height:1.7;color:var(--muted);margin-top:14px}}.table-wrap{{width:100%;max-height:640px;overflow:auto;background:var(--paper);border-top:1px solid #b6bdb4;border-bottom:1px solid var(--rule);overscroll-behavior:contain;scrollbar-width:thin}}table{{border-collapse:separate;border-spacing:0;width:100%;font-size:12px;line-height:1.55}}th,td{{text-align:left;vertical-align:top;padding:11px 13px;border-bottom:1px solid #e9ebe4;min-width:96px;max-width:380px;overflow-wrap:anywhere}}th{{position:sticky;top:0;z-index:1;background:#f0f2ec;color:#4e5a51;font-size:11px;font-weight:600;white-space:nowrap;box-shadow:inset 0 -1px var(--rule)}}tbody tr:last-child td{{border-bottom:0}}tbody tr:hover{{background:#f7f9f4}}.number{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:11px;min-width:115px}}th.number{{font-family:inherit}}.empty{{padding:28px 13px;color:var(--muted)}}footer{{border-top:1px solid var(--rule);padding-top:18px;display:flex;justify-content:space-between;gap:20px;font-size:11px;color:var(--muted)}}
@media(max-width:900px){{.layout{{grid-template-columns:minmax(0,1fr);gap:28px;padding:26px 20px 40px}}.contents{{position:static;border-bottom:1px solid var(--rule);padding-bottom:16px}}.contents-label{{margin-bottom:8px}}.contents-links{{display:flex;flex-wrap:wrap;column-gap:22px}}.contents a{{padding:5px 0}}.topbar{{padding:15px 20px}}.table-wrap{{max-height:500px}}}}
@media(max-width:540px){{.generated{{display:none}}.header-meta{{gap:8px 12px}}.report-header{{margin-bottom:26px}}.report-section{{margin-bottom:30px}}th,td{{padding:10px}}footer{{display:block}}footer p{{margin:4px 0}}}}
@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
@media print{{:root{{--canvas:#fff}}html{{scroll-padding:0}}.topbar{{padding:0 0 10px}}.layout{{display:block;padding:20px 0 0;max-width:none}}.contents{{display:none}}.report-header{{padding-bottom:18px;margin-bottom:24px}}h1{{font-size:27px}}.report-section{{margin-bottom:24px;break-before:auto}}.section-heading{{break-after:avoid}}.summary-body p{{padding:10px 0;break-inside:avoid}}.table-wrap{{max-height:none;overflow:visible;border-top:1px solid var(--rule)}}table{{font-size:8px;table-layout:fixed}}th,td,.number{{min-width:0;max-width:none;font-size:8px;padding:5px;white-space:normal;overflow-wrap:anywhere}}th{{position:static}}thead{{display:table-header-group}}tr{{break-inside:avoid}}a{{color:inherit;text-decoration:none}}footer{{margin-top:20px}}}}
</style></head><body><div class="topbar"><div><span class="wordmark">DART</span><span class="topbar-label">기업 재무 보고서</span></div><span class="generated">{generated}</span></div><div class="layout"><nav class="contents" aria-label="보고서 목차"><p class="contents-label">목차</p><div class="contents-links">{''.join(navigation)}</div></nav><main><header class="report-header"><p class="document-type">재무·회계 분석</p><h1>{company}</h1><div class="header-meta"><span class="{badge_class}">{source_mode}</span><span>{scope}</span><span>연간 {annual_count}개 · 중간 {interim_count}개 기간</span></div></header><section id="summary" class="report-section"><div class="section-heading"><span class="section-index">00</span><h2>검토 요약</h2></div><div class="summary-body">{''.join(summaries)}</div><p class="note">대조 일치는 확보된 항목의 산식 일치를 뜻합니다. 자료 부족·미확인 주석은 별도 검토가 필요합니다.</p></section>{''.join(sections)}<section id="sources" class="report-section"><div class="section-heading"><span class="section-index">{source_index:02d}</span><h2>원천 계정과 계산 근거</h2></div>{source_table}</section><footer><p>DART · {company}</p><p>금액·비율의 단위와 원천 정밀도는 각 표를 따릅니다.</p></footer></main></div></body></html>'''


def make_markdown(dataset: Dataset, analysis: dict) -> str:
    def md(value):
        return escape(_text(value)).replace("|", "\\|").replace("\n", "<br>").replace("\r", "")
    lines = [f"# {md(dataset.company)} 재무·회계 분석", "", f"{_mode(dataset)} · {dataset.scope}", "", "## 검토 요약", ""]
    lines += [f"- {md(x)}" for x in build_summary(dataset, analysis)]
    for title, headers, rows in _sections(dataset, analysis):
        lines += ["", f"## {title}", "", "| " + " | ".join(map(md, headers)) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
        lines += ["| " + " | ".join(map(md, row)) + " |" for row in rows]
    lines += ["", "## 원천 계정", "", "| " + " | ".join(SOURCE_HEADERS) + " |", "| " + " | ".join("---" for _ in SOURCE_HEADERS) + " |"]
    lines += ["| " + " | ".join(map(md, row)) + " |" for row in _source_rows(dataset)]
    lines += ["", "대조 통과는 확보된 자료의 계산식 일치입니다. 미완료 대조·주석은 이상 없음으로 해석하지 않습니다."]
    return "\n".join(lines)

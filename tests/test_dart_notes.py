from io import BytesIO
from zipfile import ZipFile

import pytest

from dart_analyst import dart_notes
from dart_analyst.dart_notes import parse_note_topics


SOURCE_ID = "20260311001234"
SOURCE_URL = f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={SOURCE_ID}"


def archive_of(files: dict[str, str | bytes]) -> bytes:
    stream = BytesIO()
    with ZipFile(stream, "w") as archive:
        for name, content in files.items():
            archive.writestr(name, content.encode("utf-8") if isinstance(content, str) else content)
    return stream.getvalue()


def by_topic(payload: bytes) -> dict:
    return {row["topic"]: row for row in parse_note_topics(payload, SOURCE_ID, SOURCE_URL)}


def test_extracts_five_passages_with_source_and_locations():
    xml = """<?xml version="1.0" encoding="utf-8"?>
    <DOCUMENT><SECTION>
      <TITLE>중요한 회계정책</TITLE><P>수익은 수행의무가 충족되는 시점에 인식합니다.</P>
      <TITLE>차입금 및 유동성 위험</TITLE><P>차입금의 만기는 2027년입니다.</P>
      <TITLE>우발채무 및 약정사항</TITLE><P>보증 약정의 상세내용입니다.</P>
      <TITLE>특수관계자 거래</TITLE><P>거래금액은 100원입니다.</P>
      <TITLE>감사의견</TITLE><P>감사인의 원문 의견을 확인해야 합니다.</P>
    </SECTION></DOCUMENT>"""
    rows = by_topic(archive_of({"filing.xml": xml}))
    assert len(rows) == 5
    assert all(row["status"] == "발췌 가능" for row in rows.values())
    assert "수행의무" in rows["회계정책"]["excerpt"]
    assert "2027년" in rows["차입금·유동성"]["excerpt"]
    assert all(row["source_id"] == SOURCE_ID for row in rows.values())
    assert all(row["source_url"] == SOURCE_URL for row in rows.values())
    assert all("filing.xml / DOCUMENT/SECTION[1]/TITLE[" in row["location"] for row in rows.values())


def test_absent_topic_requires_original_review_and_does_not_conclude_no_risk():
    rows = by_topic(archive_of({"report.xml": "<DOCUMENT><P>회사의 일반현황입니다.</P></DOCUMENT>"}))
    assert all(row["status"] == "원문 확인 필요" for row in rows.values())
    assert all(row["excerpt"] == "" for row in rows.values())
    assert all(row["location"] == "자동 탐색에서 해당 절을 찾지 못함" for row in rows.values())


def test_preserves_words_split_by_inline_markup_and_caps_excerpt():
    xml = "<DOCUMENT><P>회계<SPAN>정책</SPAN> " + "정책설명 " * 200 + "</P></DOCUMENT>"
    row = by_topic(archive_of({"report.xml": xml}))["회계정책"]
    assert row["status"] == "발췌 가능"
    assert row["excerpt"].startswith("회계정책")
    assert len(row["excerpt"]) <= 600


def test_repairs_dart_literals_without_changing_existing_references_or_cdata():
    xml = """<DOCUMENT>
      <!-- comment with an unescaped ampersand & -->
      <TITLE>회계정책</TITLE>
      <P>S&P, R&D, A &amp; B, &#x26;, <![CDATA[C&D]]></P>
      <TD ENG="D&O > caption"><이사ㆍ감사 전체의 보수현황></TD>
    </DOCUMENT>"""
    row = by_topic(archive_of({"report.xml": xml}))["회계정책"]
    assert row["status"] == "발췌 가능"
    assert row["excerpt"] == "회계정책 S&P, R&D, A & B, &, C&D <이사ㆍ감사 전체의 보수현황>"


def test_repairs_dart_paragraph_captions_with_observed_label_shapes():
    xml = """<DOCUMENT><TITLE>회계정책</TITLE>
      <P USERMARK="A-C">        <응용처별 매출액과  비중></P>
      <P><연결 기준>        (단위 : 백만원)</P>
      <P>제품별 매출은 다음과 같습니다.<제품별 매출>        (단위: 백만원, %)</P>
      <P><주요 관계회사 및 지분 현황> (기준일: 2026.08.13)</P>
    </DOCUMENT>"""
    row = by_topic(archive_of({"report.xml": xml}))["회계정책"]
    assert row["status"] == "발췌 가능"
    assert row["excerpt"] == (
        "회계정책 <응용처별 매출액과 비중> <연결 기준> (단위 : 백만원) "
        "제품별 매출은 다음과 같습니다.<제품별 매출> (단위: 백만원, %) "
        "<주요 관계회사 및 지분 현황> (기준일: 2026.08.13)"
    )


@pytest.mark.parametrize("tag, before, literal", [("TE", "", "신 설"), ("P", "", "신  설"),
                                                  ("TE", "(3) 배당 조항. (4) ", "신 설")])
def test_repairs_observed_article_addition_inside_prose(tag, before, literal):
    xml = f"""<DOCUMENT><{tag} USERMARK="F-10">부칙- 변경전 : {before}<{literal}>- 변경후 : 회계정책을 설명합니다.</{tag}></DOCUMENT>"""
    policy = by_topic(archive_of({"filing.xml": xml}))["회계정책"]
    assert policy["status"] == "발췌 가능"
    assert "회계정책을 설명합니다." in policy["excerpt"]


def test_repairs_observed_certification_name_in_paragraph():
    xml = """<DOCUMENT><P>고용노동부로부터 <대한민국 일·생활 균형 우수기업 >으로 인증받은 사례입니다.</P>
    <TITLE>회계정책</TITLE><P>연결 기준입니다.</P></DOCUMENT>"""
    assert by_topic(archive_of({"filing.xml": xml}))["회계정책"]["status"] == "발췌 가능"


def test_literal_normalization_preserves_structural_xml_errors():
    xml = '<DOCUMENT><P>부칙- 변경전 : <TABLE>- 변경후 : 회계정책을 설명합니다.</P></DOCUMENT>'
    assert by_topic(archive_of({"filing.xml": xml}))["회계정책"]["status"] == "추출 실패"


def test_repairs_observed_korean_prefixes_and_standalone_captions():
    xml = """<DOCUMENT><P><기후변화> 관련 내용입니다.</P>
    <P USERMARK="B"><New Product Innovation: Hyundai & Genesis></P>
    <SPAN USERMARK="B"><유연근무제도 사용 현황></SPAN>
    <P><SPAN><주식기준보상제도 현황> 회계정책을 설명합니다.</SPAN></P></DOCUMENT>"""
    policy = by_topic(archive_of({"filing.xml": xml}))["회계정책"]
    assert policy["status"] == "발췌 가능"


def test_audit_excerpt_skips_chapter_heading_and_uses_audit_section_body():
    xml = """<DOCUMENT><SECTION>
      <TITLE>V. 회계감사인의 감사의견 등</TITLE>
      <SECTION><TITLE>1. 외부감사에 관한 사항</TITLE><P>당반기 검토보고서 확인.</P></SECTION>
    </SECTION></DOCUMENT>"""
    row = by_topic(archive_of({"report.xml": xml}))["감사의견"]
    assert row["status"] == "발췌 가능"
    assert row["excerpt"] == "1. 외부감사에 관한 사항 당반기 검토보고서 확인."


def test_heading_without_body_requires_original_review():
    xml = "<DOCUMENT><TITLE>감사의견</TITLE><TITLE>기타 자료</TITLE><P>다른 내용</P></DOCUMENT>"
    row = by_topic(archive_of({"report.xml": xml}))["감사의견"]
    assert row["status"] == "원문 확인 필요"
    assert row["excerpt"] == ""


@pytest.mark.parametrize(
    "xml",
    [
        '<!DOCTYPE DOCUMENT [<!ENTITY local SYSTEM "file:///etc/passwd">]><DOCUMENT><P>&local;</P></DOCUMENT>',
        '<!DOCTYPE DOCUMENT [<!ENTITY x "expanded">]><DOCUMENT><P>&x;</P></DOCUMENT>',
        "<DOCUMENT><P>닫히지 않은 원문",
        "<DOCUMENT><P>회계정책 R&D &unresolved;</P></DOCUMENT>",
        "<DOCUMENT><P>회계정책 R&D &#0;</P></DOCUMENT>",
        '<DOCUMENT><P>회계정책 R&D</P><TD><제목 종류="값"></TD></DOCUMENT>',
        '<DOCUMENT><P>회계정책 <제목 종류="값"></P></DOCUMENT>',
    ],
)
def test_rejects_dtd_entities_and_malformed_xml(xml):
    rows = by_topic(archive_of({"report.xml": xml}))
    assert all(row["status"] == "추출 실패" for row in rows.values())
    assert all(row["excerpt"] == "" for row in rows.values())


def test_invalid_archive_returns_structured_failures():
    rows = by_topic(b"<result><status>013</status></result>")
    assert len(rows) == 5
    assert all(row["status"] == "추출 실패" for row in rows.values())


@pytest.mark.parametrize("block", [
    '<TE>광고매체판매업 <개정 2015.03.20></TE>',
    '<P>안전 조직 <설비                      강건화TFT> 발족</P>',
    '<TD>자기주식 보유현황<단기 자기주식 취득ㆍ처분ㆍ소각 계획></TD>',
    '<TD><신설></TD><P>부칙 <2025.3.25></P>',
    '<P><SPAN><</SPAN> 범위 표시</P>',
    '<TE ENG="" CJ telenix co.,Ltd "" VALIGN="MIDDLE">회사</TE>',
    '<TH WIDTH="291" ENG="HD Hyundai Co., Ltd.(formerly, Hyundai Heavy Industries Holdings Co., Ltd.) "">HD현대㈜</TH>',
    '<TD ENG="Company "" WIDTH="291">회사</TD>',
    '<P><SPAN><채무보증</SPAN></P>',
])
def test_shared_literal_rules_cover_real_company_regressions(block):
    xml = f"<DOCUMENT>{block}<TITLE>회계정책</TITLE><P>연결재무제표 기준입니다.</P></DOCUMENT>"
    rows = by_topic(archive_of({"filing.xml": xml}))
    assert rows["회계정책"]["status"] == "발췌 가능"
    assert "보정 후 XML 검증" in rows["회계정책"]["normalization"]


def test_reads_multiple_xml_files_and_keeps_each_passages_filename():
    payload = archive_of(
        {
            "main.xml": "<DOCUMENT><TITLE>회계정책</TITLE><P>회계정책 본문</P></DOCUMENT>",
            "attachments/audit.XML": "<DOCUMENT><TITLE>감사의견</TITLE><P>감사보고서 본문</P></DOCUMENT>",
        }
    )
    rows = by_topic(payload)
    assert rows["회계정책"]["location"].startswith("main.xml /")
    assert rows["감사의견"]["location"].startswith("attachments/audit.XML /")
    assert "감사보고서 본문" in rows["감사의견"]["excerpt"]


@pytest.mark.parametrize("filename", ["../report.xml", "/report.xml", "folder/../../report.xml", "C:\\report.xml"])
def test_rejects_unsafe_archive_paths_even_without_disk_extraction(filename):
    rows = by_topic(archive_of({filename: "<DOCUMENT><P>회계정책</P></DOCUMENT>"}))
    assert all(row["status"] == "추출 실패" for row in rows.values())
    assert all("경로" in row["location"] for row in rows.values())


def test_archive_limits_apply_before_parsing(monkeypatch):
    payload = archive_of({"report.xml": "<DOCUMENT><P>회계정책</P></DOCUMENT>"})
    monkeypatch.setattr(dart_notes, "MAX_ARCHIVE_BYTES", len(payload) - 1)
    assert all(row["status"] == "추출 실패" for row in by_topic(payload).values())


def test_member_size_limits_apply_before_reading(monkeypatch):
    payload = archive_of({"report.xml": "<DOCUMENT><P>회계정책</P></DOCUMENT>"})
    monkeypatch.setattr(dart_notes, "MAX_MEMBER_BYTES", 10)
    assert all(row["status"] == "추출 실패" for row in by_topic(payload).values())


def test_file_count_limits_apply_to_all_archive_members(monkeypatch):
    payload = archive_of({"report.xml": "<D/>", "image.png": b"a"})
    monkeypatch.setattr(dart_notes, "MAX_FILES", 1)
    assert all(row["status"] == "추출 실패" for row in by_topic(payload).values())


def test_malformed_one_of_many_documents_does_not_claim_complete_extraction():
    payload = archive_of({"good.xml": "<D><P>회계정책</P></D>", "bad.xml": "<D>"})
    assert all(row["status"] == "추출 실패" for row in by_topic(payload).values())

from datetime import date
from decimal import Decimal
from io import BytesIO
from zipfile import ZipFile

import pytest

from dart_analyst import xbrl


IFRS = "https://xbrl.ifrs.org/taxonomy/2024-03-27/ifrs-full"
AXIS = "ConsolidatedAndSeparateFinancialStatementsAxis"
CONTEXT = f"""
<x:context id="half">
  <x:entity><x:identifier scheme="urn:dart">00164742</x:identifier></x:entity>
  <x:period><x:startDate>2026-01-01</x:startDate><x:endDate>2026-06-30</x:endDate></x:period>
  <x:scenario>
    <d:explicitMember xmlns:filing="{IFRS}" dimension="filing:{AXIS}">filing:ConsolidatedMember</d:explicitMember>
  </x:scenario>
</x:context>
"""
UNIT = """
<x:unit id="won"><x:measure xmlns:money="http://www.xbrl.org/2003/iso4217">money:KRW</x:measure></x:unit>
"""
FACT = '<f:ProfitLoss contextRef="half" unitRef="won" decimals="-6">5472888000000</f:ProfitLoss>'


def document(body: str) -> str:
    return (f'<x:xbrl xmlns:x="http://www.xbrl.org/2003/instance" '
            f'xmlns:d="http://xbrl.org/2006/xbrldi" xmlns:f="{IFRS}">{body}</x:xbrl>')


def zipped(xml: str, *, name="reports/unknown-name.xbrl", extra=None) -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w") as archive:
        archive.writestr(name, xml)
        for filename, content in (extra or {}).items():
            archive.writestr(filename, content)
    return buffer.getvalue()


def test_keeps_numeric_fact_and_namespace_resolved_context():
    result = xbrl.read_xbrl_archive(zipped(document(CONTEXT + UNIT + FACT), extra={"ignored_pre.xml": "not parsed"}))
    fact, = result.facts
    assert fact.concept == f"{{{IFRS}}}ProfitLoss"
    assert fact.value == Decimal("5472888000000")
    assert fact.decimals == "-6"
    assert (fact.context.start, fact.context.end) == (date(2026, 1, 1), date(2026, 6, 30))
    assert fact.context.identifier == "00164742"
    assert fact.context.dimensions == (
        xbrl.XbrlDimension(f"{{{IFRS}}}{AXIS}", f"{{{IFRS}}}ConsolidatedMember", "scenario"),
    )
    assert (fact.context.scope, fact.currency) == ("CFS", "KRW")


def test_local_namespace_rebinding_cannot_impersonate_consolidation():
    ctx = CONTEXT.replace(f'xmlns:filing="{IFRS}"', 'xmlns:filing="urn:untrusted"')
    fact, = xbrl.read_xbrl_archive(zipped(document(ctx + UNIT + FACT))).facts
    assert fact.context.scope is None


def test_preserves_duplicates_and_marks_typed_context_as_qualified():
    ctx = CONTEXT.replace("</x:scenario>", '<d:typedMember dimension="f:CustomAxis"><f:Label>data</f:Label></d:typedMember></x:scenario>')
    second = FACT.replace("5472888000000", "1")
    facts = xbrl.read_xbrl_archive(zipped(document(ctx + UNIT + FACT + second))).facts
    assert [f.value for f in facts] == [Decimal("5472888000000"), Decimal("1")]
    assert all(f.context.has_other_content for f in facts)


@pytest.mark.parametrize("payload", [
    b"not a zip",
    zipped(document(""), name="../unsafe.xbrl"),
    zipped(document(""), extra={"second.xbrl": document("")}),
    zipped('<!DOCTYPE x:xbrl [<!ENTITY bad SYSTEM "file:///not-read">]>' + document("&bad;")),
    zipped(document(CONTEXT + CONTEXT + UNIT + FACT)),
    zipped(document(CONTEXT + UNIT + FACT.replace('unitRef="won"', 'unitRef="missing"'))),
    zipped(document(CONTEXT + UNIT + FACT.replace("5472888000000", "NaN"))),
])
def test_rejects_unsafe_or_ambiguous_input(payload):
    with pytest.raises(xbrl.XbrlError):
        xbrl.read_xbrl_archive(payload)


def test_member_limit_applies_to_ignored_members(monkeypatch):
    monkeypatch.setattr(xbrl, "_MAX_MEMBER_BYTES", 500)
    with pytest.raises(xbrl.XbrlError, match="크기 한도"):
        xbrl.read_xbrl_archive(zipped(document(""), extra={"linkbase.xml": "x" * 501}))


@pytest.mark.parametrize("label_file", ["anything_lab-ko.xml", "labels/lab_00123456-ko_2011-04-29.xml"])
def test_extension_labels_resolve_actual_schema_ids_without_guessing_names(label_file):
    namespace = "http://dart.fss.or.kr/taxonomy/2026-06-30/entity00123456"
    schema = f"""<schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="{namespace}">
      <element id="arbitrary-id" name="OwnerMovement"/></schema>"""
    labels = """<linkbase xmlns="http://www.xbrl.org/2003/linkbase" xmlns:x="http://www.w3.org/1999/xlink">
      <labelLink><loc x:label="source" x:href="model.xsd#arbitrary-id"/>
      <label x:label="text" x:role="http://www.xbrl.org/2003/role/label" xml:lang="ko">소유주와의 거래 합계</label>
      <labelArc x:from="source" x:to="text"/></labelLink></linkbase>"""
    payload = zipped(document(CONTEXT + UNIT + FACT), extra={"model.xsd": schema, label_file: labels.replace("model.xsd#", "../model.xsd#" if "/" in label_file else "model.xsd#")})
    result = xbrl.read_xbrl_archive(payload)
    assert result.labels == {f"{{{namespace}}}OwnerMovement": ("소유주와의 거래 합계",)}
    assert len(result.facts) == 1
    assert not result.label_error


def test_invalid_optional_labels_preserve_standard_numeric_facts():
    result = xbrl.read_xbrl_archive(zipped(document(CONTEXT + UNIT + FACT), extra={"anything_lab-ko.xml": "<broken>"}))
    assert len(result.facts) == 1
    assert result.labels == {}
    assert result.label_error

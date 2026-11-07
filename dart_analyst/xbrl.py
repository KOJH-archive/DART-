"""Read one OpenDART XBRL instance in memory without selecting accounting facts."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from io import BytesIO
from pathlib import PurePosixPath
import re
import stat
from urllib.parse import urlparse
from xml.etree.ElementTree import Element
from zipfile import BadZipFile, ZipFile
from zlib import error as ZlibError

from defusedxml import ElementTree
from defusedxml.common import DefusedXmlException

_XBRLI = "{http://www.xbrl.org/2003/instance}"
_XBRLDI = "{http://xbrl.org/2006/xbrldi}"
_XSI_NIL = "{http://www.w3.org/2001/XMLSchema-instance}nil"
_ISO4217 = "{http://www.xbrl.org/2003/iso4217}"
_IFRS = re.compile(r"\{https?://xbrl\.ifrs\.org/taxonomy/\d{4}-\d{2}-\d{2}/ifrs-full\}")
_DART = re.compile(r"\{https?://dart\.fss\.or\.kr/taxonomy/\d{4}-\d{2}-\d{2}/ifrs/dart\}")
DART_IDENTIFIER_SCHEME = "http://dart.fss.or.kr/ifrs/CIK"
_MAX_ZIP_BYTES = 30 * 1024 * 1024
_MAX_MEMBER_BYTES = 20 * 1024 * 1024
_MAX_TOTAL_BYTES = 60 * 1024 * 1024
_MAX_FILES = 100
_MAX_XML_NODES = 300_000
_MAX_XML_DEPTH = 128
_NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE]([+-]?[0-9]{1,3}))?")
_NCNAME = re.compile(r"[^\W\d][\w.-]*")


class XbrlError(ValueError):
    """The archive or instance cannot be safely interpreted."""


@dataclass(frozen=True)
class XbrlDimension:
    axis: str
    member: str
    location: str


@dataclass(frozen=True)
class XbrlContext:
    identifier: str
    identifier_scheme: str
    start: date | None
    end: date | None
    instant: date | None
    dimensions: tuple[XbrlDimension, ...]
    has_other_content: bool

    @property
    def scope(self) -> str | None:
        for item in self.dimensions:
            namespace = _IFRS.match(item.axis)
            if namespace is None:
                continue
            prefix = namespace.group()
            if item.axis != prefix + "ConsolidatedAndSeparateFinancialStatementsAxis":
                continue
            if item.member == prefix + "ConsolidatedMember":
                return "CFS"
            if item.member == prefix + "SeparateMember":
                return "OFS"
        return None


@dataclass(frozen=True)
class XbrlFact:
    concept: str
    context_id: str
    context: XbrlContext
    unit: str
    value: Decimal
    decimals: str | None
    precision: str | None

    @property
    def rounding_unit(self) -> Decimal:
        if self.decimals == "INF":
            return Decimal(0)
        if self.decimals is not None and re.fullmatch(r"[+-]?\d{1,3}", self.decimals):
            places = int(self.decimals)
            if abs(places) <= 20:
                return Decimal(10) ** -places
        return Decimal(0)

    @property
    def standard_account_id(self) -> str | None:
        for pattern, prefix in ((_IFRS, "ifrs-full_"), (_DART, "dart_")):
            if namespace := pattern.match(self.concept):
                return prefix + self.concept[namespace.end():]
        return None

    @property
    def currency(self) -> str | None:
        code = self.unit.removeprefix(_ISO4217)
        return code if self.unit.startswith(_ISO4217) and re.fullmatch(r"[A-Z]{3}", code) else None


@dataclass(frozen=True)
class XbrlInstance:
    member_name: str
    facts: tuple[XbrlFact, ...]
    labels: dict[str, tuple[str, ...]] = field(default_factory=dict)
    label_sources: tuple[str, ...] = ()
    label_error: str = ""


def _read_instance(payload: bytes) -> tuple[str, bytes, dict[str, bytes]]:
    if not isinstance(payload, bytes) or len(payload) > _MAX_ZIP_BYTES:
        raise XbrlError("XBRL ZIP 형식 또는 크기가 허용 범위를 벗어났습니다.")
    try:
        with ZipFile(BytesIO(payload)) as archive:
            members = archive.infolist()
            if len(members) > _MAX_FILES or sum(info.file_size for info in members) > _MAX_TOTAL_BYTES:
                raise XbrlError("XBRL ZIP의 파일 개수 또는 압축 해제 크기가 허용 한도를 넘었습니다.")
            seen = set()
            instances = []
            for info in members:
                name = info.orig_filename.replace("\\", "/")
                path = PurePosixPath(name)
                if (not name or "\x00" in name or path.is_absolute() or ".." in path.parts
                        or ":" in name or str(path).casefold() in seen
                        or stat.S_IFMT(info.external_attr >> 16) == stat.S_IFLNK or info.flag_bits & 1):
                    raise XbrlError("XBRL ZIP에 허용되지 않은 파일 항목이 있습니다.")
                seen.add(str(path).casefold())
                if info.file_size > _MAX_MEMBER_BYTES:
                    raise XbrlError("XBRL ZIP 내부 파일이 크기 한도를 넘었습니다.")
                if not info.is_dir() and path.suffix.lower() == ".xbrl":
                    instances.append(info)
            if len(instances) != 1:
                raise XbrlError("단일 .xbrl 인스턴스를 식별할 수 없습니다.")
            with archive.open(instances[0]) as stream:
                content = stream.read(_MAX_MEMBER_BYTES + 1)
            if len(content) > _MAX_MEMBER_BYTES:
                raise XbrlError("XBRL 인스턴스가 크기 한도를 넘었습니다.")
            related = {}
            for info in members:
                if (info.filename.lower().endswith((".xsd", "_lab-ko.xml"))
                        or re.fullmatch(r"lab_[\w.-]+-ko_\d{4}-\d{2}-\d{2}\.xml", PurePosixPath(info.filename).name.lower())):
                    with archive.open(info) as stream:
                        document = stream.read(_MAX_MEMBER_BYTES + 1)
                    if len(document) > _MAX_MEMBER_BYTES:
                        raise XbrlError("XBRL 보조 문서가 크기 한도를 넘었습니다.")
                    related[info.filename] = document
            return instances[0].filename, content, related
    except (BadZipFile, OSError, EOFError, RuntimeError, ZlibError) as exc:
        raise XbrlError("XBRL ZIP을 안전하게 읽을 수 없습니다.") from exc


def _qname(text: str, namespaces: dict[str, str]) -> str:
    prefix, separator, local = text.strip().partition(":")
    if not separator:
        prefix, local = "", prefix
    if not _NCNAME.fullmatch(local) or (separator and not _NCNAME.fullmatch(prefix)):
        raise XbrlError("XBRL QName 형식이 올바르지 않습니다.")
    namespace = namespaces.get(prefix)
    if prefix and not namespace:
        raise XbrlError("XBRL QName 네임스페이스를 찾을 수 없습니다.")
    return f"{{{namespace}}}{local}" if namespace else local


def _parse_xml(content: bytes, expected_root: str = _XBRLI + "xbrl") -> tuple[Element, dict[Element, tuple[str, ...]]]:
    namespaces: dict[str, str] = {"xml": "http://www.w3.org/XML/1998/namespace"}
    pending: list[tuple[str, str]] = []
    scopes: list[list[tuple[str, str | None]]] = []
    qualified: dict[Element, tuple[str, ...]] = {}
    events = ElementTree.iterparse(BytesIO(content), events=("start-ns", "start", "end"),
                                    forbid_dtd=True, forbid_entities=True, forbid_external=True)
    nodes = 0
    try:
        for event, value in events:
            if event == "start-ns":
                pending.append(value)
            elif event == "start":
                nodes += 1
                if nodes > _MAX_XML_NODES or len(scopes) >= _MAX_XML_DEPTH:
                    raise XbrlError("XBRL XML 구조가 허용 한도를 넘었습니다.")
                previous = [(prefix, namespaces.get(prefix)) for prefix, _ in pending]
                scopes.append(previous)
                namespaces.update(pending)
                pending.clear()
            else:
                if value.tag == _XBRLDI + "explicitMember":
                    qualified[value] = (_qname(value.get("dimension", ""), namespaces),
                                        _qname(value.text or "", namespaces))
                elif value.tag == _XBRLI + "measure":
                    qualified[value] = (_qname(value.text or "", namespaces),)
                for prefix, old in scopes.pop():
                    if old is None:
                        namespaces.pop(prefix, None)
                    else:
                        namespaces[prefix] = old
    except (DefusedXmlException, ElementTree.ParseError, LookupError) as exc:
        raise XbrlError("XBRL XML을 안전하게 읽을 수 없습니다.") from exc
    if events.root is None or events.root.tag != expected_root:
        raise XbrlError("XBRL 인스턴스 루트가 올바르지 않습니다.")
    return events.root, qualified


def _read_labels(documents: dict[str, bytes]) -> dict[str, tuple[str, ...]]:
    schema_ns = "{http://www.w3.org/2001/XMLSchema}"
    link_ns = "{http://www.xbrl.org/2003/linkbase}"
    xlink = "{http://www.w3.org/1999/xlink}"
    concepts = {}
    schema_names = set()
    for filename, content in documents.items():
        if not filename.lower().endswith(".xsd"):
            continue
        name = PurePosixPath(filename).name
        if name in schema_names:
            raise XbrlError("XBRL 스키마 파일명을 유일하게 식별할 수 없습니다.")
        schema_names.add(name)
        root, _ = _parse_xml(content, schema_ns + "schema")
        namespace = root.get("targetNamespace", "")
        for element in root.findall(schema_ns + "element"):
            identifier, local = element.get("id"), element.get("name")
            if identifier and local and _NCNAME.fullmatch(local) and namespace:
                if (name, identifier) in concepts:
                    raise XbrlError("XBRL 스키마 요소 ID가 중복되었습니다.")
                concepts[(name, identifier)] = f"{{{namespace}}}{local}"
    labels: dict[str, set[str]] = {}
    for filename, content in documents.items():
        if filename.lower().endswith(".xsd"):
            continue
        root, _ = _parse_xml(content, link_ns + "linkbase")
        for link in root.findall(link_ns + "labelLink"):
            locators = {}
            resources = {}
            for element in link:
                label = element.get(xlink + "label", "")
                if element.tag == link_ns + "loc":
                    href = urlparse(element.get(xlink + "href", ""))
                    concept = concepts.get((PurePosixPath(href.path).name, href.fragment))
                    if concept:
                        if label in locators and locators[label] != concept:
                            raise XbrlError("XBRL 라벨의 개념 참조가 중복되었습니다.")
                        locators[label] = concept
                elif (element.tag == link_ns + "label"
                      and element.get("{http://www.w3.org/XML/1998/namespace}lang", "").startswith("ko")
                      and element.get(xlink + "role") == "http://www.xbrl.org/2003/role/label"):
                    text = " ".join("".join(element.itertext()).split())
                    if 0 < len(text) <= 160:
                        resources.setdefault(label, set()).add(text)
                        if len(resources[label]) > 1:
                            raise XbrlError("XBRL 기본 라벨 자원이 중복되었습니다.")
            for arc in link.findall(link_ns + "labelArc"):
                concept = locators.get(arc.get(xlink + "from", ""))
                if concept:
                    labels.setdefault(concept, set()).update(resources.get(arc.get(xlink + "to", ""), ()))
    return {concept: tuple(sorted(texts)) for concept, texts in labels.items()}


def _read_date(element: Element) -> date:
    raw = (element.text or "").strip()
    result = date.fromisoformat(raw)
    if len(element) or raw != result.isoformat():
        raise ValueError
    return result


def _context(element: Element, qualified: dict[Element, tuple[str, ...]]) -> XbrlContext:
    entities = element.findall(_XBRLI + "entity")
    periods = element.findall(_XBRLI + "period")
    if len(entities) != 1 or len(periods) != 1:
        raise XbrlError("XBRL 문맥에서 회사 또는 기간이 누락되거나 중복되었습니다.")
    entity, period = entities[0], periods[0]
    identifiers = entity.findall(_XBRLI + "identifier")
    if len(identifiers) != 1:
        raise XbrlError("XBRL 회사 식별자가 누락되거나 중복되었습니다.")
    identifier = identifiers[0]
    code = (identifier.text or "").strip()
    scheme = identifier.get("scheme", "").strip()
    if not code or not scheme or len(identifier):
        raise XbrlError("XBRL 회사 식별자가 올바르지 않습니다.")
    tags = tuple(node.tag for node in period)
    try:
        start = end = instant = None
        if tags == (_XBRLI + "startDate", _XBRLI + "endDate"):
            start, end = map(_read_date, period)
            if start > end:
                raise ValueError
        elif tags == (_XBRLI + "instant",):
            instant = _read_date(period[0])
        elif tags != (_XBRLI + "forever",) or len(period[0]) or (period[0].text or "").strip():
            raise ValueError
    except ValueError as exc:
        raise XbrlError("XBRL 문맥 기간이 올바르지 않습니다.") from exc
    dimensions = []
    axes = set()
    other = (any(child.tag not in {_XBRLI + tag for tag in ("entity", "period", "scenario")} for child in element)
             or any(child.tag not in {_XBRLI + tag for tag in ("identifier", "segment")} for child in entity))
    for parent, location in ((entity, "segment"), (element, "scenario")):
        containers = parent.findall(_XBRLI + location)
        if len(containers) > 1:
            raise XbrlError("XBRL 문맥에 같은 차원 컨테이너가 중복되었습니다.")
        for container in containers:
            for child in container:
                if child.tag != _XBRLDI + "explicitMember" or len(child):
                    other = True
                    continue
                axis, member = qualified[child]
                if axis in axes:
                    raise XbrlError("XBRL 문맥에 같은 축이 중복되었습니다.")
                axes.add(axis)
                dimensions.append(XbrlDimension(axis, member, location))
    return XbrlContext(code, scheme, start, end, instant,
                       tuple(sorted(dimensions, key=lambda item: item.axis)), other)


def read_xbrl_archive(payload: bytes) -> XbrlInstance:
    """Return top-level, single-measure numeric facts with original provenance.

    Nil facts, text and compound units are outside this reader's numeric scope.
    Unrecognized context content is flagged; callers must not treat such a
    context as an unqualified total. Facts are kept individually, including
    duplicates and conflicts. No schema or linkbase reference is fetched.
    """
    name, content, related = _read_instance(payload)
    root, qualified = _parse_xml(content)
    contexts: dict[str, XbrlContext] = {}
    units: dict[str, str | None] = {}
    for element in root:
        if element.tag == _XBRLI + "context":
            context_id = element.get("id", "")
            if not context_id or context_id in contexts:
                raise XbrlError("XBRL 문맥 ID가 누락되거나 중복되었습니다.")
            contexts[context_id] = _context(element, qualified)
        elif element.tag == _XBRLI + "unit":
            unit_id = element.get("id", "")
            if not unit_id or unit_id in units:
                raise XbrlError("XBRL 단위 ID가 누락되거나 중복되었습니다.")
            is_simple = len(element) == 1 and element[0].tag == _XBRLI + "measure" and not len(element[0])
            units[unit_id] = qualified[element[0]][0] if is_simple else None
    facts = []
    for element in root:
        unit_id = element.get("unitRef")
        if unit_id is None or element.get(_XSI_NIL) in {"true", "1"}:
            continue
        context_id = element.get("contextRef", "")
        if context_id not in contexts or unit_id not in units:
            raise XbrlError("XBRL 사실의 문맥 또는 단위 참조가 존재하지 않습니다.")
        unit = units[unit_id]
        if unit is None:
            continue
        raw_value = (element.text or "").strip()
        number = _NUMBER.fullmatch(raw_value) if len(raw_value) <= 128 and not len(element) else None
        if number is None or abs(int(number[1] or "0")) > 99:
            raise XbrlError("XBRL 수치의 형식 또는 정밀도가 허용 범위를 벗어났습니다.")
        facts.append(XbrlFact(element.tag, context_id, contexts[context_id], unit,
                             Decimal(raw_value), element.get("decimals"), element.get("precision")))
    try:
        labels = _read_labels(related)
        label_error = ""
    except XbrlError as exc:
        labels = {}
        label_error = str(exc)
    return XbrlInstance(name, tuple(facts), labels, tuple(related), label_error)

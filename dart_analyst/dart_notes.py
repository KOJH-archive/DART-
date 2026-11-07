"""Bounded extraction of passages from a DART original-document archive.

This module locates text; it does not determine an audit opinion or conclude
that a financial risk exists (or does not exist).  A missing passage always
requires checking the original filing.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import PurePosixPath
import re
import stat
from xml.etree.ElementTree import Element
from zipfile import BadZipFile, ZipFile
from zlib import error as ZlibError

from defusedxml import ElementTree
from defusedxml.common import DefusedXmlException


MAX_ARCHIVE_BYTES = 30 * 1024 * 1024
# A verified bank half-year original is 21,282,590 bytes. Keep a bounded
# document allowance independent from the unchanged node/text/total limits.
MAX_MEMBER_BYTES = 30 * 1024 * 1024
MAX_TOTAL_UNCOMPRESSED_BYTES = 60 * 1024 * 1024
MAX_FILES = 100
MAX_XML_NODES = 300_000
MAX_TEXT_CHARACTERS = 8_000_000
MAX_EXCERPT_CHARACTERS = 600
MAX_LITERAL_REPAIRS = 2_048

# Deliberately do not expand these into inferred synonyms such as
# "관계기업", which is not equivalent to a related-party transaction note.
_TOPICS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("회계정책", (r"회계\s*정책",)),
    ("차입금·유동성", (r"차입금", r"차입\s*부채", r"유동성")),
    ("우발채무·약정", (r"우발\s*채무", r"우발\s*부채", r"약정\s*사항", r"약정")),
    ("특수관계자", (r"특수\s*관계자",)),
    ("감사의견", (r"감사\s*의견", r"감사인의\s*의견", r"독립된\s*감사인의\s*감사보고서",
              r"외부\s*감사에\s*관한\s*사항")),
)
_OPERATING_TOPICS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("사업부문·수익구조", (r"영업\s*부문", r"사업\s*부문", r"부문별\s*정보", r"매출의?\s*구성")),
    ("원가·운전자본", (r"매출\s*원가", r"원재료.*가격", r"재고.*평가", r"운전\s*자본")),
)

_BLOCK_TAGS = {"P", "TD", "TH", "TE", "TITLE", "SUBTITLE", "TITLE1", "TITLE2", "TITLE3", "TITLE4"}

# Some DART XML has bare ampersands in text and attributes, plus angle-wrapped
# Korean captions in table cells and paragraphs. Leave markup and reference-like
# strings to the strict parser. Preserve comments, CDATA and instructions.
_XML_OPAQUE_SECTIONS = re.compile(
    r"(<!--.*?(?:-->|\Z)|<!\[CDATA\[.*?(?:\]\]>|\Z)|<\?.*?(?:\?>|\Z))", re.DOTALL
)
_BARE_AMPERSAND = re.compile(r"""&(?!#|[^\s<>&;"']+;)""")
# Tokenize markup and text separately. XML declarations, comments and CDATA
# remain opaque. Only short prose in a DART text block can become a literal.
_XML_TOKEN = re.compile(r"""<(?:[^<>"']|"[^"]*"|'[^']*')*>|[^<]+|<""", re.DOTALL)
_XML_NAME = re.compile(r"</?([A-Za-z_][A-Za-z0-9_.:-]*)(?=[\s/>])")
_LITERAL_CAPTION = re.compile(r"[\u3131-\u318e\uac00-\ud7a3]|^[A-Z][a-z][A-Za-z-]*[ \t]+[A-Za-z]|^\d[\d .:/()_-]*$")
_DART_ENG_QUOTES = re.compile(r'\bENG=""([^<>"=]{1,160})""(?=\s+[A-Z_]+=|/?>)')
_DART_ENG_TRAILING_QUOTE = re.compile(
    r'(<(?:TE|TD|TH)\b[^<>]*?\bENG=")([^<>"\r\n]{1,160})""(?=\s+[A-Z_]+=|/?>)'
)

@dataclass(frozen=True)
class _Segment:
    text: str
    filename: str
    path: str
    heading: bool
    normalized: bool = False


class _ExtractionError(ValueError):
    pass


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _local_name(tag: object) -> str:
    if not isinstance(tag, str):
        return ""
    return tag.rsplit("}", 1)[-1].upper()


def _validate_member_name(name: str) -> None:
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    if (
        not normalized
        or "\x00" in normalized
        or path.is_absolute()
        or ".." in path.parts
        or re.match(r"^[A-Za-z]:", normalized)
    ):
        raise _ExtractionError("압축파일에 허용되지 않은 경로가 있습니다.")


def _read_documents(payload: bytes) -> list[tuple[str, bytes]]:
    if len(payload) > MAX_ARCHIVE_BYTES:
        raise _ExtractionError("원문 압축파일의 크기가 허용 한도를 넘었습니다.")
    try:
        with ZipFile(BytesIO(payload)) as archive:
            members = archive.infolist()
            if len(members) > MAX_FILES:
                raise _ExtractionError("압축파일의 파일 개수가 허용 한도를 넘었습니다.")
            uncompressed = 0
            documents = []
            for member in members:
                _validate_member_name(member.filename)
                if stat.S_IFMT(member.external_attr >> 16) == stat.S_IFLNK:
                    raise _ExtractionError("압축파일의 심볼릭 링크는 처리하지 않습니다.")
                if member.flag_bits & 1:
                    raise _ExtractionError("암호화된 원문 압축파일은 처리하지 않습니다.")
                if member.file_size > MAX_MEMBER_BYTES:
                    raise _ExtractionError("압축파일 내부 문서의 크기가 허용 한도를 넘었습니다.")
                uncompressed += member.file_size
                if uncompressed > MAX_TOTAL_UNCOMPRESSED_BYTES:
                    raise _ExtractionError("압축 해제 후 전체 크기가 허용 한도를 넘었습니다.")
                if member.is_dir() or not member.filename.lower().endswith(".xml"):
                    continue
                with archive.open(member) as stream:
                    content = stream.read(MAX_MEMBER_BYTES + 1)
                if len(content) > MAX_MEMBER_BYTES:
                    raise _ExtractionError("압축파일 내부 문서의 크기가 허용 한도를 넘었습니다.")
                documents.append((member.filename, content))
            if not documents:
                raise _ExtractionError("압축파일에서 XML 원문을 찾지 못했습니다.")
            return documents
    except _ExtractionError:
        raise
    except (BadZipFile, OSError, EOFError, RuntimeError, ValueError, ZlibError) as exc:
        raise _ExtractionError("원문 압축파일을 안전하게 읽지 못했습니다.") from exc


def _escape_dart_literals(content: bytes) -> bytes | None:
    parts = _XML_OPAQUE_SECTIONS.split(content.decode("utf-8"))
    stack: list[str] = []
    repairs = 0

    def record_repair() -> None:
        nonlocal repairs
        repairs += 1
        if repairs > MAX_LITERAL_REPAIRS:
            raise _ExtractionError("XML 원문의 문자 보정 횟수가 허용 한도를 넘었습니다.")

    def escape_ampersand(_match: re.Match[str]) -> str:
        record_repair()
        return "&amp;"

    def repair_eng(value: re.Match[str]) -> str:
        record_repair()
        return 'ENG="&quot;' + value[1] + '&quot;"'

    def repair_eng_trailing(value: re.Match[str]) -> str:
        record_repair()
        return value[1] + value[2] + '&quot;"'

    for index in range(0, len(parts), 2):
        # An unmatched trailing quote prevents tokenization of the whole tag.
        # Repair only the observed ENG attribute in DART table-cell markup.
        parts[index] = _DART_ENG_TRAILING_QUOTE.sub(repair_eng_trailing, parts[index])
        normalized = []
        for match in _XML_TOKEN.finditer(parts[index]):
            token = match[0]
            if token.startswith(("<TE ", "<TD ", "<TH ")):
                token = _DART_ENG_QUOTES.sub(repair_eng, token)
            inside_text = any(tag.upper() in _BLOCK_TAGS | {"SPAN"} for tag in stack)
            caption = token[1:-1] if token.startswith("<") and token.endswith(">") else ""
            is_literal = (inside_text and 0 < len(caption) <= 160
                          and not any(char in caption for char in '=\'"!?')
                          and bool(_LITERAL_CAPTION.search(caption)))
            bare_literal = False
            if token == "<" and inside_text:
                tail = parts[index][match.end():match.end() + 161]
                bare_literal = tail.startswith("<") or bool(re.match(r"[가-힣][^<>='\"]{0,159}(?=<)", tail))
            if bare_literal:
                record_repair()
                token = "&lt;"
            elif is_literal:
                record_repair()
                token = "&lt;" + caption + "&gt;"
            elif name := _XML_NAME.match(token):
                tag = name[1]
                if token.startswith("</"):
                    if stack and stack[-1] == tag:
                        stack.pop()
                elif not token.endswith("/>"):
                    stack.append(tag)
            normalized.append(_BARE_AMPERSAND.sub(escape_ampersand, token))
        parts[index] = "".join(normalized)
    return "".join(parts).encode("utf-8") if repairs else None

def _parse_document_xml(content: bytes) -> Element:
    restrictions = dict(forbid_dtd=True, forbid_entities=True, forbid_external=True)
    try:
        return ElementTree.fromstring(content, **restrictions)
    except ElementTree.ParseError:
        repaired = _escape_dart_literals(content)
        if repaired is None:
            raise
        root = ElementTree.fromstring(repaired, **restrictions)
        root.set("_dart_literal_normalization", "true")
        return root


def _document_segments(filename: str, content: bytes) -> list[_Segment]:
    try:
        root = _parse_document_xml(content)
    except _ExtractionError:
        raise
    except (DefusedXmlException, ElementTree.ParseError, LookupError, ValueError) as exc:
        raise _ExtractionError("XML 원문을 안전하게 해석하지 못했습니다.") from exc

    node_count = 0
    for _ in root.iter():
        node_count += 1
        if node_count > MAX_XML_NODES:
            raise _ExtractionError("XML 원문의 구조가 허용 한도를 넘었습니다.")

    segments: list[_Segment] = []
    characters = 0

    def append(text: str | None, path: str, heading: bool = False) -> None:
        nonlocal characters
        normalized = _normalize(text or "")
        if normalized:
            characters += len(normalized)
            if characters > MAX_TEXT_CHARACTERS:
                raise _ExtractionError("XML 원문의 텍스트가 허용 한도를 넘었습니다.")
            segments.append(_Segment(normalized, filename, path, heading,
                                     root.get("_dart_literal_normalization") == "true"))

    # Iterative traversal avoids Python recursion limits on deeply nested XML.
    stack: list[tuple[Element, str, bool]] = [(root, _local_name(root.tag) or "ROOT", False)]
    while stack:
        element, path, tail_only = stack.pop()
        if tail_only:
            append(element.tail, f"{path}/tail")
            continue
        tag = _local_name(element.tag)
        if tag in _BLOCK_TAGS:
            # itertext preserves words split across inline markup and avoids
            # counting the same paragraph once per ancestor element.
            append("".join(element.itertext()), path, tag.startswith("TITLE") or tag == "SUBTITLE")
            continue
        append(element.text, path)
        children = list(element)
        ordinals: dict[str, int] = {}
        positioned = []
        for child in children:
            child_tag = _local_name(child.tag) or "NODE"
            ordinals[child_tag] = ordinals.get(child_tag, 0) + 1
            child_path = f"{path}/{child_tag}[{ordinals[child_tag]}]"
            positioned.append((child, child_path))
        for child, child_path in reversed(positioned):
            stack.append((child, child_path, True))
            stack.append((child, child_path, False))
    return segments


def _excerpt(segments: list[_Segment], index: int, match_start: int) -> str:
    chosen = segments[index]
    start = max(0, match_start - 100) if not chosen.heading else 0
    fragments = [chosen.text[start:]]
    length = len(fragments[0])
    for following in segments[index + 1 :]:
        if following.filename != chosen.filename or following.heading:
            break
        if length >= MAX_EXCERPT_CHARACTERS:
            break
        fragments.append(following.text)
        length += len(following.text) + 1
    excerpt = " ".join(fragments)
    if len(excerpt) > MAX_EXCERPT_CHARACTERS:
        excerpt = excerpt[: MAX_EXCERPT_CHARACTERS - 1].rstrip() + "…"
    return excerpt


def _failures(source_id: str, source_url: str, message: str) -> list[dict]:
    return [
        {
            "topic": topic,
            "status": "추출 실패",
            "excerpt": "",
            "source_id": source_id,
            "source_url": source_url,
            "location": message,
        }
        for topic, _ in _TOPICS
    ]


def parse_note_topics(payload: bytes, source_id: str, source_url: str, *, include_operating_context: bool = False) -> list[dict]:
    """Return five evidence passages, or explicit manual-review/failure states.

    ``발췌 가능`` means only that a related passage was located.  It is never a
    determination that the passage is complete, the accounts are correct, the
    audit opinion is unqualified, or a risk is absent.  No archive member is
    extracted to disk and no network/entity reference is resolved.
    """
    if not isinstance(payload, bytes):
        return _failures(source_id, source_url, "원문 응답이 바이트 형식이 아닙니다.")
    try:
        documents = _read_documents(payload)
        segments = []
        for filename, content in documents:
            segments.extend(_document_segments(filename, content))
        if not segments:
            raise _ExtractionError("XML 원문에서 분석할 텍스트를 찾지 못했습니다.")
    except _ExtractionError as exc:
        return _failures(source_id, source_url, str(exc))

    results = []
    for topic, patterns in _TOPICS + (_OPERATING_TOPICS if include_operating_context else ()):
        pattern = re.compile("|".join(f"(?:{item})" for item in patterns))
        candidates = []
        heading_without_body = False
        for index, segment in enumerate(segments):
            match = pattern.search(segment.text)
            if match:
                if segment.heading:
                    following = segments[index + 1] if index + 1 < len(segments) else None
                    if not following or following.heading or following.filename != segment.filename:
                        heading_without_body = True
                        continue
                candidates.append((not segment.heading, index, match.start()))
        base = {"topic": topic, "source_id": source_id, "source_url": source_url}
        if not candidates:
            results.append(
                {
                    **base,
                    "status": "원문 확인 필요",
                    "excerpt": "",
                    "location": ("관련 제목만 찾았으며 본문은 원문 확인 필요" if heading_without_body
                                 else "자동 탐색에서 해당 절을 찾지 못함"),
                }
            )
            continue
        _, index, match_start = min(candidates)
        chosen = segments[index]
        results.append(
            {
                **base,
                "status": "발췌 가능",
                "excerpt": _excerpt(segments, index, match_start),
                "location": f"{chosen.filename} / {chosen.path}",
                "normalization": "본문의 꺾쇠 문구·앰퍼샌드 보정 후 XML 검증" if chosen.normalized else "원본 XML 검증",
            }
        )
    return results

"""Display-only formatting for the accounting workbench.

The engine owns calculations and comparability. These helpers only format its
reported values; they never replace missing inputs or calculate a new ratio.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext
from typing import Iterable

import pandas as pd


STATUS_LABELS = {
    'calculated': '산출 완료',
    'partial': '일부 자료',
    'missing_source': '자료 부족',
    'missing_current': '당기 자료 없음',
    'missing_previous': '비교 자료 없음',
    'mapping_pending': '계정 확인 필요',
    'invalid_denominator': '분모 확인 필요',
    'invalid_amount': '금액 확인 필요',
    'not_comparable': '비교 기준 불일치',
    'not_applicable': '산출 대상 아님',
    'duplicate': '중복 계정',
    'context_changed': '계정 문맥 변경',
    'pass': '일치',
    'fail': '불일치',
    'incomplete': '자료 부족',
    'complete': '처리 완료',
    'complete_for_supported_identities': '지원 계정 비교 완료',
}


def _decimal(value) -> Decimal | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        n = Decimal(str(value))
        return n if n.is_finite() else None
    except (InvalidOperation, ValueError, TypeError):
        return None


def _format(value: Decimal, *, exact=False, signed=False) -> str:
    with localcontext() as context:
        context.prec = max(64, len(value.as_tuple().digits) + abs(value.adjusted()) + 4)
        rounded = value if exact else value.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        if rounded == 0:
            rounded = abs(rounded)
        text = format(rounded, ',f')
    if '.' in text:
        text = text.rstrip('0').rstrip('.')
    return ('+' if signed and rounded > 0 else '') + text


def amount(value, unit: str | None = 'KRW', compact: bool = True) -> str:
    """Format reported values without floats; exact mode retains all decimals.

    KRW compact mode uses 억 for normal balances. Sub-million balances keep 원
    so a nonzero amount is never displayed as zero merely due to conversion.
    A missing currency stays explicitly unconfirmed rather than assuming KRW.
    """
    n = _decimal(value)
    if n is None:
        return '—'
    if unit in {'KRW', '원'}:
        if compact and (n == 0 or abs(n) >= Decimal('1000000')):
            with localcontext() as context:
                context.prec = max(64, len(n.as_tuple().digits) + abs(n.adjusted()) + 4)
                return _format(n / Decimal('100000000')) + '억'
        return _format(n, exact=True) + '원'
    if unit in {'%', '배', '일'}:
        return _format(n, exact=not compact) + unit
    if unit == '':
        return _format(n, exact=not compact)
    if not unit:
        return _format(n, exact=True) + ' (통화 미확인)'
    return _format(n, exact=not compact) + ' ' + unit


def change_label(comparison: dict | None) -> str | None:
    """Use only a comparable reported percent with a positive prior value."""
    if not comparison or comparison.get('status') != 'calculated':
        return None
    previous = _decimal(comparison.get('previous'))
    pct = _decimal(comparison.get('pct'))
    if previous is None or previous <= 0 or pct is None:
        return None
    return _format(pct, signed=True) + '%'


def _status(row: dict) -> str:
    return STATUS_LABELS.get(row.get('status'), '확인 필요')


def _sources(row: dict) -> str:
    source = row.get('source_ids') or []
    if isinstance(source, str):
        return source
    return ', '.join(dict.fromkeys(str(x) for x in source if x)) or '—'


def _percent(row: dict) -> str:
    label = change_label(row)
    return label if label is not None else '—'


def comparison_frame(rows: Iterable[dict]) -> pd.DataFrame:
    columns = ['계정', '비교기간', '당기', '비교금액', '당기금액', '증감액', '증감률', '상태', '확인사항', '공시']
    display = []
    for row in rows:
        currency = row.get('currency')
        display.append({
            '계정': row.get('label') or row.get('account_name') or '계정 미확인',
            '비교기간': row.get('from_period') or '—',
            '당기': row.get('to_period') or '—',
            '비교금액': amount(row.get('previous'), currency),
            '당기금액': amount(row.get('current'), currency),
            '증감액': amount(row.get('delta'), currency),
            '증감률': _percent(row),
            '상태': _status(row),
            '확인사항': row.get('reason') or '—',
            '공시': _sources(row),
        })
    return pd.DataFrame(display, columns=columns)


def metrics_frame(rows: Iterable[dict]) -> pd.DataFrame:
    columns = ['지표', '값', '상태', '산식', '확인사항', '공시']
    return pd.DataFrame([{
        '지표': row.get('label') or '지표 미확인',
        '값': amount(row.get('value'), row.get('unit')),
        '상태': _status(row),
        '산식': row.get('formula') or '—',
        '확인사항': row.get('reason') or '—',
        '공시': _sources(row),
    } for row in rows], columns=columns)


def history_detail_frame(rows: Iterable[dict]) -> pd.DataFrame:
    """Full raw comparison detail keeps currency amounts exact, including cents."""
    columns = ['계정', '재무제표', '구성원', '비교기간', '비교 기준', '비교금액', '당기금액', '증감액',
               '증감률', '상태', '재작성', '이전 공시값', '확인사항', '계정 ID', '공시']
    display = []
    for row in rows:
        currency = row.get('currency')
        display.append({
            '계정': row.get('account_name') or row.get('label') or '계정 미확인',
            '재무제표': row.get('sj_div') or '—',
            '구성원': row.get('account_detail') or '—',
            '비교기간': row.get('from_period') or '—',
            '비교 기준': row.get('comparison_basis') or '—',
            '비교금액': amount(row.get('previous'), currency, compact=False),
            '당기금액': amount(row.get('current'), currency, compact=False),
            '증감액': amount(row.get('delta'), currency, compact=False),
            '증감률': _percent(row),
            '상태': _status(row),
            '재작성': '차이 있음' if row.get('restated') else '—',
            '이전 공시값': amount(row.get('historical_previous'), currency, compact=False),
            '확인사항': row.get('reason') or '—',
            '계정 ID': row.get('account_id') or '—',
            '공시': _sources(row),
        })
    return pd.DataFrame(display, columns=columns)

from decimal import Decimal

import pytest

from dart_analyst.presentation import (
    amount, change_label, comparison_frame, history_detail_frame, metrics_frame,
)


@pytest.mark.parametrize('value', [None, 'NaN', 'Infinity', 'invalid', True])
def test_missing_invalid_values_are_not_zero(value):
    assert amount(value) == '—'


def test_krw_compact_and_exact_precision():
    assert amount('120000000000') == '1,200억'
    assert amount(Decimal('-10875000000')) == '-108.75억'
    assert amount('12345678901234567.89', compact=False) == '12,345,678,901,234,567.89원'
    assert amount('100') == '100원'
    assert amount('0') == '0억'


def test_foreign_currency_and_unknown_currency_not_relabelled_won():
    assert amount('1200.125', 'USD') == '1,200.13 USD'
    assert amount('1200.125', 'USD', compact=False) == '1,200.125 USD'
    assert amount('1200', None) == '1,200 (통화 미확인)'
    assert amount('12.5', '%') == '12.5%'
    assert amount('1.234', '배') == '1.23배'


@pytest.mark.parametrize('previous', ['0', '-100', None, 'NaN'])
def test_nonpositive_or_missing_base_never_shows_percent(previous):
    assert change_label({'status':'calculated','previous':previous,'pct':'20'}) is None


def test_only_calculated_comparisons_have_changes():
    assert change_label({'status':'calculated','previous':'100','pct':'20.25'}) == '+20.25%'
    assert change_label({'status':'calculated','previous':'100','pct':'-5'}) == '-5%'
    assert change_label({'status':'calculated','previous':'100','pct':'0'}) == '0%'
    assert change_label({'status':'not_comparable','previous':'100','pct':'20'}) is None


def test_comparison_table_has_meaningful_labels_without_internal_keys():
    rows=[{'key':'revenue','label':'매출액','currency':'USD','from_period':'2024',
           'to_period':'2025','previous':'100','current':'120','delta':'20','pct':'20',
           'status':'calculated','source_ids':['A','B','A']}]
    frame=comparison_frame(rows)
    assert frame.loc[0,'당기금액'] == '120 USD'
    assert frame.loc[0,'증감률'] == '+20%'
    assert frame.loc[0,'상태'] == '산출 완료'
    assert frame.loc[0,'공시'] == 'A, B'
    assert 'key' not in frame.columns
    assert 'source_ids' not in frame.columns


def test_metrics_missings_keep_reasons_and_formula_visible():
    frame=metrics_frame([{'label':'ROE','value':None,'unit':'%','status':'missing_source',
                          'formula':'순이익 / 평균 자본','reason':'기초 지분 미확보'}])
    assert frame.loc[0,'값'] == '—'
    assert frame.loc[0,'상태'] == '자료 부족'
    assert frame.loc[0,'산식'] == '순이익 / 평균 자본'
    assert frame.loc[0,'확인사항'] == '기초 지분 미확보'


def test_raw_history_keeps_exact_value_and_revision_context():
    frame=history_detail_frame([{'account_name':'매출액','account_id':'ifrs-full_Revenue',
          'currency':'KRW','current':'12345678901234567.89','previous':'100.01',
          'historical_previous':'90.01','delta':'12345678901234467.88','pct':None,
          'status':'calculated','restated':True,'comparison_basis':'당기 공시 비교열 우선',
          'source_ids':['20250301000001']}])
    assert frame.loc[0,'당기금액'] == '12,345,678,901,234,567.89원'
    assert frame.loc[0,'이전 공시값'] == '90.01원'
    assert frame.loc[0,'재작성'] == '차이 있음'
    assert frame.loc[0,'비교 기준'] == '당기 공시 비교열 우선'
    assert frame.loc[0,'공시'] == '20250301000001'


def test_empty_frames_preserve_headers():
    assert list(comparison_frame([]).columns)[0] == '계정'
    assert list(metrics_frame([]).columns)[0] == '지표'
    assert list(history_detail_frame([]).columns)[0] == '계정'

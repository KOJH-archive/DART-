"""Regression tests for accounting issues found during integration review."""
from decimal import Decimal

import pytest

from dart_analyst.dart_client import DartClient
from dart_analyst.engine import analyze
from dart_analyst.models import Dataset


def revenue_row(current, **prior):
    return {'sj_div': 'IS', 'account_id': 'ifrs-full_Revenue',
            'account_nm': '매출액', 'currency': 'KRW',
            'thstrm_amount': current, **prior}


@pytest.mark.parametrize('prior', ['', '-', 'NaN', 'invalid'])
def test_selected_blank_or_invalid_comparative_blocks_stale_fallback(prior):
    old = DartClient._normalize([revenue_row('100', frmtrm_amount='80')], 2023, 12, 'CFS', '20240301000001')
    current = DartClient._normalize([revenue_row('120', frmtrm_amount=prior)], 2024, 12, 'CFS', '20250301000001')
    ds = Dataset('검증 기업', scope='CFS', periods=[old, current])
    result = analyze(ds)
    comparative = current.comparatives['revenue']
    assert comparative.amount is None
    assert '과거 공시로 대체하지 않음' in comparative.reason
    growth = next(m for m in result['metrics'] if m['key'] == 'revenue_growth' and m['period'] == current.label)
    assert growth['value'] is None
    assert growth['status'] == 'missing_source'


def test_absent_comparative_column_can_use_compatible_historical_filing():
    old = DartClient._normalize([revenue_row('100')], 2023, 12, 'CFS', '20240301000001')
    current = DartClient._normalize([revenue_row('120')], 2024, 12, 'CFS', '20250301000001')
    result = analyze(Dataset('검증 기업', scope='CFS', periods=[old, current]))
    growth = next(m for m in result['metrics'] if m['key'] == 'revenue_growth' and m['period'] == current.label)
    assert growth['status'] == 'calculated'
    assert Decimal(growth['value']) == Decimal('20')


def test_blank_selected_opening_equity_does_not_use_old_roe_base():
    def equity_row(amount, prior):
        return {'sj_div': 'BS', 'account_id': 'ifrs-full_EquityAttributableToOwnersOfParent',
                'account_nm': '지배기업 소유주지분', 'currency': 'KRW',
                'thstrm_amount': amount, 'frmtrm_amount': prior}
    old = DartClient._normalize([equity_row('500', '450')], 2023, 12, 'CFS', '20240301000001')
    current = DartClient._normalize([equity_row('600', ''),
        {'sj_div':'IS', 'account_id':'ifrs-full_ProfitLossAttributableToOwnersOfParent',
         'account_nm':'지배주주순이익', 'currency':'KRW', 'thstrm_amount':'60', 'frmtrm_amount':'50'}
    ], 2024, 12, 'CFS', '20250301000001')
    result = analyze(Dataset('검증 기업', scope='CFS', periods=[old, current]))
    roe = next(m for m in result['metrics'] if m['key'] == 'roe' and m['period'] == current.label)
    assert roe['value'] is None
    assert roe['status'] == 'missing_source'

"""User-facing data presentation checks; no screenshot or calculation mirrors."""
from decimal import Decimal
from pathlib import Path

from streamlit.testing.v1 import AppTest
from dart_analyst.demo import build_demo


def app():
    return AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py').run(timeout=30)


def frame_with(at, column):
    matches = [item.value for item in at.dataframe if column in item.value.columns]
    assert len(matches) == 1, [(list(item.columns), len(item)) for item in matches]
    return matches[0]


def load_scenario(at, scenario):
    at.selectbox(key='demo_scenario').set_value(scenario)
    next(b for b in at.button if b.label == '가상 자료 분석').click().run(timeout=30)
    assert not at.exception


def test_raw_statement_and_search_filters_are_combined():
    at = app()
    at.selectbox(key='raw_statement').set_value('BS').run(timeout=30)
    at.text_input(key='account_search').set_value('현금').run(timeout=30)
    assert not at.exception
    detail = frame_with(at, '계정 ID')
    assert len(detail) == 1
    assert detail.iloc[0]['계정'] == '현금및현금성자산'
    assert set(detail['재무제표']) == {'BS'}
    assert detail.iloc[0]['당기금액'] == '10,000,000,000원'


def test_standard_account_view_has_korean_columns_and_search():
    at = app()
    at.radio(key='account_view').set_value('표준 계정').run(timeout=30)
    next(t for t in at.text_input if t.label == '표준 계정 검색').set_value('매출').run(timeout=30)
    assert not at.exception
    matrices = [item.value for item in at.dataframe if '2025' in item.value.columns]
    assert len(matrices) == 1
    assert len(matrices[0]) > 0
    assert all('매출' in name for name in matrices[0]['계정'])
    assert not any('key' in item.columns or 'source_ids' in item.columns
                   for item in [d.value for d in at.dataframe if '계정' in d.value.columns])


def test_period_change_updates_kpis_tables_and_chart_horizon():
    at = app()
    at.selectbox(key='selected_period').set_value('2024').run(timeout=30)
    assert not at.exception
    assert next(m.value for m in at.metric if m.label == '매출액') == '1,000억'
    overview = at.dataframe[0].value
    assert overview.loc[overview['계정'] == '매출액', '당기금액'].iloc[0] == '1,000억'
    assert any('2024-01-01' in caption.value and '2024-12-31' in caption.value
               for caption in at.caption)
    assert any('선택 기간 2024' in caption.value and 'DEMO-2024-FY' in caption.value
               for caption in at.caption)
    # Plot specifications expose displayed years without requiring a browser.
    spec = at.get('plotly_chart')[0].proto.spec
    assert '2024' in spec
    assert '2025' not in spec


def test_interim_profit_turns_to_loss_in_kpi_and_source_linked_summary():
    data = build_demo()
    interim = next(period for period in data.periods if period.kind == 'YTD')
    interim.facts['operating_profit'].amount = Decimal('-500000000')
    at = AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py')
    at.session_state['dataset'] = data
    at.run(timeout=30)
    at.selectbox(key='selected_period').set_value(interim.label).run(timeout=30)
    assert not at.exception
    assert next(metric.delta for metric in at.metric if metric.label == '영업이익') == '전년 동기 적자 전환'
    assert any('영업이익 적자 전환' in item.value and interim.filing_id in item.value for item in at.markdown)


def test_interim_unverified_cash_flows_stay_pending_in_raw_detail():
    at = app()
    at.selectbox(key='selected_period').set_value('2026 H1').run(timeout=30)
    at.selectbox(key='raw_statement').set_value('CF').run(timeout=30)
    at.checkbox(key='pending_accounts').check().run(timeout=30)
    assert not at.exception
    detail = frame_with(at, '계정 ID')
    assert len(detail) > 0
    assert set(detail['상태']) == {'비교 기준 불일치'}
    assert set(detail['증감률']) == {'—'}
    assert all('기간 문맥 미확인' in reason for reason in detail['확인사항'])


def test_missing_bridge_and_revision_are_distinct_visible_states():
    at = app()
    load_scenario(at, 'missing')
    at.selectbox(key='selected_period').set_value('2026 H1').run(timeout=30)
    assert next(m.value for m in at.metric if m.label == '자료 부족') == '1건'
    assert next(m.value for m in at.metric if m.label == '불일치') == '0건'
    load_scenario(at, 'restatement')
    at.selectbox(key='selected_period').set_value('2025').run(timeout=30)
    detail = frame_with(at, '계정 ID')
    revised = detail[detail['재작성'] == '차이 있음']
    assert len(revised) == 3
    assert all(value != '—' for value in revised['이전 공시값'])
    assert all('재작성/버전 확인' in reason for reason in revised['확인사항'])
    assert not at.exception


def test_imported_foreign_currency_bridge_retains_its_currency():
    data = build_demo()
    data.source_mode = 'import'
    data.metadata['original_source_mode'] = 'demo'
    for period in data.periods:
        for facts in (period.facts, period.comparatives):
            for fact in facts.values():
                fact.currency = 'USD'
        for raw in period.raw_accounts:
            raw['currency'] = 'USD'
    at = AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py')
    at.session_state['dataset'] = data
    at.run(timeout=30)
    assert not at.exception
    ledgers = [item.value for item in at.markdown if 'class="ledger"' in item.value]
    assert len(ledgers) == 4
    assert all('USD' in html and '억' not in html for html in ledgers)

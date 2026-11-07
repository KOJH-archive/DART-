from streamlit.testing.v1 import AppTest
from pathlib import Path
from dart_analyst.demo import build_demo
from dart_analyst.dart_client import DartClient


def app():
    return AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py').run(timeout=30)


def test_demo_screen_and_cash_mismatch_flow():
    at = app()
    assert not at.exception
    assert at.title[0].value == '가상기업 A'
    assert at.selectbox(key='selected_period').value == '2025'
    at.selectbox(key='demo_scenario').set_value('cash_mismatch')
    next(b for b in at.button if b.label == '가상 자료 분석').click().run(timeout=30)
    at.selectbox(key='selected_period').set_value('2026 H1').run(timeout=30)
    assert not at.exception
    assert next(m.value for m in at.metric if m.label == '불일치') == '1건'
    assert any('가상' in item.value for item in at.caption)


def test_live_query_ui_with_mock_data(monkeypatch):
    company = {'corp_code': '00126380', 'corp_name': '테스트 회사', 'stock_code': '005930'}
    monkeypatch.setattr(DartClient, 'search_companies', lambda self, query: [company])
    def load(self, *args, **kwargs):
        ds = build_demo()
        ds.company = '테스트 회사'
        ds.source_mode = 'live'
        ds.notes = [{'topic':'회계정책','status':'발췌 가능','source_id':'20260301000001','excerpt':'모의 응답','source_url':'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20260301000001'}]
        return ds
    monkeypatch.setattr(DartClient, 'load_company', load)
    at = app()
    at.radio(key='source_mode').set_value('DART 기업 조회').run()
    next(t for t in at.text_input if t.label == 'DART API 인증키').set_value('mock-key')
    next(t for t in at.text_input if t.label == '회사명 또는 종목코드').set_value('테스트')
    next(b for b in at.button if b.label == '기업 검색').click().run(timeout=30)
    next(b for b in at.button if b.label == '공시 수집 · 분석').click().run(timeout=30)
    assert not at.exception
    assert at.title[0].value == '테스트 회사'
    assert not any('가상' in item.value for item in at.caption)


def test_missing_key_never_calls_dart(monkeypatch):
    monkeypatch.delenv('DART_API_KEY', raising=False)
    def forbidden(*args, **kwargs):
        raise AssertionError('API call must not occur')
    monkeypatch.setattr(DartClient, 'search_companies', forbidden)
    at = app()
    at.radio(key='source_mode').set_value('DART 기업 조회').run()
    next(t for t in at.text_input if t.label == '회사명 또는 종목코드').set_value('테스트')
    next(b for b in at.button if b.label == '기업 검색').click().run()
    assert not at.exception
    assert any('인증키' in item.value for item in at.error)

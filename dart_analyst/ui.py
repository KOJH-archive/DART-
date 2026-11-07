"""Streamlit presentation; all accounting values come from the analysis engine."""
from __future__ import annotations

from decimal import Decimal
from datetime import datetime, timezone, timedelta
from html import escape
import os
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from .dart_client import DartClient, DartError, INTERIM_CF_HOLD
from .demo import build_demo, NAMES
from .engine import LABELS, analyze, profit_transition
from .exporters import make_excel, make_html, make_markdown, safe_source_url
from .models import dataset_from_json, dataset_to_json
from .narrative import COMMENTARY_FORMAT_VERSION, CommentaryError, build_summary, generate_ai_commentary, commentary_matches
from .presentation import STATUS_LABELS, amount, change_label, comparison_frame, metrics_frame, history_detail_frame
from .news import NewsError, fetch_news, select_news, summarize_news

STATEMENTS = {'BS':'재무상태표','IS':'손익계산서','CIS':'포괄손익계산서','CF':'현금흐름표','SCE':'자본변동표'}
SCENARIOS = {'normal':'기본 자료','restatement':'과거 비교금액 재작성','missing':'현금 조정항목 누락','cash_mismatch':'현금 연결 5억 원 불일치'}
COLORS = ['#244c41','#9a8060','#6c8395']


def set_dataset(data):
    st.session_state.dataset = data
    st.session_state.pop('ai_commentary', None)
    st.session_state.pop('recent_news', None)
    if st.session_state.get('selected_period') not in {p.label for p in data.periods}:
        st.session_state.pop('selected_period', None)


def table(frame, *, height=380):
    if frame.empty:
        st.caption('선택한 조건에 해당하는 자료가 없습니다.')
        return
    numeric = {'값','비교금액','당기금액','증감액','증감률','이전 공시값'}
    config = {col:st.column_config.TextColumn(alignment='right') for col in frame.columns
              if col in numeric or (str(col)[:4].isdigit() and len(str(col)) >= 4)}
    config.update({'계정':st.column_config.TextColumn(width='medium',pinned=True),
                   '확인사항':st.column_config.TextColumn(width='large')})
    st.dataframe(frame, width='stretch', hide_index=True,
                 height=min(height, max(90, 36 * (len(frame) + 1))),
                 column_config=config)


def sidebar():
    with st.sidebar:
        st.markdown('<div class="wordmark"><strong>DART</strong><span>재무 분석</span></div>', unsafe_allow_html=True)
        mode = st.radio('자료 선택', ['검증용 가상 자료','DART 기업 조회','저장 자료 불러오기'], key='source_mode')
        st.divider()
        if mode == '검증용 가상 자료':
            scenario = st.selectbox('검증 시나리오', list(SCENARIOS), format_func=SCENARIOS.__getitem__, key='demo_scenario')
            if st.button('가상 자료 분석', type='primary', width='stretch'):
                set_dataset(build_demo(scenario))
            st.caption('가상 기업의 자료로 비교·대조 기능을 살펴봅니다.')
        elif mode == 'DART 기업 조회':
            api_key = st.text_input('DART API 인증키', value=os.getenv('DART_API_KEY',''), type='password', help='현재 세션에서 사용합니다. 보고서에는 저장되지 않습니다.')
            query = st.text_input('회사명 또는 종목코드', placeholder='삼성전자 또는 005930')
            if st.button('기업 검색', width='stretch'):
                if not api_key:
                    st.error('DART 인증키를 입력해 주세요.')
                elif not query.strip():
                    st.error('검색어를 입력해 주세요.')
                else:
                    try:
                        with st.spinner('회사 목록 조회 중'):
                            with DartClient(api_key) as client:
                                st.session_state.candidates = client.search_companies(query)
                        if not st.session_state.candidates:
                            st.info('일치하는 회사가 없습니다.')
                    except Exception:
                        st.session_state.candidates = []
                        st.error('기업 검색에 실패했습니다. 인증키와 연결 상태를 확인해 주세요.')
            candidates = st.session_state.get('candidates', [])
            if candidates:
                selected = st.selectbox('분석할 기업', candidates, format_func=lambda c:f"{c['corp_name']} · {c.get('stock_code') or c['corp_code']}")
                years = st.select_slider('연간 조회 범위', options=[3,4,5], value=5)
                scope = st.selectbox('분석 기준', ['CFS','OFS'], format_func=lambda x:'연결재무제표' if x == 'CFS' else '별도재무제표')
                interim = st.checkbox('최신 중간보고서 포함', value=True)
                if st.button('공시 수집 · 분석', type='primary', width='stretch'):
                    if not api_key:
                        st.error('인증키를 입력해 주세요.')
                    else:
                        try:
                            with st.spinner('공시·재무제표 수집 중'):
                                with DartClient(api_key) as client:
                                    loaded = client.load_company(selected['corp_code'], selected['corp_name'], selected.get('stock_code',''), years=years, scope=scope, include_interim=interim)
                            if loaded.periods:
                                set_dataset(loaded)
                            else:
                                st.error('비교 가능한 재무제표가 없습니다.')
                                for issue in loaded.issues:
                                    st.write(issue)
                        except DartError as exc:
                            st.error(str(exc))
                        except Exception:
                            st.error('수집을 완료하지 못했습니다. 인증키·업종·공시 상태를 확인해 주세요.')
            st.caption('지원 범위 · 전업종 · 12월 결산 · 원화')
        else:
            uploaded = st.file_uploader('분석 자료 JSON', type=['json'])
            if uploaded and st.button('저장 자료 분석', type='primary', width='stretch'):
                try:
                    imported = dataset_from_json(uploaded.getvalue().decode('utf-8'))
                    imported.metadata['original_source_mode'] = imported.source_mode
                    imported.source_mode = 'import'
                    imported.issues.append('저장 자료: 이 실행에서 DART 원본을 재조회하지 않았습니다.')
                    if not imported.periods:
                        raise ValueError('empty')
                    set_dataset(imported)
                except Exception:
                    st.error('분석 자료 형식이 올바르지 않습니다.')
            st.caption('보관 자료를 불러옵니다. 최신 정정공시는 재조회가 필요합니다.')


def chart_style(fig, *, height=285):
    fig.update_layout(height=height, margin=dict(l=6,r=10,t=10,b=40),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      colorway=COLORS, hovermode='x unified',
                      font=dict(family='Pretendard, Noto Sans KR, sans-serif',size=11,color='#69736d'),
                      legend=dict(orientation='h',y=-.21,x=0,font=dict(size=11)),
                      hoverlabel=dict(bgcolor='white',font_size=12),
                      xaxis=dict(showgrid=False,zeroline=False,tickfont=dict(size=11)),
                      yaxis=dict(gridcolor='#e4e6de',zerolinecolor='#ccd1c6',tickformat=',.0f',title=None))
    st.plotly_chart(fig, width='stretch', config={'displayModeBar':False,'scrollZoom':False})


def line_chart(periods, keys):
    fig = go.Figure()
    available = False
    for key in keys:
        values = []
        for p in periods:
            f = p.facts.get(key)
            values.append(float(f.amount*f.unit/Decimal(100000000)) if f and f.amount is not None and f.currency == 'KRW' and f.scope == p.scope else None)
        available = available or any(v is not None for v in values)
        fig.add_trace(go.Scatter(x=[p.label for p in periods],y=values,name=NAMES.get(key,key),
                                 mode='lines+markers',line=dict(width=2),marker=dict(size=5),
                                 connectgaps=False,hovertemplate='%{y:,.2f}억 원<extra>%{fullData.name}</extra>'))
    if not available:
        st.caption('표시할 원화 연간 자료가 없습니다.')
        return
    chart_style(fig)


def selected_comparisons(analysis, period):
    return [{**c,'currency':period.facts[c['key']].currency if c['key'] in period.facts else None}
            for c in analysis['comparisons'] if c['to_period'] == period.label]


def ai_commentary(dataset, analysis):
    with st.expander('AI 검토 메모'):
        st.caption('로컬 Ollama가 최신 기간의 지표·주석과 업종별 검토 관점을 고릅니다. 메모는 공시에서 확인한 변화와 업종 배경을 구분해 표시합니다.')
        key_col, model_col = st.columns(2)
        base_url = key_col.text_input('Ollama 주소', value=os.getenv('OLLAMA_BASE_URL','http://127.0.0.1:11434'))
        model = model_col.text_input('모델', value=os.getenv('OLLAMA_MODEL','qwen3.5:4b'), placeholder='qwen3.5:4b')
        if st.button('검토 메모 생성 · 로컬 모델 호출'):
            try:
                with st.spinner('근거를 확인하며 설명 생성 중'):
                    st.session_state.ai_commentary = generate_ai_commentary(dataset,analysis,base_url,model)
            except CommentaryError as exc:
                st.error(str(exc))
        result = st.session_state.get('ai_commentary',{})
        if result and not commentary_matches(dataset, result):
            st.session_state.pop('ai_commentary', None)
            st.info('표시·검증 기준이 개선되었습니다. 검토 메모를 다시 생성해 주세요.')
            result = {}
        if result.get('period'):
            st.caption(f"메모 기준 기간 · {result['period']}")
        if omitted := result.get('omitted_claims'):
            st.caption(f'근거 검증을 통과하지 못한 항목 {omitted}개를 제외했습니다.')
        for review_index, review in enumerate(result.get('industry_reviews', [])):
            st.markdown(f"**{review['title']}**")
            st.write(review['observation'])
            receipts = list(dict.fromkeys(r for row in review['comparisons'] for r in row['source_ids']))
            st.caption(f"공시 근거 · {', '.join(receipts)}")
            st.caption(f"업종 배경 · {review['background']}")
            st.write(review['question'])
            if review.get('supporting_notes'):
                with st.expander(f"{review['title']} · 관련 사업 공시"):
                    for note_index, note in enumerate(review['supporting_notes']):
                        st.write(note['excerpt'])
                        st.caption(f"{note['topic']} · {note['source_id']} · {note['location']}")
                        if (url := safe_source_url(note.get('source_url'))):
                            st.link_button('관련 사업 공시 원문',url,key=f'review-source-{review_index}-{note_index}')
        for claim in result.get('claims',[]):
            st.write(claim['rendered_text'])
            st.caption({'observation':'계산 지표','question':'확인 항목'}.get(claim['kind'],'검토 필요'))
        if result:
            with st.expander('문장별 근거'):
                st.json({k:result.get(k,{}) for k in ['industry_reviews','claims','metric_catalog','evidence_catalog']})


@st.cache_data(ttl=300, max_entries=1, show_spinner=False)
def cached_news():
    return fetch_news()


def recent_news(dataset):
    with st.expander('최근 경제 뉴스 · 연합인포맥스'):
        st.caption('최근 7일 이내 RSS 제공 기사에서 기업·업종 관련 뉴스와 금리·환율 이슈를 찾습니다. 재무제표 기준 기간과 기사 발행일을 함께 확인하세요.')
        if st.button('최근 뉴스 불러오기', key='load_recent_news'):
            with st.spinner('연합인포맥스 RSS 조회 중'):
                snapshot = cached_news()
                candidates = select_news(snapshot['articles'], dataset)
                st.session_state.recent_news = {
                    **snapshot, 'articles': candidates, 'display': candidates[:5], 'ai_selected': False,
                }
        news = st.session_state.get('recent_news')
        if not news:
            return
        for issue in news['errors']:
            st.warning(issue)
        if not news['articles']:
            st.info('현재 RSS에서 최근 7일 이내의 기사를 확보하지 못했습니다.')
            return
        zone = timezone(timedelta(hours=9))
        retrieved = datetime.fromisoformat(news['retrieved_at']).astimezone(zone)
        st.caption(f"수집 시각 · {retrieved:%Y-%m-%d %H:%M} KST · 피드당 최근 제공분 · 5분 캐시")
        if st.button('Ollama로 핵심 3~5건 선정', key='summarize_recent_news'):
            try:
                with st.spinner('로컬 모델이 핵심 기사와 문장을 고르는 중'):
                    selected = summarize_news(
                        news['articles'], os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434'),
                        os.getenv('OLLAMA_MODEL', 'qwen3.5:4b'),
                    )
                news['display'] = selected
                news['ai_selected'] = True
            except (NewsError, CommentaryError) as exc:
                st.warning(str(exc))
        st.caption('Ollama 선정 · RSS 제공 핵심 문장' if news['ai_selected'] else '관련도와 발행일 순 · RSS 제공 요약')
        for article in news['display']:
            published = datetime.fromisoformat(article['published_at']).astimezone(zone)
            st.markdown(f"**{article['title']}**")
            st.caption(f"{published:%Y-%m-%d %H:%M} KST · {article['section']} · {article['relevance']}")
            if article['summary'] != article['title']:
                st.write(article['summary'])
            st.link_button('연합인포맥스 원문', article['url'])


def overview(dataset, analysis, periods, period):
    annual = [p for p in periods if p.kind == 'FY' and p.end <= period.end]
    left, right = st.columns(2,gap='large')
    with left:
        st.subheader('이익과 영업현금')
        st.caption('연간 추이 · 억 원')
        line_chart(annual,['net_income','cfo'])
    with right:
        st.subheader('매출채권·재고·현금')
        st.caption('연간 잔액 · 억 원')
        line_chart(annual,['receivables','inventory','cash'])
    st.subheader(f'{period.label} 주요 변동')
    rows = selected_comparisons(analysis,period)
    focus = {'revenue','operating_profit','net_income','cfo','receivables','inventory','borrowings'}
    summary_frame = comparison_frame(r for r in rows if r['key'] in focus)
    table(summary_frame[['계정','비교금액','당기금액','증감률','상태']],height=330)
    st.caption('흐름 계정은 전년 동일 기간과 비교합니다. —는 자료 부족 또는 비교 불가입니다.')
    left, right = st.columns([1,1],gap='large')
    with left:
        st.subheader('수익성과 현금전환')
        focus_metrics = {'operating_margin','cfo_to_net_income','fcf','roe'}
        table(metrics_frame(m for m in analysis['metrics'] if m['period'] == period.label and m['key'] in focus_metrics).iloc[:,:3],height=215)
    with right:
        st.subheader('검토할 항목')
        relevant = [c for c in analysis['checks'] if c['period'] == period.label and c['status'] != 'pass']
        if relevant:
            for row in relevant:
                st.write(f"**{row['label']}**")
                st.caption(row.get('reason') or STATUS_LABELS.get(row['status'],'확인 필요'))
        else:
            passed = sum(c['status'] == 'pass' for c in analysis['checks'] if c['period'] == period.label)
            st.write(f'확보된 자료에서 연결 대조 {passed}개 항목이 일치합니다.')
            st.caption('계정·주석 전체에 대한 검증 결과는 아닙니다.')
    with st.expander('계산 요약과 검토 근거'):
        for line in build_summary(dataset,analysis):
            st.write(line)
    ai_commentary(dataset,analysis)
    recent_news(dataset)


def account_comparison(dataset, analysis, periods, period):
    history = analysis['account_history']
    view = st.radio('계정 범위',['공시 전체 계정','표준 계정'],horizontal=True,key='account_view',label_visibility='collapsed')
    if view == '공시 전체 계정':
        hrows = history['rows']
        search_col, statement_col = st.columns([3,1])
        term = search_col.text_input('계정 검색',placeholder='계정명 또는 XBRL ID',key='account_search')
        statement = statement_col.selectbox('재무제표',['전체',*STATEMENTS],format_func=lambda k:STATEMENTS.get(k,k),key='raw_statement')
        filtered = [r for r in hrows if (statement == '전체' or r['sj_div'] == statement) and (not term or term.casefold() in f"{r['account_name']} {r['account_id']}".casefold())]
        matrix = {}
        for row in filtered:
            identity = matrix.setdefault(row['key'], {'계정':row['account_name'],'재무제표':STATEMENTS.get(row['sj_div'],row['sj_div']),'구성원':row['account_detail'] or '—'})
            identity[row['to_period']] = amount(row.get('current'),row.get('currency'))
        st.caption('원화는 억 원 표시 · 연간/누적 구분 · 정확한 원금액은 대조 상세에서 확인')
        table(pd.DataFrame(list(matrix.values())),height=430)
        st.subheader(f'{period.label} 대조 상세')
        pending = st.checkbox('보류된 계정만 보기',key='pending_accounts')
        selected = [r for r in filtered if r['to_period'] == period.label and (not pending or r['status'] != 'calculated')]
        table(history_detail_frame(selected),height=390)
        with st.expander('비교 기준과 범위'):
            for line in history['limitations']:
                st.write(line)
            st.caption('중간 재무상태표의 비교열은 전년 말입니다. 전년 동분기와 구분합니다.')
    else:
        term = st.text_input('표준 계정 검색',placeholder='예: 매출, 현금, 재고')
        matrix = []
        for key in dict.fromkeys(k for p in periods for k in p.facts):
            name = next(p.facts[key].name for p in periods if key in p.facts)
            if term and term not in name and term.casefold() not in key.casefold():
                continue
            row = {'계정':name}
            for p in periods:
                fact = p.facts.get(key)
                row[p.label] = amount(fact.amount*fact.unit if fact and fact.amount is not None else None, fact.currency if fact else None)
            matrix.append(row)
        st.caption('원화는 억 원 표시 · 연간과 중간기간의 길이가 다르므로 증감은 동종 기간끼리 산출')
        table(pd.DataFrame(matrix),height=430)
        st.subheader(f'{period.label} 비교기 대비 변화')
        rows = selected_comparisons(analysis,period)
        if term:
            rows = [r for r in rows if term in r['label'] or term.casefold() in r['key'].casefold()]
        table(comparison_frame(rows),height=390)
    with st.expander(f'{period.label} 원본 데이터'):
        st.caption('미매핑 계정도 포함합니다. 아래 표의 값은 원본 API 필드입니다.')
        table(pd.DataFrame(period.raw_accounts),height=390)


def reconciliation(analysis, period):
    checks = [c for c in analysis['checks'] if c['period'] == period.label]
    cols = st.columns(4)
    for col,status,title in zip(cols,['pass','fail','incomplete','not_comparable'],['대조 일치','불일치','자료 부족','기준 불일치']):
        col.metric(title,f"{sum(c['status'] == status for c in checks)}건")
    st.caption('확보된 항목과 산식의 대조 결과입니다. 누락된 값을 차액으로 보충하지 않습니다.')
    for check in checks:
        status = check['status']
        with st.expander(f"{check['label']}  ·  {STATUS_LABELS.get(status,status)}",expanded=status != 'pass'):
            currencies = {period.facts[k].currency for k in check['input_keys'] if k in period.facts and period.facts[k].amount is not None}
            currency = next(iter(currencies)) if len(currencies) == 1 else None
            cells = ''.join(f'<div><span>{title}</span><strong>{escape(amount(check.get(key),currency))}</strong></div>' for key,title in [('left','좌변'),('right','우변'),('difference','차이')])
            st.markdown(f'<div class="ledger">{cells}</div>',unsafe_allow_html=True)
            st.caption(check.get('reason',''))
            if proof := check.get('reported_net_change'):
                basis = {'before_fx':'환율효과 제외','after_fx':'환율효과 포함','unverified':'표시 범위 확인 필요'}
                st.caption('공시 구성 합계로 확인한 순증감 기준 · '+basis.get(proof.get('basis'),'확인 필요'))
            st.caption('참조 계정: '+', '.join(NAMES.get(k,LABELS.get(k,k)) for k in check['input_keys']))
    bridge = next((c for c in checks if c['key'] == 'cash_flow'),{})
    ending_key = 'cash_end' if 'cash_end' in bridge.get('input_keys', []) else 'cash'
    keys = [k for k in bridge.get('input_keys', [])
            if k not in {ending_key, bridge.get('reported_net_change', {}).get('key')}]
    if (bridge.get('status') in {'pass','fail'}
            and all(k in period.facts and period.facts[k].amount is not None
                    for k in keys)
            and all(period.facts[k].currency == 'KRW' for k in bridge['input_keys'])):
        st.subheader('현금의 증감 구성')
        ending = period.facts[ending_key]
        st.caption(f"{period.label} · 억 원 · 공시 기말 현금 {amount(ending.amount*ending.unit)}")
        values = [float(period.facts[k].amount*period.facts[k].unit/Decimal(100000000)) for k in keys]
        fig = go.Figure(go.Waterfall(x=[LABELS.get(k,k) for k in keys]+['산식상 기말'],y=values+[0],measure=['absolute']+['relative']*(len(keys)-1)+['total'],connector=dict(line=dict(color='#bdc5ba',width=1)),increasing=dict(marker=dict(color=COLORS[0])),decreasing=dict(marker=dict(color='#b17a62')),totals=dict(marker=dict(color='#6c8395'))))
        chart_style(fig,height=330)
    with st.expander('현금·자본 대조 시 유의사항'):
        st.write('현금 지급 배당과 자본에 인식한 배당을 구분합니다. 환율·비현금 거래·기타 조정이 누락되면 대조를 보류합니다. 일치 결과는 전체 계정·주석의 완전성을 보증하지 않습니다.')


def evidence(dataset, period):
    st.subheader('계정의 원천 공시')
    facts = period.facts
    if facts:
        key = st.selectbox('확인할 계정',list(facts),format_func=lambda k:facts[k].name,key='evidence_account')
        f = facts[key]
        st.metric(f.name,amount(f.amount*f.unit if f.amount is not None else None,f.currency))
        left,right = st.columns([3,1],vertical_alignment='center')
        left.caption(f'{STATEMENTS.get(f.statement,f.statement)} · {f.start} — {f.end} · {f.currency}')
        if (url := safe_source_url(f.source_url)):
            right.link_button('공시 원문',url,width='stretch')
        with st.expander('원천 필드와 출처 상세'):
            st.json({'계정':f.name,'원금액':str(f.amount) if f.amount is not None else None,'단위':str(f.unit),'통화':f.currency,'기준':f.scope,'시작':f.start,'종료':f.end,'기간유형':f.period_kind,'계정ID':f.account_id,'공시':f.source_id,'원본필드':f.source_field,'확인사항':f.reason})
            if f.source_details:
                st.json(f.source_details, expanded=False)
    st.subheader('주석 발췌')
    st.caption('관련 문단을 발췌한 자료입니다. 발췌 없음이 위험 없음을 뜻하지 않습니다.')
    for index,note in enumerate(dataset.notes):
        with st.expander(f"{note.get('topic','주석')} · {note.get('status','미확인')}"):
            st.write(note.get('excerpt') or '확인 가능한 발췌가 없습니다.')
            st.caption(note.get('location',''))
            if note.get('normalization'):
                st.caption(note['normalization'])
            if (url := safe_source_url(note.get('source_url'))):
                st.link_button('공시 원문',url,key=f'note-{index}')


def downloads(dataset, analysis):
    st.subheader('분석 보고서')
    st.caption('비교 기준·산식·출처와 미완료 대조 항목을 함께 저장합니다. 생성된 AI 메모도 포함합니다.')
    analysis = {**analysis, 'ai_commentary': st.session_state.get('ai_commentary')}
    formats = [
        ('Excel','계정 비교, 재무지표, 회계 대조와 원천 계정','dart-analysis.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',make_excel),
        ('HTML','목차가 있는 보고서. 브라우저 인쇄로 PDF 저장','dart-report.html','text/html',make_html),
        ('Markdown','문서 편집과 기록용 텍스트 보고서','dart-report.md','text/markdown',make_markdown),
    ]
    for label,description,name,mime,generate in formats:
        st.divider()
        left,right = st.columns([4,1],vertical_alignment='center')
        left.markdown(f'<div class="file-label">{label}</div><div class="file-meta">{description}</div>',unsafe_allow_html=True)
        right.download_button('다운로드',generate(dataset,analysis),file_name=name,mime=mime,key=f'download-{label}',width='stretch')
    st.divider()
    left,right = st.columns([4,1],vertical_alignment='center')
    left.markdown('<div class="file-label">분석 자료 JSON</div><div class="file-meta">당기·비교기 원천 자료. 앱에서 다시 불러올 수 있습니다.</div>',unsafe_allow_html=True)
    right.download_button('자료 저장',dataset_to_json(dataset),file_name='dart-dataset.json',mime='application/json',width='stretch')


def main():
    st.set_page_config(page_title='DART · 재무 분석',page_icon=':material/table_chart:',layout='wide',initial_sidebar_state='expanded')
    st.markdown('<style>'+Path(__file__).with_name('ui.css').read_text()+'</style>',unsafe_allow_html=True)
    sidebar()
    if 'dataset' not in st.session_state:
        set_dataset(build_demo())
    dataset = st.session_state.dataset
    analysis = analyze(dataset)
    periods = sorted(dataset.periods,key=lambda p:(p.end,p.kind))
    if not periods:
        st.info('비교할 자료가 없습니다. 기업을 조회하거나 저장 자료를 불러오세요.')
        return
    labels = [p.label for p in reversed(periods)]
    default = next((p.label for p in reversed(periods) if p.kind == 'FY'),labels[0])
    st.markdown('<div class="workspace-label">기업 재무분석</div>',unsafe_allow_html=True)
    left,right = st.columns([5,2],vertical_alignment='bottom')
    with left:
        st.title(dataset.company)
    with right:
        selected = st.selectbox('상세 분석 기간',labels,index=labels.index(default),key='selected_period')
    period = next(p for p in periods if p.label == selected)
    scope = '연결' if period.scope == 'CFS' else '별도'
    kind = '연간' if period.kind == 'FY' else '누적 중간 실적'
    source = {'demo':'가상 검증 자료','import':'보관 자료 · DART 재조회 안 함','live':'OpenDART','dart':'OpenDART'}.get(dataset.source_mode,'사용자 자료')
    stock = f' · {dataset.stock_code}' if dataset.stock_code else ''
    st.caption(f'{source}{stock}  ·  {scope}  ·  {kind}  ·  {period.start} — {period.end}')
    if dataset.source_mode == 'demo':
        st.caption('실제 기업의 공시가 아닌 가상 데이터입니다.')
    rows = selected_comparisons(analysis,period)
    by_key = {r['key']:r for r in rows}
    cols = st.columns(4,gap='large')
    for col,key,title in zip(cols,['revenue','operating_profit','net_income','cfo'],['매출액','영업이익','순이익','영업현금흐름']):
        f = period.facts.get(key)
        comparison = by_key.get(key)
        delta = profit_transition(comparison) or change_label(comparison)
        col.metric(title,amount(f.amount*f.unit if f and f.amount is not None else None,f.currency if f else None),delta=f'전년 동기 {delta}' if delta else None,delta_color='off')
    checks = [c for c in analysis['checks'] if c['period'] == period.label]
    passed = sum(c['status'] == 'pass' for c in checks)
    failed = sum(c['status'] == 'fail' for c in checks)
    unfinished = sum(c['status'] not in {'pass','fail'} for c in checks)
    hrows = [r for r in analysis['account_history']['rows'] if r['to_period'] == period.label]
    compared = sum(r['status'] == 'calculated' for r in hrows)
    strip = f'<span>연결 대조 <strong>{passed}/{len(checks)} 일치</strong></span><span>계정 비교 <strong>{compared}/{len(hrows)} 산출</strong></span>'
    if failed:
        strip += f'<span class="attention">불일치 <strong>{failed}건</strong></span>'
    if unfinished:
        strip += f'<span>자료·기준 확인 <strong>{unfinished}건</strong></span>'
    st.markdown(f'<div class="review-strip">{strip}</div>',unsafe_allow_html=True)
    issues = list(dict.fromkeys(dataset.issues + [
        issue for p in dataset.periods for issue in p.issues
        if issue.partition(': ')[2] != INTERIM_CF_HOLD
    ]))
    for p in dataset.periods:
        held = [LABELS.get(parts[0], parts[0]) for issue in p.issues
                if (parts := issue.partition(': '))[2] == INTERIM_CF_HOLD]
        if held:
            issues.append(f'{p.label} · 공시 {p.filing_id} · {INTERIM_CF_HOLD} 대상 {len(held)}개 · {", ".join(held)}')
    if issues:
        with st.expander(f'자료 확인사항 · {len(issues)}건'):
            for issue in issues:
                st.write(issue)
            for index,gap in enumerate(dataset.metadata.get('filing_gaps', [])):
                st.write(f"{gap['period']} · 보류된 공시 원문 확인")
                st.caption(gap['reason'])
                for receipt in dict.fromkeys([gap['selected_receipt'], *gap['api_receipts']]):
                    if isinstance(receipt,str) and len(receipt) == 14 and receipt.isdecimal():
                        st.link_button(f'공시 {receipt}',f'https://dart.fss.or.kr/dsaf001/main.do?rcpNo={receipt}',
                                       key=f'filing-gap-{index}-{receipt}')
    tabs = st.tabs(['개요','계정 비교','연결 대조','재무지표','공시 근거','내보내기'])
    with tabs[0]:
        overview(dataset,analysis,periods,period)
    with tabs[1]:
        account_comparison(dataset,analysis,periods,period)
    with tabs[2]:
        reconciliation(analysis,period)
    with tabs[3]:
        st.subheader(f'{period.label} 재무지표')
        table(metrics_frame(m for m in analysis['metrics'] if m['period'] == period.label),height=600)
        with st.expander('계산 기준'):
            st.write('연결 ROE는 지배주주 순이익과 평균 지배주주지분을 사용합니다. 별도는 해당 회사 전체 순이익·자본을 사용합니다. 기초잔액·기간·분모가 맞지 않으면 산출을 보류합니다. 중간 ROE·ROA는 연율화하지 않습니다.')
    with tabs[4]:
        evidence(dataset,period)
    with tabs[5]:
        downloads(dataset,analysis)
    st.divider()
    st.caption(f'DART 재무 분석  ·  {len(periods)}개 기간  ·  선택 기간 {period.label}  ·  공시 {period.filing_id}  ·  금액의 통화·비교 기준은 각 표에 표시')

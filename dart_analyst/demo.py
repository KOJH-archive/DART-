"""명확히 표시된 가상 검증 데이터. 실제 공시를 가장하지 않습니다."""
from copy import deepcopy
from decimal import Decimal as D
from .models import Dataset, Fact, Period

NAMES = {
    'revenue':'매출액','cost_of_sales':'매출원가','gross_profit':'매출총이익',
    'operating_profit':'영업이익','net_income':'전체 당기순이익','parent_net_income':'지배주주 순이익',
    'assets':'자산총계','liabilities':'부채총계','equity':'자본총계','parent_equity':'지배주주 지분',
    'current_assets':'유동자산','current_liabilities':'유동부채','cash':'현금및현금성자산',
    'receivables':'순매출채권','inventory':'재고자산','cfo':'영업활동현금흐름',
    'cfi':'투자활동현금흐름','cff':'재무활동현금흐름','fx_effect':'환율변동효과',
    'other_cash_effects':'기타 현금조정','cash_beginning':'기초 현금',
    'capex_ppe':'유형자산 현금취득','capex_intangible':'무형자산 현금취득',
    'borrowings':'차입금(리스 제외)','lease_liabilities':'리스부채','interest_expense':'총이자비용',
    'oci':'기타포괄손익','dividends_paid':'현금배당 지급','equity_dividends':'자본차감 배당',
    'equity_beginning':'기초 자본','equity_other_changes':'기타 자본변동',
}
BS = {'assets','liabilities','equity','parent_equity','current_assets','current_liabilities','cash','receivables','inventory','borrowings','lease_liabilities'}
CF = {'cfo','cfi','cff','fx_effect','other_cash_effects','cash_beginning','capex_ppe','capex_intangible','dividends_paid'}
SCE = {'oci','equity_dividends','equity_beginning','equity_other_changes'}


def _period(year, values, kind='FY', end=None):
    start, end = f'{year}-01-01', end or f'{year}-12-31'
    p = Period(label=f'{year}' if kind=='FY' else f'{year} H1', year=year,start=start,end=end,kind=kind,filing_id=f'DEMO-{year}-{kind}')
    for k,v in values.items():
        statement = 'BS' if k in BS else 'CF' if k in CF else 'SCE' if k in SCE else 'IS'
        f=Fact(k,NAMES[k],D(str(v))*D('100000000'),statement,end if statement=='BS' else start,end,
               source_id=p.filing_id,account_id=f'demo:{k}',period_kind=kind,
               attribution='parent' if k.startswith('parent_') else 'total')
        p.facts[k]=f
        p.raw_accounts.append({'sj_div':statement,'account_id':f.account_id,'account_nm':f.name,'thstrm_amount':str(f.amount),'rcept_no':p.filing_id})
    return p


def _sync_raw(dataset):
    """API-shaped fictional rows agree with scenario facts, including revisions."""
    for p in dataset.periods:
        p.raw_accounts=[]
        for key,f in p.facts.items():
            raw={'sj_div':f.statement,'account_id':f.account_id,'account_nm':f.name,
                 'currency':f.currency,'unit':str(f.unit),'fs_div':p.scope,
                 'bsns_year':str(p.year),'rcept_no':p.filing_id,
                 'reprt_code':{'03':'11013','06':'11012','09':'11014','12':'11011'}[p.end[5:7]],
                 'account_detail':'자본 [member]' if f.statement=='SCE' else ''}
            current_field='thstrm_add_amount' if p.kind=='YTD' and f.statement in {'IS','CIS'} else 'thstrm_amount'
            prior_field='frmtrm_add_amount' if p.kind=='YTD' and f.statement in {'IS','CIS'} else 'frmtrm_amount'
            raw[current_field]=str(f.amount) if f.amount is not None else ''
            comp=p.comparatives.get(key)
            if f.statement=='BS' and p.kind=='YTD':
                annual=next((old for old in dataset.periods if old.kind=='FY' and old.year==p.year-1),None)
                comp=annual.facts.get(key) if annual else None
            if comp:
                raw[prior_field]=str(comp.amount) if comp.amount is not None else ''
            p.raw_accounts.append(raw)


def build_demo(scenario='normal'):
    # 단위 억 원. CFO/CFI/CFF와 자본변동은 모두 가상 원천값으로 명시합니다.
    rows = [
      (2021,600,450,42,30,40,30,550,250,300,60,140,70,60),
      (2022,700,525,49,36,50,35,620,270,350,70,160,85,70),
      (2023,800,600,64,48,60,40,700,300,400,80,180,100,80),
      (2024,1000,750,100,80,70,50,850,400,450,90,230,140,120),
      (2025,1200,930,108,90,45,80,1000,520,480,100,320,220,170),
    ]
    previous_cash, previous_equity=50,270
    dataset=Dataset('가상기업 A',source_mode='demo',metadata={'scenario':scenario,'notice':'모든 숫자와 메모는 검증용 가상 데이터입니다. 실제 DART 공시를 조회하지 않았습니다.'})
    for year,rev,cogs,op,ni,cfo,capex,assets,liabilities,equity,cash,debt,ar,inv in rows:
        dividends=20
        values=dict(revenue=rev,cost_of_sales=cogs,gross_profit=rev-cogs,operating_profit=op,
          net_income=ni,parent_net_income=ni,assets=assets,liabilities=liabilities,equity=equity,parent_equity=equity,
          current_assets=cash+ar+inv,current_liabilities=round(liabilities*.65),cash=cash,receivables=ar,inventory=inv,
          cfo=cfo,cfi=-capex,cff=cash-previous_cash-cfo+capex,fx_effect=0,other_cash_effects=0,
          cash_beginning=previous_cash,capex_ppe=capex-5,capex_intangible=5,borrowings=debt,lease_liabilities=20,
          interest_expense=18 if year==2025 else 10,oci=0,dividends_paid=dividends,equity_dividends=dividends,
          equity_beginning=previous_equity,equity_other_changes=equity-previous_equity-ni+dividends)
        p=_period(year,values)
        if dataset.periods:
            p.comparatives=deepcopy(dataset.periods[-1].facts)
            for f in p.comparatives.values():
                f.source_id=p.filing_id
                f.source_field='frmtrm_amount'
        dataset.periods.append(p)
        previous_cash,previous_equity=cash,equity
    annual=dataset.periods[-1]
    halfvals={k:f.amount/D('100000000') for k,f in annual.facts.items()}
    for k in halfvals:
        if k not in BS: halfvals[k] *= D('0.5')
    halfvals.update(revenue=640,cost_of_sales=500,gross_profit=140,operating_profit=52,net_income=40,parent_net_income=40,
      assets=1080,liabilities=565,equity=515,parent_equity=515,cash=110,current_assets=550,current_liabilities=370,
      receivables=235,inventory=190,borrowings=350,cfo=30,cfi=-45,cff=25,fx_effect=0,other_cash_effects=0,
      cash_beginning=100,capex_ppe=40,capex_intangible=5,dividends_paid=10,equity_dividends=10,equity_beginning=480,equity_other_changes=5,oci=0)
    half=_period(2026,halfvals,'YTD','2026-06-30')
    oldhalf=deepcopy(halfvals)
    oldhalf.update(revenue=580,cost_of_sales=440,gross_profit=140,operating_profit=55,net_income=43,parent_net_income=43,
      assets=920,liabilities=450,equity=470,parent_equity=470,cash=95,receivables=180,inventory=145,
      cfo=28,cfi=-35,cff=12,cash_beginning=90,equity_beginning=450,equity_dividends=10,equity_other_changes=-13,
      capex_ppe=30,capex_intangible=5)
    half.comparatives=_period(2025,oldhalf,'YTD','2025-06-30').facts
    for f in half.comparatives.values():
        f.source_id=half.filing_id; f.source_field='frmtrm_add_amount'
    dataset.periods.append(half)
    if scenario=='restatement':
        for k in ['equity','parent_equity']:
            annual.comparatives[k].amount=D('44000000000')
        annual.comparatives['assets'].amount=D('84000000000')
        annual.facts['equity_beginning'].amount=D('44000000000')
        annual.facts['equity_other_changes'].amount+=D('1000000000')
        annual.issues.append('검증 시나리오: 2024년 비교 자본·자산이 후속 공시에서 재작성됨')
    elif scenario=='missing':
        half.facts['fx_effect'].amount=None
        half.facts['fx_effect'].reason='가상 시나리오: 환율변동효과 미확보'
    elif scenario=='cash_mismatch':
        half.facts['cash'].amount+=D('500000000')
        half.issues.append('검증 시나리오: 기말 현금에 5억 원 불일치를 주입함')
    elif scenario!='normal':
        raise ValueError('알 수 없는 검증 시나리오입니다.')
    dataset.notes=[{'topic':t,'status':'가상 검증 자료','excerpt':'실제 주석 원문은 미확보입니다. 실제 기업 분석에서는 관련 공시 원문을 확인해야 합니다.',
                    'source_id':'DEMO-2025-FY','source_url':'','location':'가상 자료 — 원문 공시 없음'}
                   for t in ['감사의견','차입금·유동성','채권·재고','손상·무형자산','특수관계자·우발사항']]
    _sync_raw(dataset)
    return dataset

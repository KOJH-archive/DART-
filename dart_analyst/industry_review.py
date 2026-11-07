"""Industry background and questions, keyed to OpenDART industry codes."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewLens:
    title: str
    keys: tuple[str, str]
    background: str
    question: str


_PROFILES = (
    (("64992", "71520"), ReviewLens("지주회사 · 연결 범위", ("operating_profit", "net_income"),
        "연결 이익은 자회사 실적과 편입·제외, 지분법 및 처분손익에 영향을 받을 수 있습니다.",
        "사업부문과 종속기업 변동 주석에서 자회사 실적과 연결 범위 변동의 영향을 구분할 수 있나요?")),
    (("641",), ReviewLens("은행 · 이자손익과 신용비용", ("operating_profit", "net_income"),
        "은행 수익은 조달비용과 대출 수익률의 차이, 수수료, 신용손실 비용 등에 영향을 받습니다.",
        "순이자손익과 대손충당금 전입액 중 어느 항목이 이익 변동을 설명하는지 공시에서 확인할 수 있나요?")),
    (("65",), ReviewLens("보험 · 보험손익과 투자손익", ("operating_profit", "net_income"),
        "보험서비스 결과와 투자·보험금융손익은 서로 다르게 움직일 수 있습니다.",
        "보험서비스손익과 투자·보험금융손익의 변화 중 전체 이익에 더 크게 반영된 항목은 무엇인가요?")),
    (("64", "66"), ReviewLens("금융 · 수수료와 평가손익", ("operating_profit", "net_income"),
        "금융사의 이익에는 수수료, 이자손익, 금융상품 평가손익이 함께 반영될 수 있습니다.",
        "반복되는 수익원과 평가·처분손익을 손익 주석에서 구분할 수 있나요?")),
    (("261",), ReviewLens("반도체 · 제품 구성과 생산능력", ("revenue", "operating_profit"),
        "제품 가격과 고부가 제품 비중, 가동률과 감가상각은 매출과 영업이익에 서로 다른 영향을 줄 수 있습니다.",
        "제품별 매출, 생산설비 가동률, 감가상각 공시 중 어느 근거로 매출과 이익의 움직임을 설명할 수 있나요?")),
    (("26",), ReviewLens("전자 · 제품 구성과 원가", ("revenue", "operating_profit"),
        "제품 구성, 부품 원가와 생산 가동률이 변하면 매출과 영업이익의 증가 속도가 달라질 수 있습니다.",
        "사업부문별 매출·이익 및 원가 주석에서 변화가 집중된 부문을 확인할 수 있나요?")),
    (("30",), ReviewLens("자동차 · 판매 구성과 비용", ("revenue", "operating_profit"),
        "차종·지역별 판매 구성, 판매 인센티브와 보증비용이 수익성에 영향을 줄 수 있습니다.",
        "지역·차종별 판매와 판매비·보증충당부채 주석에서 이익 변동의 단서를 확인할 수 있나요?")),
    (("45", "46", "47"), ReviewLens("유통 · 재고와 현금", ("operating_profit", "cfo"),
        "재고 매입과 공급업체 결제 시점이 손익과 별개로 영업현금흐름을 움직일 수 있습니다.",
        "재고 구성과 매입채무 변동을 함께 보면 현금흐름 변화의 원인을 좁힐 수 있나요?")),
    (("49", "50", "51", "52"), ReviewLens("운송·물류 · 물동량과 운임", ("revenue", "operating_profit"),
        "물동량, 운임, 연료비와 운송수단 가동률의 변화가 운송·물류 이익에 영향을 줄 수 있습니다.",
        "운송 부문별 물동량·운임과 연료·운송비 자료에서 매출과 이익의 움직임을 설명할 수 있나요?")),
    (("20",), ReviewLens("화학 · 판매가격과 원재료", ("revenue", "operating_profit"),
        "제품 판매가격과 원재료 가격의 차이, 설비 가동률이 화학 제조 이익에 영향을 줄 수 있습니다.",
        "사업부문별 이익과 주요 제품·원재료 가격 공시에서 가격차와 가동률의 영향을 구분할 수 있나요?")),
    (("24",), ReviewLens("금속 · 판매가격과 가동률", ("revenue", "operating_profit"),
        "금속 제품 가격, 원료·에너지 비용과 설비 가동률이 매출과 영업이익에 서로 다른 영향을 줄 수 있습니다.",
        "주요 제품·원재료 가격과 생산량, 사업부문별 이익 자료에서 변화가 집중된 부문을 확인할 수 있나요?")),
    (("10", "11"), ReviewLens("식음료 · 판매 구성과 원가", ("revenue", "operating_profit"),
        "제품별 판매 구성, 원재료 가격과 물류·판매비용이 매출과 영업이익에 영향을 줄 수 있습니다.",
        "사업부문별 실적과 주요 원재료 가격, 판매관리비에서 이익 변동의 단서를 확인할 수 있나요?")),
    (("311", "41", "42"), ReviewLens("수주 산업 · 공정과 원가", ("operating_profit", "cfo"),
        "장기 계약의 진행률과 총예정원가 변경, 청구와 수금 시차가 손익과 현금에 다르게 반영될 수 있습니다.",
        "수주잔고, 계약자산 및 총예정원가 변경 주석에서 이익과 현금 변화의 단서를 확인할 수 있나요?")),
    (("58", "59", "60", "61", "62", "63"), ReviewLens("정보서비스 · 계약과 비용", ("revenue", "operating_profit"),
        "서비스별 반복매출 비중, 계약 인식 시점과 인건비·콘텐츠 비용이 실적에 영향을 줄 수 있습니다.",
        "서비스별 매출 구성과 주요 비용 변동으로 매출과 이익의 움직임을 설명할 수 있나요?")),
)

_PROFIT = ReviewLens("매출과 영업이익", ("revenue", "operating_profit"),
    "같은 매출 변동이라도 원가와 판매관리비에 따라 이익의 변화 폭이 달라질 수 있습니다.",
    "매출원가와 판매관리비 중 어느 항목이 영업이익 변동에 더 크게 반영됐나요?")
_CASH = ReviewLens("손익과 영업현금", ("net_income", "cfo"),
    "순이익과 영업현금흐름의 차이에는 비현금 손익, 운전자본과 납부 시점이 반영될 수 있습니다.",
    "현금흐름표와 관련 주석에서 비현금 조정과 운전자본 변동을 구분할 수 있나요?")
_CAPITAL = ReviewLens("이익과 자본", ("net_income", "equity"),
    "기말 자본에는 이익 외에도 배당, 기타포괄손익과 자본거래가 반영될 수 있습니다.",
    "자본변동표에서 순이익, 배당 및 기타포괄손익의 영향을 각각 확인할 수 있나요?")


def review_lenses(industry_code: str) -> tuple[ReviewLens, ...]:
    profile = next((lens for prefixes, lens in _PROFILES if industry_code.startswith(prefixes)), None)
    general = (_CAPITAL,) if industry_code.startswith(("64", "65", "66")) else (_PROFIT, _CASH, _CAPITAL)
    if profile is None:
        return general
    return (profile, *(lens for lens in general if lens.keys != profile.keys))

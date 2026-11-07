# 가상기업 A 재무·회계 분석

가상 검증 데이터 · 실제 기업 아님 · CFS

## 검토 요약

- 가상 기업의 검증용 데이터입니다. 실제 DART 기업 분석 결과가 아닙니다.
- 2025 연간: 2024-01-01~2024-12-31 (현재 공시 비교값) 대비 매출액 1,000 억 원 → 1,200 억 원 (증감률 20 %); 영업이익 100 억 원 → 108 억 원 (증감률 8 %)입니다. [근거: DEMO-2025-FY · revenue, operating_profit]
- 2025 연간: 2024-01-01~2024-12-31 (현재 공시 비교값) 대비 영업현금흐름 70 억 원 → 45 억 원 (증감률 -35.71 %)입니다. [근거: DEMO-2025-FY · cfo]
- 2025 연간: 영업이익률 2024 10 % → 9 %; 순이익 현금 전환 2024 0.88 배 → 0.5 배; 현금 취득액 차감 FCF 2024 20 억 원 → -35 억 원입니다. [근거: DEMO-2025-FY, DEMO-2024-FY · operating_margin, cfo_to_net_income, fcf]
- 2025 연간: DSO (총매출 근사치) 2024 43.92 일 → 54.75 일; DIO 2024 48.8 일 → 56.91 일입니다. 매출채권·재고의 회수 및 소진 변화는 관련 주석과 함께 확인하세요. [근거: DEMO-2025-FY, DEMO-2024-FY · dso, dio]
- 2026 H1 누적: 2025-01-01~2025-06-30 (현재 공시 비교값) 대비 매출액 580 억 원 → 640 억 원 (증감률 10.34 %); 영업이익 55 억 원 → 52 억 원 (증감률 -5.45 %)입니다. [근거: DEMO-2026-YTD · revenue, operating_profit]
- 2026 H1 누적: 2025-01-01~2025-06-30 (현재 공시 비교값) 대비 영업현금흐름 28 억 원 → 30 억 원 (증감률 7.14 %)입니다. [근거: DEMO-2026-YTD · cfo]
- 2026 H1 누적: 영업이익률 8.12 %; 순이익 현금 전환 0.75 배; 현금 취득액 차감 FCF -15 억 원입니다. [근거: DEMO-2026-YTD · operating_margin, cfo_to_net_income, fcf]
- 2026 H1 누적: DSO (총매출 근사치) 64.34 일; DIO 65.16 일입니다. 매출채권·재고의 회수 및 소진 변화는 관련 주석과 함께 확인하세요. [근거: DEMO-2026-YTD, DEMO-2025-FY · dso, dio]
- 검증 시나리오: 2024년 비교 자본·자산이 후속 공시에서 재작성됨

## 자료 범위·처리 현황

| 항목 | 내용 |
| --- | --- |
| 회사 | 가상기업 A |
| 데이터 유형 | 가상 검증 데이터 · 실제 기업 아님 |
| 연결범위 | CFS |
| 처리 현황 | {&quot;periods&quot;: 6, &quot;metric_statuses&quot;: {&quot;missing_source&quot;: 6, &quot;calculated&quot;: 88, &quot;not_applicable&quot;: 2}, &quot;check_statuses&quot;: {&quot;pass&quot;: 24, &quot;fail&quot;: 0, &quot;incomplete&quot;: 0, &quot;not_comparable&quot;: 0}, &quot;status&quot;: &quot;partial&quot;, &quot;issues&quot;: [], &quot;note&quot;: &quot;공시 원천 계정·주석 전체를 빠짐없이 검증했다는 보증이 아닙니다.&quot;} |
| 자료 메타데이터 | {&quot;scenario&quot;: &quot;restatement&quot;, &quot;notice&quot;: &quot;모든 숫자와 메모는 검증용 가상 데이터입니다. 실제 DART 공시를 조회하지 않았습니다.&quot;} |
| 표시 단위 | 비교·대조 금액은 통화 기본 단위, 변화율은 %. 요약만 소수 둘째 자리 반올림; KRW 금액은 억 원 표시. |
| 2021 | {&quot;시작&quot;: &quot;2021-01-01&quot;, &quot;종료&quot;: &quot;2021-12-31&quot;, &quot;기간&quot;: &quot;FY&quot;, &quot;연결범위&quot;: &quot;CFS&quot;, &quot;공시&quot;: &quot;DEMO-2021-FY&quot;, &quot;이슈&quot;: []} |
| 2022 | {&quot;시작&quot;: &quot;2022-01-01&quot;, &quot;종료&quot;: &quot;2022-12-31&quot;, &quot;기간&quot;: &quot;FY&quot;, &quot;연결범위&quot;: &quot;CFS&quot;, &quot;공시&quot;: &quot;DEMO-2022-FY&quot;, &quot;이슈&quot;: []} |
| 2023 | {&quot;시작&quot;: &quot;2023-01-01&quot;, &quot;종료&quot;: &quot;2023-12-31&quot;, &quot;기간&quot;: &quot;FY&quot;, &quot;연결범위&quot;: &quot;CFS&quot;, &quot;공시&quot;: &quot;DEMO-2023-FY&quot;, &quot;이슈&quot;: []} |
| 2024 | {&quot;시작&quot;: &quot;2024-01-01&quot;, &quot;종료&quot;: &quot;2024-12-31&quot;, &quot;기간&quot;: &quot;FY&quot;, &quot;연결범위&quot;: &quot;CFS&quot;, &quot;공시&quot;: &quot;DEMO-2024-FY&quot;, &quot;이슈&quot;: []} |
| 2025 | {&quot;시작&quot;: &quot;2025-01-01&quot;, &quot;종료&quot;: &quot;2025-12-31&quot;, &quot;기간&quot;: &quot;FY&quot;, &quot;연결범위&quot;: &quot;CFS&quot;, &quot;공시&quot;: &quot;DEMO-2025-FY&quot;, &quot;이슈&quot;: [&quot;검증 시나리오: 2024년 비교 자본·자산이 후속 공시에서 재작성됨&quot;]} |
| 2026 H1 | {&quot;시작&quot;: &quot;2026-01-01&quot;, &quot;종료&quot;: &quot;2026-06-30&quot;, &quot;기간&quot;: &quot;YTD&quot;, &quot;연결범위&quot;: &quot;CFS&quot;, &quot;공시&quot;: &quot;DEMO-2026-YTD&quot;, &quot;이슈&quot;: []} |

## 핵심 지표

| 기간 | 지표 | 값 | 단위 | 상태 | 계산식 | 출처 | 계산 제한 사유 | 입력 계정 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021 | 전년 동기 매출 성장률 | N/A | % | missing_source | (당기 매출 / 전년 동일 기간 매출 − 1) × 100 | [] | 전년 동일 기간 비교값 미확보 | [&quot;revenue&quot;, &quot;previous:revenue&quot;] |
| 2021 | 매출총이익률 | 25.00 | % | calculated | 매출총이익 / 매출 × 100 | [&quot;DEMO-2021-FY&quot;] |  | [&quot;gross_profit&quot;, &quot;revenue&quot;] |
| 2021 | 영업이익률 | 7.00 | % | calculated | 영업이익 / 매출 × 100 | [&quot;DEMO-2021-FY&quot;] |  | [&quot;operating_profit&quot;, &quot;revenue&quot;] |
| 2021 | 전체 순이익률 | 5.00 | % | calculated | 전체 순이익 / 매출 × 100 | [&quot;DEMO-2021-FY&quot;] |  | [&quot;net_income&quot;, &quot;revenue&quot;] |
| 2021 | 유동비율 | 117.2839506172839506172839506172840 | % | calculated | 유동자산 / 유동부채 × 100 | [&quot;DEMO-2021-FY&quot;] |  | [&quot;current_assets&quot;, &quot;current_liabilities&quot;] |
| 2021 | 부채비율 | 83.33333333333333333333333333333333 | % | calculated | 총부채 / 총자본 × 100 | [&quot;DEMO-2021-FY&quot;] |  | [&quot;liabilities&quot;, &quot;equity&quot;] |
| 2021 | 순이익 현금 전환 | 1.333333333333333333333333333333333 | 배 | calculated | 영업현금흐름 / 전체 순이익 | [&quot;DEMO-2021-FY&quot;] |  | [&quot;cfo&quot;, &quot;net_income&quot;] |
| 2021 | 이자보상배율 | 4.2 | 배 | calculated | 영업이익 / 총이자비용 | [&quot;DEMO-2021-FY&quot;] |  | [&quot;operating_profit&quot;, &quot;interest_expense&quot;] |
| 2021 | 공시 차입금 − 현금 (리스 포함 여부 확인 필요) | 8000000000 | KRW | calculated | 공시 차입금 − 현금및현금성자산; 리스 포함 여부는 원천 정의 확인 | [&quot;DEMO-2021-FY&quot;] |  | [&quot;borrowings&quot;, &quot;cash&quot;] |
| 2021 | 현금 CAPEX | 3000000000 | KRW | calculated | 유형·무형자산 현금 취득액 합계 | [&quot;DEMO-2021-FY&quot;] |  | [&quot;capex_ppe&quot;, &quot;capex_intangible&quot;] |
| 2021 | 현금 취득액 차감 FCF | 1000000000 | KRW | calculated | CFO − 유형 현금 취득 − 무형 현금 취득 | [&quot;DEMO-2021-FY&quot;] |  | [&quot;cfo&quot;, &quot;capex_ppe&quot;, &quot;capex_intangible&quot;] |
| 2021 | 지배주주 ROE | N/A | % | missing_source | 지배주주 순이익 / 평균 지배주주지분 × 100 | [] | parent_equity: 비교 가능한 기초잔액 미확보 | [&quot;parent_net_income&quot;, &quot;opening:parent_equity&quot;, &quot;parent_equity&quot;] |
| 2021 | ROA | N/A | % | missing_source | 전체 순이익 / 평균 총자산 × 100 | [] | assets: 비교 가능한 기초잔액 미확보 | [&quot;net_income&quot;, &quot;opening:assets&quot;, &quot;assets&quot;] |
| 2021 | DSO (총매출 근사치) | N/A | 일 | missing_source | 평균 순매출채권 / 매출액 × 기간 일수 | [] | receivables: 비교 가능한 기초잔액 미확보 | [&quot;revenue&quot;, &quot;opening:receivables&quot;, &quot;receivables&quot;] |
| 2021 | DIO | N/A | 일 | missing_source | 평균 재고자산 / 매출원가 × 기간 일수 | [] | inventory: 비교 가능한 기초잔액 미확보 | [&quot;cost_of_sales&quot;, &quot;opening:inventory&quot;, &quot;inventory&quot;] |
| 2021 | 현금흐름식 발생액 지표 | N/A | % | missing_source | (전체 순이익 − CFO) / 평균 총자산 × 100 | [] | assets: 비교 가능한 기초잔액 미확보 | [&quot;net_income&quot;, &quot;cfo&quot;, &quot;opening:assets&quot;, &quot;assets&quot;] |
| 2022 | 전년 동기 매출 성장률 | 16.66666666666666666666666666666670 | % | calculated | (당기 매출 / 전년 동일 기간 매출 − 1) × 100 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;revenue&quot;, &quot;previous:revenue&quot;] |
| 2022 | 매출총이익률 | 25.00 | % | calculated | 매출총이익 / 매출 × 100 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;gross_profit&quot;, &quot;revenue&quot;] |
| 2022 | 영업이익률 | 7.00 | % | calculated | 영업이익 / 매출 × 100 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;operating_profit&quot;, &quot;revenue&quot;] |
| 2022 | 전체 순이익률 | 5.142857142857142857142857142857143 | % | calculated | 전체 순이익 / 매출 × 100 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;net_income&quot;, &quot;revenue&quot;] |
| 2022 | 유동비율 | 127.8409090909090909090909090909091 | % | calculated | 유동자산 / 유동부채 × 100 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;current_assets&quot;, &quot;current_liabilities&quot;] |
| 2022 | 부채비율 | 77.14285714285714285714285714285714 | % | calculated | 총부채 / 총자본 × 100 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;liabilities&quot;, &quot;equity&quot;] |
| 2022 | 순이익 현금 전환 | 1.388888888888888888888888888888889 | 배 | calculated | 영업현금흐름 / 전체 순이익 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;cfo&quot;, &quot;net_income&quot;] |
| 2022 | 이자보상배율 | 4.9 | 배 | calculated | 영업이익 / 총이자비용 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;operating_profit&quot;, &quot;interest_expense&quot;] |
| 2022 | 공시 차입금 − 현금 (리스 포함 여부 확인 필요) | 9000000000 | KRW | calculated | 공시 차입금 − 현금및현금성자산; 리스 포함 여부는 원천 정의 확인 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;borrowings&quot;, &quot;cash&quot;] |
| 2022 | 현금 CAPEX | 3500000000 | KRW | calculated | 유형·무형자산 현금 취득액 합계 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;capex_ppe&quot;, &quot;capex_intangible&quot;] |
| 2022 | 현금 취득액 차감 FCF | 1500000000 | KRW | calculated | CFO − 유형 현금 취득 − 무형 현금 취득 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;cfo&quot;, &quot;capex_ppe&quot;, &quot;capex_intangible&quot;] |
| 2022 | 지배주주 ROE | 11.07692307692307692307692307692308 | % | calculated | 지배주주 순이익 / 평균 지배주주지분 × 100 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;parent_net_income&quot;, &quot;opening:parent_equity&quot;, &quot;parent_equity&quot;] |
| 2022 | ROA | 6.153846153846153846153846153846154 | % | calculated | 전체 순이익 / 평균 총자산 × 100 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;net_income&quot;, &quot;opening:assets&quot;, &quot;assets&quot;] |
| 2022 | DSO (총매출 근사치) | 40.41071428571428571428571428571428 | 일 | calculated | 평균 순매출채권 / 매출액 × 기간 일수 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;revenue&quot;, &quot;opening:receivables&quot;, &quot;receivables&quot;] |
| 2022 | DIO | 45.19047619047619047619047619047619 | 일 | calculated | 평균 재고자산 / 매출원가 × 기간 일수 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;cost_of_sales&quot;, &quot;opening:inventory&quot;, &quot;inventory&quot;] |
| 2022 | 현금흐름식 발생액 지표 | -2.393162393162393162393162393162393 | % | calculated | (전체 순이익 − CFO) / 평균 총자산 × 100 | [&quot;DEMO-2022-FY&quot;] |  | [&quot;net_income&quot;, &quot;cfo&quot;, &quot;opening:assets&quot;, &quot;assets&quot;] |
| 2023 | 전년 동기 매출 성장률 | 14.28571428571428571428571428571430 | % | calculated | (당기 매출 / 전년 동일 기간 매출 − 1) × 100 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;revenue&quot;, &quot;previous:revenue&quot;] |
| 2023 | 매출총이익률 | 25.00 | % | calculated | 매출총이익 / 매출 × 100 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;gross_profit&quot;, &quot;revenue&quot;] |
| 2023 | 영업이익률 | 8.00 | % | calculated | 영업이익 / 매출 × 100 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;operating_profit&quot;, &quot;revenue&quot;] |
| 2023 | 전체 순이익률 | 6.00 | % | calculated | 전체 순이익 / 매출 × 100 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;net_income&quot;, &quot;revenue&quot;] |
| 2023 | 유동비율 | 133.3333333333333333333333333333333 | % | calculated | 유동자산 / 유동부채 × 100 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;current_assets&quot;, &quot;current_liabilities&quot;] |
| 2023 | 부채비율 | 75.00 | % | calculated | 총부채 / 총자본 × 100 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;liabilities&quot;, &quot;equity&quot;] |
| 2023 | 순이익 현금 전환 | 1.25 | 배 | calculated | 영업현금흐름 / 전체 순이익 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;cfo&quot;, &quot;net_income&quot;] |
| 2023 | 이자보상배율 | 6.4 | 배 | calculated | 영업이익 / 총이자비용 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;operating_profit&quot;, &quot;interest_expense&quot;] |
| 2023 | 공시 차입금 − 현금 (리스 포함 여부 확인 필요) | 10000000000 | KRW | calculated | 공시 차입금 − 현금및현금성자산; 리스 포함 여부는 원천 정의 확인 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;borrowings&quot;, &quot;cash&quot;] |
| 2023 | 현금 CAPEX | 4000000000 | KRW | calculated | 유형·무형자산 현금 취득액 합계 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;capex_ppe&quot;, &quot;capex_intangible&quot;] |
| 2023 | 현금 취득액 차감 FCF | 2000000000 | KRW | calculated | CFO − 유형 현금 취득 − 무형 현금 취득 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;cfo&quot;, &quot;capex_ppe&quot;, &quot;capex_intangible&quot;] |
| 2023 | 지배주주 ROE | 12.800 | % | calculated | 지배주주 순이익 / 평균 지배주주지분 × 100 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;parent_net_income&quot;, &quot;opening:parent_equity&quot;, &quot;parent_equity&quot;] |
| 2023 | ROA | 7.272727272727272727272727272727273 | % | calculated | 전체 순이익 / 평균 총자산 × 100 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;net_income&quot;, &quot;opening:assets&quot;, &quot;assets&quot;] |
| 2023 | DSO (총매출 근사치) | 42.203125 | 일 | calculated | 평균 순매출채권 / 매출액 × 기간 일수 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;revenue&quot;, &quot;opening:receivables&quot;, &quot;receivables&quot;] |
| 2023 | DIO | 45.625 | 일 | calculated | 평균 재고자산 / 매출원가 × 기간 일수 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;cost_of_sales&quot;, &quot;opening:inventory&quot;, &quot;inventory&quot;] |
| 2023 | 현금흐름식 발생액 지표 | -1.818181818181818181818181818181818 | % | calculated | (전체 순이익 − CFO) / 평균 총자산 × 100 | [&quot;DEMO-2023-FY&quot;] |  | [&quot;net_income&quot;, &quot;cfo&quot;, &quot;opening:assets&quot;, &quot;assets&quot;] |
| 2024 | 전년 동기 매출 성장률 | 25.00 | % | calculated | (당기 매출 / 전년 동일 기간 매출 − 1) × 100 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;revenue&quot;, &quot;previous:revenue&quot;] |
| 2024 | 매출총이익률 | 25.00 | % | calculated | 매출총이익 / 매출 × 100 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;gross_profit&quot;, &quot;revenue&quot;] |
| 2024 | 영업이익률 | 10.0 | % | calculated | 영업이익 / 매출 × 100 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;operating_profit&quot;, &quot;revenue&quot;] |
| 2024 | 전체 순이익률 | 8.00 | % | calculated | 전체 순이익 / 매출 × 100 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;net_income&quot;, &quot;revenue&quot;] |
| 2024 | 유동비율 | 134.6153846153846153846153846153846 | % | calculated | 유동자산 / 유동부채 × 100 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;current_assets&quot;, &quot;current_liabilities&quot;] |
| 2024 | 부채비율 | 88.88888888888888888888888888888889 | % | calculated | 총부채 / 총자본 × 100 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;liabilities&quot;, &quot;equity&quot;] |
| 2024 | 순이익 현금 전환 | 0.875 | 배 | calculated | 영업현금흐름 / 전체 순이익 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;cfo&quot;, &quot;net_income&quot;] |
| 2024 | 이자보상배율 | 10 | 배 | calculated | 영업이익 / 총이자비용 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;operating_profit&quot;, &quot;interest_expense&quot;] |
| 2024 | 공시 차입금 − 현금 (리스 포함 여부 확인 필요) | 14000000000 | KRW | calculated | 공시 차입금 − 현금및현금성자산; 리스 포함 여부는 원천 정의 확인 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;borrowings&quot;, &quot;cash&quot;] |
| 2024 | 현금 CAPEX | 5000000000 | KRW | calculated | 유형·무형자산 현금 취득액 합계 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;capex_ppe&quot;, &quot;capex_intangible&quot;] |
| 2024 | 현금 취득액 차감 FCF | 2000000000 | KRW | calculated | CFO − 유형 현금 취득 − 무형 현금 취득 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;cfo&quot;, &quot;capex_ppe&quot;, &quot;capex_intangible&quot;] |
| 2024 | 지배주주 ROE | 18.82352941176470588235294117647059 | % | calculated | 지배주주 순이익 / 평균 지배주주지분 × 100 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;parent_net_income&quot;, &quot;opening:parent_equity&quot;, &quot;parent_equity&quot;] |
| 2024 | ROA | 10.32258064516129032258064516129032 | % | calculated | 전체 순이익 / 평균 총자산 × 100 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;net_income&quot;, &quot;opening:assets&quot;, &quot;assets&quot;] |
| 2024 | DSO (총매출 근사치) | 43.92 | 일 | calculated | 평균 순매출채권 / 매출액 × 기간 일수 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;revenue&quot;, &quot;opening:receivables&quot;, &quot;receivables&quot;] |
| 2024 | DIO | 48.79999999999999999999999999999999 | 일 | calculated | 평균 재고자산 / 매출원가 × 기간 일수 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;cost_of_sales&quot;, &quot;opening:inventory&quot;, &quot;inventory&quot;] |
| 2024 | 현금흐름식 발생액 지표 | 1.290322580645161290322580645161290 | % | calculated | (전체 순이익 − CFO) / 평균 총자산 × 100 | [&quot;DEMO-2024-FY&quot;] |  | [&quot;net_income&quot;, &quot;cfo&quot;, &quot;opening:assets&quot;, &quot;assets&quot;] |
| 2025 | 전년 동기 매출 성장률 | 20.0 | % | calculated | (당기 매출 / 전년 동일 기간 매출 − 1) × 100 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;revenue&quot;, &quot;previous:revenue&quot;] |
| 2025 | 매출총이익률 | 22.500 | % | calculated | 매출총이익 / 매출 × 100 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;gross_profit&quot;, &quot;revenue&quot;] |
| 2025 | 영업이익률 | 9.00 | % | calculated | 영업이익 / 매출 × 100 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;operating_profit&quot;, &quot;revenue&quot;] |
| 2025 | 전체 순이익률 | 7.500 | % | calculated | 전체 순이익 / 매출 × 100 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;net_income&quot;, &quot;revenue&quot;] |
| 2025 | 유동비율 | 144.9704142011834319526627218934911 | % | calculated | 유동자산 / 유동부채 × 100 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;current_assets&quot;, &quot;current_liabilities&quot;] |
| 2025 | 부채비율 | 108.3333333333333333333333333333333 | % | calculated | 총부채 / 총자본 × 100 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;liabilities&quot;, &quot;equity&quot;] |
| 2025 | 순이익 현금 전환 | 0.5 | 배 | calculated | 영업현금흐름 / 전체 순이익 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;cfo&quot;, &quot;net_income&quot;] |
| 2025 | 이자보상배율 | 6 | 배 | calculated | 영업이익 / 총이자비용 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;operating_profit&quot;, &quot;interest_expense&quot;] |
| 2025 | 공시 차입금 − 현금 (리스 포함 여부 확인 필요) | 22000000000 | KRW | calculated | 공시 차입금 − 현금및현금성자산; 리스 포함 여부는 원천 정의 확인 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;borrowings&quot;, &quot;cash&quot;] |
| 2025 | 현금 CAPEX | 8000000000 | KRW | calculated | 유형·무형자산 현금 취득액 합계 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;capex_ppe&quot;, &quot;capex_intangible&quot;] |
| 2025 | 현금 취득액 차감 FCF | -3500000000 | KRW | calculated | CFO − 유형 현금 취득 − 무형 현금 취득 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;cfo&quot;, &quot;capex_ppe&quot;, &quot;capex_intangible&quot;] |
| 2025 | 지배주주 ROE | 19.56521739130434782608695652173913 | % | calculated | 지배주주 순이익 / 평균 지배주주지분 × 100 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;parent_net_income&quot;, &quot;opening:parent_equity&quot;, &quot;parent_equity&quot;] |
| 2025 | ROA | 9.782608695652173913043478260869565 | % | calculated | 전체 순이익 / 평균 총자산 × 100 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;net_income&quot;, &quot;opening:assets&quot;, &quot;assets&quot;] |
| 2025 | DSO (총매출 근사치) | 54.75 | 일 | calculated | 평균 순매출채권 / 매출액 × 기간 일수 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;revenue&quot;, &quot;opening:receivables&quot;, &quot;receivables&quot;] |
| 2025 | DIO | 56.90860215053763440860215053763440 | 일 | calculated | 평균 재고자산 / 매출원가 × 기간 일수 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;cost_of_sales&quot;, &quot;opening:inventory&quot;, &quot;inventory&quot;] |
| 2025 | 현금흐름식 발생액 지표 | 4.891304347826086956521739130434783 | % | calculated | (전체 순이익 − CFO) / 평균 총자산 × 100 | [&quot;DEMO-2025-FY&quot;] |  | [&quot;net_income&quot;, &quot;cfo&quot;, &quot;opening:assets&quot;, &quot;assets&quot;] |
| 2026 H1 | 전년 동기 매출 성장률 | 10.34482758620689655172413793103450 | % | calculated | (당기 매출 / 전년 동일 기간 매출 − 1) × 100 | [&quot;DEMO-2026-YTD&quot;] |  | [&quot;revenue&quot;, &quot;previous:revenue&quot;] |
| 2026 H1 | 매출총이익률 | 21.87500 | % | calculated | 매출총이익 / 매출 × 100 | [&quot;DEMO-2026-YTD&quot;] |  | [&quot;gross_profit&quot;, &quot;revenue&quot;] |
| 2026 H1 | 영업이익률 | 8.12500 | % | calculated | 영업이익 / 매출 × 100 | [&quot;DEMO-2026-YTD&quot;] |  | [&quot;operating_profit&quot;, &quot;revenue&quot;] |
| 2026 H1 | 전체 순이익률 | 6.2500 | % | calculated | 전체 순이익 / 매출 × 100 | [&quot;DEMO-2026-YTD&quot;] |  | [&quot;net_income&quot;, &quot;revenue&quot;] |
| 2026 H1 | 유동비율 | 148.6486486486486486486486486486486 | % | calculated | 유동자산 / 유동부채 × 100 | [&quot;DEMO-2026-YTD&quot;] |  | [&quot;current_assets&quot;, &quot;current_liabilities&quot;] |
| 2026 H1 | 부채비율 | 109.7087378640776699029126213592233 | % | calculated | 총부채 / 총자본 × 100 | [&quot;DEMO-2026-YTD&quot;] |  | [&quot;liabilities&quot;, &quot;equity&quot;] |
| 2026 H1 | 순이익 현금 전환 | 0.75 | 배 | calculated | 영업현금흐름 / 전체 순이익 | [&quot;DEMO-2026-YTD&quot;] |  | [&quot;cfo&quot;, &quot;net_income&quot;] |
| 2026 H1 | 이자보상배율 | 5.777777777777777777777777777777778 | 배 | calculated | 영업이익 / 총이자비용 | [&quot;DEMO-2026-YTD&quot;] |  | [&quot;operating_profit&quot;, &quot;interest_expense&quot;] |
| 2026 H1 | 공시 차입금 − 현금 (리스 포함 여부 확인 필요) | 24000000000 | KRW | calculated | 공시 차입금 − 현금및현금성자산; 리스 포함 여부는 원천 정의 확인 | [&quot;DEMO-2026-YTD&quot;] |  | [&quot;borrowings&quot;, &quot;cash&quot;] |
| 2026 H1 | 현금 CAPEX | 4500000000 | KRW | calculated | 유형·무형자산 현금 취득액 합계 | [&quot;DEMO-2026-YTD&quot;] |  | [&quot;capex_ppe&quot;, &quot;capex_intangible&quot;] |
| 2026 H1 | 현금 취득액 차감 FCF | -1500000000 | KRW | calculated | CFO − 유형 현금 취득 − 무형 현금 취득 | [&quot;DEMO-2026-YTD&quot;] |  | [&quot;cfo&quot;, &quot;capex_ppe&quot;, &quot;capex_intangible&quot;] |
| 2026 H1 | 지배주주 ROE | N/A | % | not_applicable | 지배주주 순이익 / 평균 지배주주지분 × 100 | [] | 중간 ROE·ROA는 연율화하지 않고 보류합니다 | [&quot;parent_net_income&quot;, &quot;opening:parent_equity&quot;, &quot;parent_equity&quot;] |
| 2026 H1 | ROA | N/A | % | not_applicable | 전체 순이익 / 평균 총자산 × 100 | [] | 중간 ROE·ROA는 연율화하지 않고 보류합니다 | [&quot;net_income&quot;, &quot;opening:assets&quot;, &quot;assets&quot;] |
| 2026 H1 | DSO (총매출 근사치) | 64.33984375 | 일 | calculated | 평균 순매출채권 / 매출액 × 기간 일수 | [&quot;DEMO-2026-YTD&quot;, &quot;DEMO-2025-FY&quot;] |  | [&quot;revenue&quot;, &quot;opening:receivables&quot;, &quot;receivables&quot;] |
| 2026 H1 | DIO | 65.16 | 일 | calculated | 평균 재고자산 / 매출원가 × 기간 일수 | [&quot;DEMO-2026-YTD&quot;, &quot;DEMO-2025-FY&quot;] |  | [&quot;cost_of_sales&quot;, &quot;opening:inventory&quot;, &quot;inventory&quot;] |
| 2026 H1 | 현금흐름식 발생액 지표 | 0.9615384615384615384615384615384615 | % | calculated | (전체 순이익 − CFO) / 평균 총자산 × 100 | [&quot;DEMO-2026-YTD&quot;, &quot;DEMO-2025-FY&quot;] |  | [&quot;net_income&quot;, &quot;cfo&quot;, &quot;opening:assets&quot;, &quot;assets&quot;] |

## 계정별 과거 비교

| 계정 | 비교기간 | 당기 | 비교금액 | 당기금액 | 차이 | 변화율 (%) | 상태 | 설명 | 출처 | 금액 통화 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 매출액 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 매출원가 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 매출총이익 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 영업이익 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 전체 순이익 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 지배주주 순이익 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 총자산 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 총부채 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 총자본 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 지배주주지분 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 유동자산 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 유동부채 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 현금및현금성자산 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 순매출채권 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 재고자산 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 영업현금흐름 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 투자현금흐름 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 재무현금흐름 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 현금 환율효과 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 기타 현금 조정 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 기초 현금 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 유형자산 현금 취득 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 무형자산 현금 취득 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 공시 차입금 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 리스부채 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 총이자비용 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 기타포괄손익 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 현금 지급 배당 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 기초 자본 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 자본 인식 배당 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 기타 자본 변동 | N/A | 2021 | N/A | N/A | N/A | N/A | missing_source | 전년 동일 기간 비교값 미확보 | [] | KRW |
| 매출액 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 60000000000 | 70000000000 | 10000000000 | 16.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 매출원가 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 45000000000 | 52500000000 | 7500000000 | 16.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 매출총이익 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 15000000000 | 17500000000 | 2500000000 | 16.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 영업이익 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 4200000000 | 4900000000 | 700000000 | 16.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 전체 순이익 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 3000000000 | 3600000000 | 600000000 | 20.0 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 지배주주 순이익 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 3000000000 | 3600000000 | 600000000 | 20.0 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 총자산 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 55000000000 | 62000000000 | 7000000000 | 12.72727272727272727272727272727273 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 총부채 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 25000000000 | 27000000000 | 2000000000 | 8.00 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 총자본 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 30000000000 | 35000000000 | 5000000000 | 16.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 지배주주지분 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 30000000000 | 35000000000 | 5000000000 | 16.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 유동자산 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 19000000000 | 22500000000 | 3500000000 | 18.42105263157894736842105263157895 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 유동부채 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 16200000000 | 17600000000 | 1400000000 | 8.641975308641975308641975308641975 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 현금및현금성자산 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 6000000000 | 7000000000 | 1000000000 | 16.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 순매출채권 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 7000000000 | 8500000000 | 1500000000 | 21.42857142857142857142857142857143 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 재고자산 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 6000000000 | 7000000000 | 1000000000 | 16.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 영업현금흐름 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 4000000000 | 5000000000 | 1000000000 | 25.00 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 투자현금흐름 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | -3000000000 | -3500000000 | -500000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2022-FY&quot;] | KRW |
| 재무현금흐름 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 0 | -500000000 | -500000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2022-FY&quot;] | KRW |
| 현금 환율효과 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2022-FY&quot;] | KRW |
| 기타 현금 조정 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2022-FY&quot;] | KRW |
| 기초 현금 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 5000000000 | 6000000000 | 1000000000 | 20.0 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 유형자산 현금 취득 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 2500000000 | 3000000000 | 500000000 | 20.0 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 무형자산 현금 취득 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 500000000 | 500000000 | 0 | 0 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 공시 차입금 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 14000000000 | 16000000000 | 2000000000 | 14.28571428571428571428571428571429 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 리스부채 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 2000000000 | 2000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 총이자비용 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 1000000000 | 1000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 기타포괄손익 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2022-FY&quot;] | KRW |
| 현금 지급 배당 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 2000000000 | 2000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 기초 자본 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 27000000000 | 30000000000 | 3000000000 | 11.11111111111111111111111111111111 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 자본 인식 배당 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 2000000000 | 2000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 기타 자본 변동 | 2021-01-01~2021-12-31 (현재 공시 비교값) | 2022 | 2000000000 | 3400000000 | 1400000000 | 70.0 | calculated |  | [&quot;DEMO-2022-FY&quot;] | KRW |
| 매출액 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 70000000000 | 80000000000 | 10000000000 | 14.28571428571428571428571428571429 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 매출원가 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 52500000000 | 60000000000 | 7500000000 | 14.28571428571428571428571428571429 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 매출총이익 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 17500000000 | 20000000000 | 2500000000 | 14.28571428571428571428571428571429 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 영업이익 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 4900000000 | 6400000000 | 1500000000 | 30.61224489795918367346938775510204 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 전체 순이익 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 3600000000 | 4800000000 | 1200000000 | 33.33333333333333333333333333333333 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 지배주주 순이익 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 3600000000 | 4800000000 | 1200000000 | 33.33333333333333333333333333333333 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 총자산 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 62000000000 | 70000000000 | 8000000000 | 12.90322580645161290322580645161290 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 총부채 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 27000000000 | 30000000000 | 3000000000 | 11.11111111111111111111111111111111 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 총자본 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 35000000000 | 40000000000 | 5000000000 | 14.28571428571428571428571428571429 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 지배주주지분 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 35000000000 | 40000000000 | 5000000000 | 14.28571428571428571428571428571429 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 유동자산 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 22500000000 | 26000000000 | 3500000000 | 15.55555555555555555555555555555556 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 유동부채 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 17600000000 | 19500000000 | 1900000000 | 10.79545454545454545454545454545455 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 현금및현금성자산 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 7000000000 | 8000000000 | 1000000000 | 14.28571428571428571428571428571429 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 순매출채권 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 8500000000 | 10000000000 | 1500000000 | 17.64705882352941176470588235294118 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 재고자산 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 7000000000 | 8000000000 | 1000000000 | 14.28571428571428571428571428571429 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 영업현금흐름 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 5000000000 | 6000000000 | 1000000000 | 20.0 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 투자현금흐름 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | -3500000000 | -4000000000 | -500000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2023-FY&quot;] | KRW |
| 재무현금흐름 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | -500000000 | -1000000000 | -500000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2023-FY&quot;] | KRW |
| 현금 환율효과 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2023-FY&quot;] | KRW |
| 기타 현금 조정 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2023-FY&quot;] | KRW |
| 기초 현금 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 6000000000 | 7000000000 | 1000000000 | 16.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 유형자산 현금 취득 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 3000000000 | 3500000000 | 500000000 | 16.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 무형자산 현금 취득 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 500000000 | 500000000 | 0 | 0 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 공시 차입금 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 16000000000 | 18000000000 | 2000000000 | 12.500 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 리스부채 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 2000000000 | 2000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 총이자비용 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 1000000000 | 1000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 기타포괄손익 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2023-FY&quot;] | KRW |
| 현금 지급 배당 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 2000000000 | 2000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 기초 자본 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 30000000000 | 35000000000 | 5000000000 | 16.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 자본 인식 배당 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 2000000000 | 2000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 기타 자본 변동 | 2022-01-01~2022-12-31 (현재 공시 비교값) | 2023 | 3400000000 | 2200000000 | -1200000000 | -35.29411764705882352941176470588235 | calculated |  | [&quot;DEMO-2023-FY&quot;] | KRW |
| 매출액 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 80000000000 | 100000000000 | 20000000000 | 25.00 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 매출원가 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 60000000000 | 75000000000 | 15000000000 | 25.00 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 매출총이익 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 20000000000 | 25000000000 | 5000000000 | 25.00 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 영업이익 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 6400000000 | 10000000000 | 3600000000 | 56.2500 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 전체 순이익 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 4800000000 | 8000000000 | 3200000000 | 66.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 지배주주 순이익 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 4800000000 | 8000000000 | 3200000000 | 66.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 총자산 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 70000000000 | 85000000000 | 15000000000 | 21.42857142857142857142857142857143 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 총부채 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 30000000000 | 40000000000 | 10000000000 | 33.33333333333333333333333333333333 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 총자본 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 40000000000 | 45000000000 | 5000000000 | 12.500 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 지배주주지분 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 40000000000 | 45000000000 | 5000000000 | 12.500 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 유동자산 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 26000000000 | 35000000000 | 9000000000 | 34.61538461538461538461538461538462 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 유동부채 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 19500000000 | 26000000000 | 6500000000 | 33.33333333333333333333333333333333 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 현금및현금성자산 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 8000000000 | 9000000000 | 1000000000 | 12.500 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 순매출채권 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 10000000000 | 14000000000 | 4000000000 | 40.0 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 재고자산 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 8000000000 | 12000000000 | 4000000000 | 50.0 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 영업현금흐름 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 6000000000 | 7000000000 | 1000000000 | 16.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 투자현금흐름 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | -4000000000 | -5000000000 | -1000000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2024-FY&quot;] | KRW |
| 재무현금흐름 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | -1000000000 | -1000000000 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2024-FY&quot;] | KRW |
| 현금 환율효과 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2024-FY&quot;] | KRW |
| 기타 현금 조정 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2024-FY&quot;] | KRW |
| 기초 현금 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 7000000000 | 8000000000 | 1000000000 | 14.28571428571428571428571428571429 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 유형자산 현금 취득 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 3500000000 | 4500000000 | 1000000000 | 28.57142857142857142857142857142857 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 무형자산 현금 취득 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 500000000 | 500000000 | 0 | 0 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 공시 차입금 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 18000000000 | 23000000000 | 5000000000 | 27.77777777777777777777777777777778 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 리스부채 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 2000000000 | 2000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 총이자비용 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 1000000000 | 1000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 기타포괄손익 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2024-FY&quot;] | KRW |
| 현금 지급 배당 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 2000000000 | 2000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 기초 자본 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 35000000000 | 40000000000 | 5000000000 | 14.28571428571428571428571428571429 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 자본 인식 배당 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 2000000000 | 2000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 기타 자본 변동 | 2023-01-01~2023-12-31 (현재 공시 비교값) | 2024 | 2200000000 | -1000000000 | -3200000000 | -145.4545454545454545454545454545455 | calculated |  | [&quot;DEMO-2024-FY&quot;] | KRW |
| 매출액 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 100000000000 | 120000000000 | 20000000000 | 20.0 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 매출원가 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 75000000000 | 93000000000 | 18000000000 | 24.00 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 매출총이익 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 25000000000 | 27000000000 | 2000000000 | 8.00 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 영업이익 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 10000000000 | 10800000000 | 800000000 | 8.00 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 전체 순이익 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 8000000000 | 9000000000 | 1000000000 | 12.500 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 지배주주 순이익 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 8000000000 | 9000000000 | 1000000000 | 12.500 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 총자산 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 84000000000 | 100000000000 | 16000000000 | 19.04761904761904761904761904761905 | calculated | 재작성/공시 버전 차이: 현재 공시 비교값 사용 | [&quot;DEMO-2025-FY&quot;] | KRW |
| 총부채 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 40000000000 | 52000000000 | 12000000000 | 30.0 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 총자본 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 44000000000 | 48000000000 | 4000000000 | 9.090909090909090909090909090909091 | calculated | 재작성/공시 버전 차이: 현재 공시 비교값 사용 | [&quot;DEMO-2025-FY&quot;] | KRW |
| 지배주주지분 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 44000000000 | 48000000000 | 4000000000 | 9.090909090909090909090909090909091 | calculated | 재작성/공시 버전 차이: 현재 공시 비교값 사용 | [&quot;DEMO-2025-FY&quot;] | KRW |
| 유동자산 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 35000000000 | 49000000000 | 14000000000 | 40.0 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 유동부채 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 26000000000 | 33800000000 | 7800000000 | 30.0 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 현금및현금성자산 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 9000000000 | 10000000000 | 1000000000 | 11.11111111111111111111111111111111 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 순매출채권 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 14000000000 | 22000000000 | 8000000000 | 57.14285714285714285714285714285714 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 재고자산 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 12000000000 | 17000000000 | 5000000000 | 41.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 영업현금흐름 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 7000000000 | 4500000000 | -2500000000 | -35.71428571428571428571428571428571 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 투자현금흐름 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | -5000000000 | -8000000000 | -3000000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2025-FY&quot;] | KRW |
| 재무현금흐름 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | -1000000000 | 4500000000 | 5500000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2025-FY&quot;] | KRW |
| 현금 환율효과 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2025-FY&quot;] | KRW |
| 기타 현금 조정 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2025-FY&quot;] | KRW |
| 기초 현금 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 8000000000 | 9000000000 | 1000000000 | 12.500 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 유형자산 현금 취득 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 4500000000 | 7500000000 | 3000000000 | 66.66666666666666666666666666666667 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 무형자산 현금 취득 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 500000000 | 500000000 | 0 | 0 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 공시 차입금 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 23000000000 | 32000000000 | 9000000000 | 39.13043478260869565217391304347826 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 리스부채 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 2000000000 | 2000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 총이자비용 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 1000000000 | 1800000000 | 800000000 | 80.0 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 기타포괄손익 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2025-FY&quot;] | KRW |
| 현금 지급 배당 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 2000000000 | 2000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 기초 자본 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 40000000000 | 44000000000 | 4000000000 | 10.0 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 자본 인식 배당 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | 2000000000 | 2000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2025-FY&quot;] | KRW |
| 기타 자본 변동 | 2024-01-01~2024-12-31 (현재 공시 비교값) | 2025 | -1000000000 | -3000000000 | -2000000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2025-FY&quot;] | KRW |
| 매출액 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 58000000000 | 64000000000 | 6000000000 | 10.34482758620689655172413793103448 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 매출원가 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 44000000000 | 50000000000 | 6000000000 | 13.63636363636363636363636363636364 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 매출총이익 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 14000000000 | 14000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 영업이익 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 5500000000 | 5200000000 | -300000000 | -5.454545454545454545454545454545455 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 전체 순이익 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 4300000000 | 4000000000 | -300000000 | -6.976744186046511627906976744186047 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 지배주주 순이익 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 4300000000 | 4000000000 | -300000000 | -6.976744186046511627906976744186047 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 총자산 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 92000000000 | 108000000000 | 16000000000 | 17.39130434782608695652173913043478 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 총부채 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 45000000000 | 56500000000 | 11500000000 | 25.55555555555555555555555555555556 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 총자본 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 47000000000 | 51500000000 | 4500000000 | 9.574468085106382978723404255319149 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 지배주주지분 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 47000000000 | 51500000000 | 4500000000 | 9.574468085106382978723404255319149 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 유동자산 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 55000000000 | 55000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 유동부채 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 37000000000 | 37000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 현금및현금성자산 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 9500000000 | 11000000000 | 1500000000 | 15.78947368421052631578947368421053 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 순매출채권 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 18000000000 | 23500000000 | 5500000000 | 30.55555555555555555555555555555556 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 재고자산 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 14500000000 | 19000000000 | 4500000000 | 31.03448275862068965517241379310345 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 영업현금흐름 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 2800000000 | 3000000000 | 200000000 | 7.142857142857142857142857142857143 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 투자현금흐름 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | -3500000000 | -4500000000 | -1000000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 재무현금흐름 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 1200000000 | 2500000000 | 1300000000 | 108.3333333333333333333333333333333 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 현금 환율효과 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 기타 현금 조정 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 기초 현금 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 9000000000 | 10000000000 | 1000000000 | 11.11111111111111111111111111111111 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 유형자산 현금 취득 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 3000000000 | 4000000000 | 1000000000 | 33.33333333333333333333333333333333 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 무형자산 현금 취득 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 500000000 | 500000000 | 0 | 0 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 공시 차입금 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 35000000000 | 35000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 리스부채 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 2000000000 | 2000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 총이자비용 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 900000000.0 | 900000000.0 | 0.0 | 0 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 기타포괄손익 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 현금 지급 배당 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 1000000000 | 1000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 기초 자본 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 45000000000 | 48000000000 | 3000000000 | 6.666666666666666666666666666666667 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 자본 인식 배당 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | 1000000000 | 1000000000 | 0 | 0 | calculated |  | [&quot;DEMO-2026-YTD&quot;] | KRW |
| 기타 자본 변동 | 2025-01-01~2025-06-30 (현재 공시 비교값) | 2026 H1 | -1300000000 | 500000000 | 1800000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이로 표시 | [&quot;DEMO-2026-YTD&quot;] | KRW |

## 원천 계정 비교 범위

| 항목 | 내용 |
| --- | --- |
| 처리 현황 | {&quot;raw_rows&quot;: 186, &quot;comparison_rows&quot;: 186, &quot;statuses&quot;: {&quot;missing_previous&quot;: 31, &quot;calculated&quot;: 142, &quot;not_comparable&quot;: 13}, &quot;compared&quot;: 142, &quot;restatement_differences&quot;: 3, &quot;status&quot;: &quot;partial&quot;} |
| 비교 제한 | 수집된 전체 계정 행 중 동일한 표준 계정·재무제표·구성원·기간을 확인한 항목만 비교합니다. |
| 비교 제한 | 비표준·회사 확장 계정, 재분류, 중복, 누락과 중간 현금흐름의 기간 불명 항목은 보류합니다. |
| 비교 제한 | 재무제표 전체의 의미상 재분류·분개·주석 완전성을 검증했다는 보증이 아닙니다. |

## 원천 전체 계정 비교

| 공시 계정명 | 계정 ID | 재무제표 | 구성원 | 연결범위 | 분석기간 | 당기 시작일 | 당기 종료일 | 비교기 | 비교 기준 | 금액 통화 | 비교금액 | 당기금액 | 차이 | 변화율 (%) | 상태 | 설명 | 재작성 차이 | 기존 공시 비교금액 | 기존 공시번호 | 기존 계정명 | 당기 원천필드 | 비교 원천필드 | 출처 공시번호 | 원문 1 | 원문 2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 자산총계 | demo:assets | BS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-12-31 | 전기말 잔액 | KRW | N/A | 55000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 차입금(리스 제외) | demo:borrowings | BS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-12-31 | 전기말 잔액 | KRW | N/A | 14000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 현금및현금성자산 | demo:cash | BS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-12-31 | 전기말 잔액 | KRW | N/A | 6000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 유동자산 | demo:current_assets | BS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-12-31 | 전기말 잔액 | KRW | N/A | 19000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 유동부채 | demo:current_liabilities | BS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-12-31 | 전기말 잔액 | KRW | N/A | 16200000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 자본총계 | demo:equity | BS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-12-31 | 전기말 잔액 | KRW | N/A | 30000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 재고자산 | demo:inventory | BS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-12-31 | 전기말 잔액 | KRW | N/A | 6000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 리스부채 | demo:lease_liabilities | BS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-12-31 | 전기말 잔액 | KRW | N/A | 2000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 부채총계 | demo:liabilities | BS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-12-31 | 전기말 잔액 | KRW | N/A | 25000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 지배주주 지분 | demo:parent_equity | BS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-12-31 | 전기말 잔액 | KRW | N/A | 30000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 순매출채권 | demo:receivables | BS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-12-31 | 전기말 잔액 | KRW | N/A | 7000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 무형자산 현금취득 | demo:capex_intangible | CF |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 500000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 유형자산 현금취득 | demo:capex_ppe | CF |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 2500000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 기초 현금 | demo:cash_beginning | CF |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 5000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 재무활동현금흐름 | demo:cff | CF |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 0 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 투자활동현금흐름 | demo:cfi | CF |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | -3000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 영업활동현금흐름 | demo:cfo | CF |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 4000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 현금배당 지급 | demo:dividends_paid | CF |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 2000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 환율변동효과 | demo:fx_effect | CF |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 0 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 기타 현금조정 | demo:other_cash_effects | CF |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 0 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 매출원가 | demo:cost_of_sales | IS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 45000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 매출총이익 | demo:gross_profit | IS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 15000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 총이자비용 | demo:interest_expense | IS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 1000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 전체 당기순이익 | demo:net_income | IS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 3000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 영업이익 | demo:operating_profit | IS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 4200000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 지배주주 순이익 | demo:parent_net_income | IS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 3000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 매출액 | demo:revenue | IS |  | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 60000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 기초 자본 | demo:equity_beginning | SCE | 자본 [member] | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 27000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 자본차감 배당 | demo:equity_dividends | SCE | 자본 [member] | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 2000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 기타 자본변동 | demo:equity_other_changes | SCE | 자본 [member] | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 2000000000 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 기타포괄손익 | demo:oci | SCE | 자본 [member] | CFS | 2021 | 2021-01-01 | 2021-12-31 | 2020-01-01~2020-12-31 | 전년 동일 기간 | KRW | N/A | 0 | N/A | N/A | missing_previous | 전기 원본 기간 미확보 | False | N/A | N/A | N/A | thstrm_amount |  | [&quot;DEMO-2021-FY&quot;] | N/A | N/A |
| 자산총계 | demo:assets | BS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 55000000000 | 62000000000 | 7000000000 | 12.72727272727272727272727272727273 | calculated |  | False | 55000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 차입금(리스 제외) | demo:borrowings | BS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 14000000000 | 16000000000 | 2000000000 | 14.28571428571428571428571428571429 | calculated |  | False | 14000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 현금및현금성자산 | demo:cash | BS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 6000000000 | 7000000000 | 1000000000 | 16.66666666666666666666666666666667 | calculated |  | False | 6000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 유동자산 | demo:current_assets | BS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 19000000000 | 22500000000 | 3500000000 | 18.42105263157894736842105263157895 | calculated |  | False | 19000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 유동부채 | demo:current_liabilities | BS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 16200000000 | 17600000000 | 1400000000 | 8.641975308641975308641975308641975 | calculated |  | False | 16200000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 자본총계 | demo:equity | BS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 30000000000 | 35000000000 | 5000000000 | 16.66666666666666666666666666666667 | calculated |  | False | 30000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 재고자산 | demo:inventory | BS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 6000000000 | 7000000000 | 1000000000 | 16.66666666666666666666666666666667 | calculated |  | False | 6000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 리스부채 | demo:lease_liabilities | BS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 2000000000 | 2000000000 | 0 | 0 | calculated |  | False | 2000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 부채총계 | demo:liabilities | BS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 25000000000 | 27000000000 | 2000000000 | 8.00 | calculated |  | False | 25000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 지배주주 지분 | demo:parent_equity | BS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 30000000000 | 35000000000 | 5000000000 | 16.66666666666666666666666666666667 | calculated |  | False | 30000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 순매출채권 | demo:receivables | BS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 7000000000 | 8500000000 | 1500000000 | 21.42857142857142857142857142857143 | calculated |  | False | 7000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 무형자산 현금취득 | demo:capex_intangible | CF |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 500000000 | 500000000 | 0 | 0 | calculated |  | False | 500000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 유형자산 현금취득 | demo:capex_ppe | CF |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 2500000000 | 3000000000 | 500000000 | 20.0 | calculated |  | False | 2500000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 기초 현금 | demo:cash_beginning | CF |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 5000000000 | 6000000000 | 1000000000 | 20.0 | calculated |  | False | 5000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 재무활동현금흐름 | demo:cff | CF |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 0 | -500000000 | -500000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | 0 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 투자활동현금흐름 | demo:cfi | CF |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | -3000000000 | -3500000000 | -500000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | -3000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 영업활동현금흐름 | demo:cfo | CF |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 4000000000 | 5000000000 | 1000000000 | 25.00 | calculated |  | False | 4000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 현금배당 지급 | demo:dividends_paid | CF |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 2000000000 | 2000000000 | 0 | 0 | calculated |  | False | 2000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 환율변동효과 | demo:fx_effect | CF |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | 0 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 기타 현금조정 | demo:other_cash_effects | CF |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | 0 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 매출원가 | demo:cost_of_sales | IS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 45000000000 | 52500000000 | 7500000000 | 16.66666666666666666666666666666667 | calculated |  | False | 45000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 매출총이익 | demo:gross_profit | IS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 15000000000 | 17500000000 | 2500000000 | 16.66666666666666666666666666666667 | calculated |  | False | 15000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 총이자비용 | demo:interest_expense | IS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 1000000000 | 1000000000 | 0 | 0 | calculated |  | False | 1000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 전체 당기순이익 | demo:net_income | IS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 3000000000 | 3600000000 | 600000000 | 20.0 | calculated |  | False | 3000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 영업이익 | demo:operating_profit | IS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 4200000000 | 4900000000 | 700000000 | 16.66666666666666666666666666666667 | calculated |  | False | 4200000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 지배주주 순이익 | demo:parent_net_income | IS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 3000000000 | 3600000000 | 600000000 | 20.0 | calculated |  | False | 3000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 매출액 | demo:revenue | IS |  | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 60000000000 | 70000000000 | 10000000000 | 16.66666666666666666666666666666667 | calculated |  | False | 60000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 기초 자본 | demo:equity_beginning | SCE | 자본 [member] | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 27000000000 | 30000000000 | 3000000000 | 11.11111111111111111111111111111111 | calculated |  | False | 27000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 자본차감 배당 | demo:equity_dividends | SCE | 자본 [member] | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 2000000000 | 2000000000 | 0 | 0 | calculated |  | False | 2000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 기타 자본변동 | demo:equity_other_changes | SCE | 자본 [member] | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 2000000000 | 3400000000 | 1400000000 | 70.0 | calculated |  | False | 2000000000 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 기타포괄손익 | demo:oci | SCE | 자본 [member] | CFS | 2022 | 2022-01-01 | 2022-12-31 | 2021-01-01~2021-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | 0 | DEMO-2021-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2022-FY&quot;] | N/A | N/A |
| 자산총계 | demo:assets | BS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 62000000000 | 70000000000 | 8000000000 | 12.90322580645161290322580645161290 | calculated |  | False | 62000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 차입금(리스 제외) | demo:borrowings | BS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 16000000000 | 18000000000 | 2000000000 | 12.500 | calculated |  | False | 16000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 현금및현금성자산 | demo:cash | BS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 7000000000 | 8000000000 | 1000000000 | 14.28571428571428571428571428571429 | calculated |  | False | 7000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 유동자산 | demo:current_assets | BS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 22500000000 | 26000000000 | 3500000000 | 15.55555555555555555555555555555556 | calculated |  | False | 22500000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 유동부채 | demo:current_liabilities | BS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 17600000000 | 19500000000 | 1900000000 | 10.79545454545454545454545454545455 | calculated |  | False | 17600000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 자본총계 | demo:equity | BS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 35000000000 | 40000000000 | 5000000000 | 14.28571428571428571428571428571429 | calculated |  | False | 35000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 재고자산 | demo:inventory | BS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 7000000000 | 8000000000 | 1000000000 | 14.28571428571428571428571428571429 | calculated |  | False | 7000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 리스부채 | demo:lease_liabilities | BS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 2000000000 | 2000000000 | 0 | 0 | calculated |  | False | 2000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 부채총계 | demo:liabilities | BS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 27000000000 | 30000000000 | 3000000000 | 11.11111111111111111111111111111111 | calculated |  | False | 27000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 지배주주 지분 | demo:parent_equity | BS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 35000000000 | 40000000000 | 5000000000 | 14.28571428571428571428571428571429 | calculated |  | False | 35000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 순매출채권 | demo:receivables | BS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 8500000000 | 10000000000 | 1500000000 | 17.64705882352941176470588235294118 | calculated |  | False | 8500000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 무형자산 현금취득 | demo:capex_intangible | CF |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 500000000 | 500000000 | 0 | 0 | calculated |  | False | 500000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 유형자산 현금취득 | demo:capex_ppe | CF |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 3000000000 | 3500000000 | 500000000 | 16.66666666666666666666666666666667 | calculated |  | False | 3000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 기초 현금 | demo:cash_beginning | CF |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 6000000000 | 7000000000 | 1000000000 | 16.66666666666666666666666666666667 | calculated |  | False | 6000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 재무활동현금흐름 | demo:cff | CF |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | -500000000 | -1000000000 | -500000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | -500000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 투자활동현금흐름 | demo:cfi | CF |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | -3500000000 | -4000000000 | -500000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | -3500000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 영업활동현금흐름 | demo:cfo | CF |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 5000000000 | 6000000000 | 1000000000 | 20.0 | calculated |  | False | 5000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 현금배당 지급 | demo:dividends_paid | CF |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 2000000000 | 2000000000 | 0 | 0 | calculated |  | False | 2000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 환율변동효과 | demo:fx_effect | CF |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | 0 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 기타 현금조정 | demo:other_cash_effects | CF |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | 0 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 매출원가 | demo:cost_of_sales | IS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 52500000000 | 60000000000 | 7500000000 | 14.28571428571428571428571428571429 | calculated |  | False | 52500000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 매출총이익 | demo:gross_profit | IS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 17500000000 | 20000000000 | 2500000000 | 14.28571428571428571428571428571429 | calculated |  | False | 17500000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 총이자비용 | demo:interest_expense | IS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 1000000000 | 1000000000 | 0 | 0 | calculated |  | False | 1000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 전체 당기순이익 | demo:net_income | IS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 3600000000 | 4800000000 | 1200000000 | 33.33333333333333333333333333333333 | calculated |  | False | 3600000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 영업이익 | demo:operating_profit | IS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 4900000000 | 6400000000 | 1500000000 | 30.61224489795918367346938775510204 | calculated |  | False | 4900000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 지배주주 순이익 | demo:parent_net_income | IS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 3600000000 | 4800000000 | 1200000000 | 33.33333333333333333333333333333333 | calculated |  | False | 3600000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 매출액 | demo:revenue | IS |  | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 70000000000 | 80000000000 | 10000000000 | 14.28571428571428571428571428571429 | calculated |  | False | 70000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 기초 자본 | demo:equity_beginning | SCE | 자본 [member] | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 30000000000 | 35000000000 | 5000000000 | 16.66666666666666666666666666666667 | calculated |  | False | 30000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 자본차감 배당 | demo:equity_dividends | SCE | 자본 [member] | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 2000000000 | 2000000000 | 0 | 0 | calculated |  | False | 2000000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 기타 자본변동 | demo:equity_other_changes | SCE | 자본 [member] | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 3400000000 | 2200000000 | -1200000000 | -35.29411764705882352941176470588235 | calculated |  | False | 3400000000 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 기타포괄손익 | demo:oci | SCE | 자본 [member] | CFS | 2023 | 2023-01-01 | 2023-12-31 | 2022-01-01~2022-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | 0 | DEMO-2022-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2023-FY&quot;] | N/A | N/A |
| 자산총계 | demo:assets | BS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 70000000000 | 85000000000 | 15000000000 | 21.42857142857142857142857142857143 | calculated |  | False | 70000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 차입금(리스 제외) | demo:borrowings | BS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 18000000000 | 23000000000 | 5000000000 | 27.77777777777777777777777777777778 | calculated |  | False | 18000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 현금및현금성자산 | demo:cash | BS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 8000000000 | 9000000000 | 1000000000 | 12.500 | calculated |  | False | 8000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 유동자산 | demo:current_assets | BS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 26000000000 | 35000000000 | 9000000000 | 34.61538461538461538461538461538462 | calculated |  | False | 26000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 유동부채 | demo:current_liabilities | BS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 19500000000 | 26000000000 | 6500000000 | 33.33333333333333333333333333333333 | calculated |  | False | 19500000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 자본총계 | demo:equity | BS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 40000000000 | 45000000000 | 5000000000 | 12.500 | calculated |  | False | 40000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 재고자산 | demo:inventory | BS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 8000000000 | 12000000000 | 4000000000 | 50.0 | calculated |  | False | 8000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 리스부채 | demo:lease_liabilities | BS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 2000000000 | 2000000000 | 0 | 0 | calculated |  | False | 2000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 부채총계 | demo:liabilities | BS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 30000000000 | 40000000000 | 10000000000 | 33.33333333333333333333333333333333 | calculated |  | False | 30000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 지배주주 지분 | demo:parent_equity | BS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 40000000000 | 45000000000 | 5000000000 | 12.500 | calculated |  | False | 40000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 순매출채권 | demo:receivables | BS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 10000000000 | 14000000000 | 4000000000 | 40.0 | calculated |  | False | 10000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 무형자산 현금취득 | demo:capex_intangible | CF |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 500000000 | 500000000 | 0 | 0 | calculated |  | False | 500000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 유형자산 현금취득 | demo:capex_ppe | CF |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 3500000000 | 4500000000 | 1000000000 | 28.57142857142857142857142857142857 | calculated |  | False | 3500000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 기초 현금 | demo:cash_beginning | CF |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 7000000000 | 8000000000 | 1000000000 | 14.28571428571428571428571428571429 | calculated |  | False | 7000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 재무활동현금흐름 | demo:cff | CF |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | -1000000000 | -1000000000 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | -1000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 투자활동현금흐름 | demo:cfi | CF |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | -4000000000 | -5000000000 | -1000000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | -4000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 영업활동현금흐름 | demo:cfo | CF |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 6000000000 | 7000000000 | 1000000000 | 16.66666666666666666666666666666667 | calculated |  | False | 6000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 현금배당 지급 | demo:dividends_paid | CF |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 2000000000 | 2000000000 | 0 | 0 | calculated |  | False | 2000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 환율변동효과 | demo:fx_effect | CF |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | 0 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 기타 현금조정 | demo:other_cash_effects | CF |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | 0 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 매출원가 | demo:cost_of_sales | IS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 60000000000 | 75000000000 | 15000000000 | 25.00 | calculated |  | False | 60000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 매출총이익 | demo:gross_profit | IS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 20000000000 | 25000000000 | 5000000000 | 25.00 | calculated |  | False | 20000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 총이자비용 | demo:interest_expense | IS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 1000000000 | 1000000000 | 0 | 0 | calculated |  | False | 1000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 전체 당기순이익 | demo:net_income | IS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 4800000000 | 8000000000 | 3200000000 | 66.66666666666666666666666666666667 | calculated |  | False | 4800000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 영업이익 | demo:operating_profit | IS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 6400000000 | 10000000000 | 3600000000 | 56.2500 | calculated |  | False | 6400000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 지배주주 순이익 | demo:parent_net_income | IS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 4800000000 | 8000000000 | 3200000000 | 66.66666666666666666666666666666667 | calculated |  | False | 4800000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 매출액 | demo:revenue | IS |  | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 80000000000 | 100000000000 | 20000000000 | 25.00 | calculated |  | False | 80000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 기초 자본 | demo:equity_beginning | SCE | 자본 [member] | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 35000000000 | 40000000000 | 5000000000 | 14.28571428571428571428571428571429 | calculated |  | False | 35000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 자본차감 배당 | demo:equity_dividends | SCE | 자본 [member] | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 2000000000 | 2000000000 | 0 | 0 | calculated |  | False | 2000000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 기타 자본변동 | demo:equity_other_changes | SCE | 자본 [member] | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 2200000000 | -1000000000 | -3200000000 | -145.4545454545454545454545454545455 | calculated |  | False | 2200000000 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 기타포괄손익 | demo:oci | SCE | 자본 [member] | CFS | 2024 | 2024-01-01 | 2024-12-31 | 2023-01-01~2023-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | 0 | DEMO-2023-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2024-FY&quot;] | N/A | N/A |
| 자산총계 | demo:assets | BS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 84000000000 | 100000000000 | 16000000000 | 19.04761904761904761904761904761905 | calculated | 후속 공시 비교열과 과거 공시 당기값이 다름: 재작성/버전 확인 필요 | True | 85000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 차입금(리스 제외) | demo:borrowings | BS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 23000000000 | 32000000000 | 9000000000 | 39.13043478260869565217391304347826 | calculated |  | False | 23000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 현금및현금성자산 | demo:cash | BS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 9000000000 | 10000000000 | 1000000000 | 11.11111111111111111111111111111111 | calculated |  | False | 9000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 유동자산 | demo:current_assets | BS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 35000000000 | 49000000000 | 14000000000 | 40.0 | calculated |  | False | 35000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 유동부채 | demo:current_liabilities | BS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 26000000000 | 33800000000 | 7800000000 | 30.0 | calculated |  | False | 26000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 자본총계 | demo:equity | BS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 44000000000 | 48000000000 | 4000000000 | 9.090909090909090909090909090909091 | calculated | 후속 공시 비교열과 과거 공시 당기값이 다름: 재작성/버전 확인 필요 | True | 45000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 재고자산 | demo:inventory | BS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 12000000000 | 17000000000 | 5000000000 | 41.66666666666666666666666666666667 | calculated |  | False | 12000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 리스부채 | demo:lease_liabilities | BS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 2000000000 | 2000000000 | 0 | 0 | calculated |  | False | 2000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 부채총계 | demo:liabilities | BS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 40000000000 | 52000000000 | 12000000000 | 30.0 | calculated |  | False | 40000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 지배주주 지분 | demo:parent_equity | BS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 44000000000 | 48000000000 | 4000000000 | 9.090909090909090909090909090909091 | calculated | 후속 공시 비교열과 과거 공시 당기값이 다름: 재작성/버전 확인 필요 | True | 45000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 순매출채권 | demo:receivables | BS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 14000000000 | 22000000000 | 8000000000 | 57.14285714285714285714285714285714 | calculated |  | False | 14000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 무형자산 현금취득 | demo:capex_intangible | CF |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 500000000 | 500000000 | 0 | 0 | calculated |  | False | 500000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 유형자산 현금취득 | demo:capex_ppe | CF |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 4500000000 | 7500000000 | 3000000000 | 66.66666666666666666666666666666667 | calculated |  | False | 4500000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 기초 현금 | demo:cash_beginning | CF |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 8000000000 | 9000000000 | 1000000000 | 12.500 | calculated |  | False | 8000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 재무활동현금흐름 | demo:cff | CF |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | -1000000000 | 4500000000 | 5500000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | -1000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 투자활동현금흐름 | demo:cfi | CF |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | -5000000000 | -8000000000 | -3000000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | -5000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 영업활동현금흐름 | demo:cfo | CF |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 7000000000 | 4500000000 | -2500000000 | -35.71428571428571428571428571428571 | calculated |  | False | 7000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 현금배당 지급 | demo:dividends_paid | CF |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 2000000000 | 2000000000 | 0 | 0 | calculated |  | False | 2000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 환율변동효과 | demo:fx_effect | CF |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | 0 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 기타 현금조정 | demo:other_cash_effects | CF |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | 0 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 매출원가 | demo:cost_of_sales | IS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 75000000000 | 93000000000 | 18000000000 | 24.00 | calculated |  | False | 75000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 매출총이익 | demo:gross_profit | IS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 25000000000 | 27000000000 | 2000000000 | 8.00 | calculated |  | False | 25000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 총이자비용 | demo:interest_expense | IS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 1000000000 | 1800000000 | 800000000 | 80.0 | calculated |  | False | 1000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 전체 당기순이익 | demo:net_income | IS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 8000000000 | 9000000000 | 1000000000 | 12.500 | calculated |  | False | 8000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 영업이익 | demo:operating_profit | IS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 10000000000 | 10800000000 | 800000000 | 8.00 | calculated |  | False | 10000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 지배주주 순이익 | demo:parent_net_income | IS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 8000000000 | 9000000000 | 1000000000 | 12.500 | calculated |  | False | 8000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 매출액 | demo:revenue | IS |  | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 100000000000 | 120000000000 | 20000000000 | 20.0 | calculated |  | False | 100000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 기초 자본 | demo:equity_beginning | SCE | 자본 [member] | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 40000000000 | 44000000000 | 4000000000 | 10.0 | calculated |  | False | 40000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 자본차감 배당 | demo:equity_dividends | SCE | 자본 [member] | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 2000000000 | 2000000000 | 0 | 0 | calculated |  | False | 2000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 기타 자본변동 | demo:equity_other_changes | SCE | 자본 [member] | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | -1000000000 | -3000000000 | -2000000000 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | -1000000000 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 기타포괄손익 | demo:oci | SCE | 자본 [member] | CFS | 2025 | 2025-01-01 | 2025-12-31 | 2024-01-01~2024-12-31 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 0 | 0 | 0 | N/A | calculated | 비교기≤0: 증감률 대신 금액 차이 표시 | False | 0 | DEMO-2024-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2025-FY&quot;] | N/A | N/A |
| 자산총계 | demo:assets | BS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 100000000000 | 108000000000 | 8000000000 | 8.00 | calculated |  | False | 100000000000 | DEMO-2025-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 차입금(리스 제외) | demo:borrowings | BS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 32000000000 | 35000000000 | 3000000000 | 9.37500 | calculated |  | False | 32000000000 | DEMO-2025-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 현금및현금성자산 | demo:cash | BS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 10000000000 | 11000000000 | 1000000000 | 10.0 | calculated |  | False | 10000000000 | DEMO-2025-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 유동자산 | demo:current_assets | BS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 49000000000 | 55000000000 | 6000000000 | 12.24489795918367346938775510204082 | calculated |  | False | 49000000000 | DEMO-2025-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 유동부채 | demo:current_liabilities | BS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 33800000000 | 37000000000 | 3200000000 | 9.467455621301775147928994082840237 | calculated |  | False | 33800000000 | DEMO-2025-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 자본총계 | demo:equity | BS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 48000000000 | 51500000000 | 3500000000 | 7.291666666666666666666666666666667 | calculated |  | False | 48000000000 | DEMO-2025-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 재고자산 | demo:inventory | BS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 17000000000 | 19000000000 | 2000000000 | 11.76470588235294117647058823529412 | calculated |  | False | 17000000000 | DEMO-2025-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 리스부채 | demo:lease_liabilities | BS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 2000000000 | 2000000000 | 0 | 0 | calculated |  | False | 2000000000 | DEMO-2025-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 부채총계 | demo:liabilities | BS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 52000000000 | 56500000000 | 4500000000 | 8.653846153846153846153846153846154 | calculated |  | False | 52000000000 | DEMO-2025-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 지배주주 지분 | demo:parent_equity | BS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 48000000000 | 51500000000 | 3500000000 | 7.291666666666666666666666666666667 | calculated |  | False | 48000000000 | DEMO-2025-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 순매출채권 | demo:receivables | BS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-12-31 | 전기말 잔액 · 당기 공시 비교열 우선 | KRW | 22000000000 | 23500000000 | 1500000000 | 6.818181818181818181818181818181818 | calculated |  | False | 22000000000 | DEMO-2025-FY | N/A | thstrm_amount | frmtrm_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 무형자산 현금취득 | demo:capex_intangible | CF |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | N/A |  | N/A | N/A | N/A | N/A | N/A | not_comparable | 중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인 | False | N/A | N/A | N/A |  |  | [] | N/A | N/A |
| 유형자산 현금취득 | demo:capex_ppe | CF |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | N/A |  | N/A | N/A | N/A | N/A | N/A | not_comparable | 중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인 | False | N/A | N/A | N/A |  |  | [] | N/A | N/A |
| 기초 현금 | demo:cash_beginning | CF |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | N/A |  | N/A | N/A | N/A | N/A | N/A | not_comparable | 중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인 | False | N/A | N/A | N/A |  |  | [] | N/A | N/A |
| 재무활동현금흐름 | demo:cff | CF |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | N/A |  | N/A | N/A | N/A | N/A | N/A | not_comparable | 중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인 | False | N/A | N/A | N/A |  |  | [] | N/A | N/A |
| 투자활동현금흐름 | demo:cfi | CF |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | N/A |  | N/A | N/A | N/A | N/A | N/A | not_comparable | 중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인 | False | N/A | N/A | N/A |  |  | [] | N/A | N/A |
| 영업활동현금흐름 | demo:cfo | CF |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | N/A |  | N/A | N/A | N/A | N/A | N/A | not_comparable | 중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인 | False | N/A | N/A | N/A |  |  | [] | N/A | N/A |
| 현금배당 지급 | demo:dividends_paid | CF |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | N/A |  | N/A | N/A | N/A | N/A | N/A | not_comparable | 중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인 | False | N/A | N/A | N/A |  |  | [] | N/A | N/A |
| 환율변동효과 | demo:fx_effect | CF |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | N/A |  | N/A | N/A | N/A | N/A | N/A | not_comparable | 중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인 | False | N/A | N/A | N/A |  |  | [] | N/A | N/A |
| 기타 현금조정 | demo:other_cash_effects | CF |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | N/A |  | N/A | N/A | N/A | N/A | N/A | not_comparable | 중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인 | False | N/A | N/A | N/A |  |  | [] | N/A | N/A |
| 매출원가 | demo:cost_of_sales | IS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-01-01~2025-06-30 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 44000000000 | 50000000000 | 6000000000 | 13.63636363636363636363636363636364 | calculated |  | False | N/A | N/A | N/A | thstrm_add_amount | frmtrm_add_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 매출총이익 | demo:gross_profit | IS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-01-01~2025-06-30 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 14000000000 | 14000000000 | 0 | 0 | calculated |  | False | N/A | N/A | N/A | thstrm_add_amount | frmtrm_add_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 총이자비용 | demo:interest_expense | IS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-01-01~2025-06-30 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 900000000.0 | 900000000.0 | 0.0 | 0 | calculated |  | False | N/A | N/A | N/A | thstrm_add_amount | frmtrm_add_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 전체 당기순이익 | demo:net_income | IS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-01-01~2025-06-30 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 4300000000 | 4000000000 | -300000000 | -6.976744186046511627906976744186047 | calculated |  | False | N/A | N/A | N/A | thstrm_add_amount | frmtrm_add_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 영업이익 | demo:operating_profit | IS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-01-01~2025-06-30 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 5500000000 | 5200000000 | -300000000 | -5.454545454545454545454545454545455 | calculated |  | False | N/A | N/A | N/A | thstrm_add_amount | frmtrm_add_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 지배주주 순이익 | demo:parent_net_income | IS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-01-01~2025-06-30 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 4300000000 | 4000000000 | -300000000 | -6.976744186046511627906976744186047 | calculated |  | False | N/A | N/A | N/A | thstrm_add_amount | frmtrm_add_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 매출액 | demo:revenue | IS |  | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | 2025-01-01~2025-06-30 | 전년 동일 기간 · 당기 공시 비교열 우선 | KRW | 58000000000 | 64000000000 | 6000000000 | 10.34482758620689655172413793103448 | calculated |  | False | N/A | N/A | N/A | thstrm_add_amount | frmtrm_add_amount | [&quot;DEMO-2026-YTD&quot;] | N/A | N/A |
| 기초 자본 | demo:equity_beginning | SCE | 자본 [member] | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | N/A |  | N/A | N/A | N/A | N/A | N/A | not_comparable | 중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인 | False | N/A | N/A | N/A |  |  | [] | N/A | N/A |
| 자본차감 배당 | demo:equity_dividends | SCE | 자본 [member] | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | N/A |  | N/A | N/A | N/A | N/A | N/A | not_comparable | 중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인 | False | N/A | N/A | N/A |  |  | [] | N/A | N/A |
| 기타 자본변동 | demo:equity_other_changes | SCE | 자본 [member] | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | N/A |  | N/A | N/A | N/A | N/A | N/A | not_comparable | 중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인 | False | N/A | N/A | N/A |  |  | [] | N/A | N/A |
| 기타포괄손익 | demo:oci | SCE | 자본 [member] | CFS | 2026 H1 | 2026-01-01 | 2026-06-30 | N/A |  | N/A | N/A | N/A | N/A | N/A | not_comparable | 중간 CF/SCE 원천 행의 누적·단독 기간 문맥 미확인 | False | N/A | N/A | N/A |  |  | [] | N/A | N/A |

## 회계 연결 대조

| 기간 | 대조항목 | 상태 | 좌변 | 우변 | 차이 | 허용오차 | 설명 | 입력 계정 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021 | 자산 = 부채 + 자본 | pass | 55000000000 | 55000000000 | 0 | 1.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;assets&quot;, &quot;liabilities&quot;, &quot;equity&quot;] |
| 2021 | 매출 − 원가 = 총이익 | pass | 15000000000 | 15000000000 | 0 | 1.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;revenue&quot;, &quot;cost_of_sales&quot;, &quot;gross_profit&quot;] |
| 2021 | 기초 현금 + 현금흐름 = 기말 현금 | pass | 6000000000 | 6000000000 | 0 | 3.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;cash_beginning&quot;, &quot;cfo&quot;, &quot;cfi&quot;, &quot;cff&quot;, &quot;fx_effect&quot;, &quot;other_cash_effects&quot;, &quot;cash&quot;] |
| 2021 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | 30000000000 | 30000000000 | 0 | 3.0 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;equity_beginning&quot;, &quot;net_income&quot;, &quot;oci&quot;, &quot;equity_dividends&quot;, &quot;equity_other_changes&quot;, &quot;equity&quot;] |
| 2022 | 자산 = 부채 + 자본 | pass | 62000000000 | 62000000000 | 0 | 1.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;assets&quot;, &quot;liabilities&quot;, &quot;equity&quot;] |
| 2022 | 매출 − 원가 = 총이익 | pass | 17500000000 | 17500000000 | 0 | 1.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;revenue&quot;, &quot;cost_of_sales&quot;, &quot;gross_profit&quot;] |
| 2022 | 기초 현금 + 현금흐름 = 기말 현금 | pass | 7000000000 | 7000000000 | 0 | 3.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;cash_beginning&quot;, &quot;cfo&quot;, &quot;cfi&quot;, &quot;cff&quot;, &quot;fx_effect&quot;, &quot;other_cash_effects&quot;, &quot;cash&quot;] |
| 2022 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | 35000000000 | 35000000000 | 0 | 3.0 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;equity_beginning&quot;, &quot;net_income&quot;, &quot;oci&quot;, &quot;equity_dividends&quot;, &quot;equity_other_changes&quot;, &quot;equity&quot;] |
| 2023 | 자산 = 부채 + 자본 | pass | 70000000000 | 70000000000 | 0 | 1.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;assets&quot;, &quot;liabilities&quot;, &quot;equity&quot;] |
| 2023 | 매출 − 원가 = 총이익 | pass | 20000000000 | 20000000000 | 0 | 1.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;revenue&quot;, &quot;cost_of_sales&quot;, &quot;gross_profit&quot;] |
| 2023 | 기초 현금 + 현금흐름 = 기말 현금 | pass | 8000000000 | 8000000000 | 0 | 3.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;cash_beginning&quot;, &quot;cfo&quot;, &quot;cfi&quot;, &quot;cff&quot;, &quot;fx_effect&quot;, &quot;other_cash_effects&quot;, &quot;cash&quot;] |
| 2023 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | 40000000000 | 40000000000 | 0 | 3.0 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;equity_beginning&quot;, &quot;net_income&quot;, &quot;oci&quot;, &quot;equity_dividends&quot;, &quot;equity_other_changes&quot;, &quot;equity&quot;] |
| 2024 | 자산 = 부채 + 자본 | pass | 85000000000 | 85000000000 | 0 | 1.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;assets&quot;, &quot;liabilities&quot;, &quot;equity&quot;] |
| 2024 | 매출 − 원가 = 총이익 | pass | 25000000000 | 25000000000 | 0 | 1.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;revenue&quot;, &quot;cost_of_sales&quot;, &quot;gross_profit&quot;] |
| 2024 | 기초 현금 + 현금흐름 = 기말 현금 | pass | 9000000000 | 9000000000 | 0 | 3.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;cash_beginning&quot;, &quot;cfo&quot;, &quot;cfi&quot;, &quot;cff&quot;, &quot;fx_effect&quot;, &quot;other_cash_effects&quot;, &quot;cash&quot;] |
| 2024 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | 45000000000 | 45000000000 | 0 | 3.0 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;equity_beginning&quot;, &quot;net_income&quot;, &quot;oci&quot;, &quot;equity_dividends&quot;, &quot;equity_other_changes&quot;, &quot;equity&quot;] |
| 2025 | 자산 = 부채 + 자본 | pass | 100000000000 | 100000000000 | 0 | 1.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;assets&quot;, &quot;liabilities&quot;, &quot;equity&quot;] |
| 2025 | 매출 − 원가 = 총이익 | pass | 27000000000 | 27000000000 | 0 | 1.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;revenue&quot;, &quot;cost_of_sales&quot;, &quot;gross_profit&quot;] |
| 2025 | 기초 현금 + 현금흐름 = 기말 현금 | pass | 10000000000 | 10000000000 | 0 | 3.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;cash_beginning&quot;, &quot;cfo&quot;, &quot;cfi&quot;, &quot;cff&quot;, &quot;fx_effect&quot;, &quot;other_cash_effects&quot;, &quot;cash&quot;] |
| 2025 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | 48000000000 | 48000000000 | 0 | 3.0 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;equity_beginning&quot;, &quot;net_income&quot;, &quot;oci&quot;, &quot;equity_dividends&quot;, &quot;equity_other_changes&quot;, &quot;equity&quot;] |
| 2026 H1 | 자산 = 부채 + 자본 | pass | 108000000000 | 108000000000 | 0 | 1.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;assets&quot;, &quot;liabilities&quot;, &quot;equity&quot;] |
| 2026 H1 | 매출 − 원가 = 총이익 | pass | 14000000000 | 14000000000 | 0 | 1.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;revenue&quot;, &quot;cost_of_sales&quot;, &quot;gross_profit&quot;] |
| 2026 H1 | 기초 현금 + 현금흐름 = 기말 현금 | pass | 11000000000 | 11000000000 | 0 | 3.5 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;cash_beginning&quot;, &quot;cfo&quot;, &quot;cfi&quot;, &quot;cff&quot;, &quot;fx_effect&quot;, &quot;other_cash_effects&quot;, &quot;cash&quot;] |
| 2026 H1 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | 51500000000 | 51500000000 | 0 | 3.0 | 원천 표시 단위 반올림 허용오차 적용 | [&quot;equity_beginning&quot;, &quot;net_income&quot;, &quot;oci&quot;, &quot;equity_dividends&quot;, &quot;equity_other_changes&quot;, &quot;equity&quot;] |

## 대조 입력 상세

| 기간 | 대조항목 | 대조 상태 | 입력 계정 | 공시 계정명 | 단위 환산 금액 | 통화 | 시작일 | 종료일 | 연결범위 | 공시번호 | 원문 | 자료 사유 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021 | 자산 = 부채 + 자본 | pass | assets | 자산총계 | 55000000000 | KRW | 2021-12-31 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 자산 = 부채 + 자본 | pass | liabilities | 부채총계 | 25000000000 | KRW | 2021-12-31 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 자산 = 부채 + 자본 | pass | equity | 자본총계 | 30000000000 | KRW | 2021-12-31 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 매출 − 원가 = 총이익 | pass | revenue | 매출액 | 60000000000 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 매출 − 원가 = 총이익 | pass | cost_of_sales | 매출원가 | 45000000000 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 매출 − 원가 = 총이익 | pass | gross_profit | 매출총이익 | 15000000000 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cash_beginning | 기초 현금 | 5000000000 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cfo | 영업활동현금흐름 | 4000000000 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cfi | 투자활동현금흐름 | -3000000000 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cff | 재무활동현금흐름 | 0 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 기초 현금 + 현금흐름 = 기말 현금 | pass | fx_effect | 환율변동효과 | 0 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 기초 현금 + 현금흐름 = 기말 현금 | pass | other_cash_effects | 기타 현금조정 | 0 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cash | 현금및현금성자산 | 6000000000 | KRW | 2021-12-31 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_beginning | 기초 자본 | 27000000000 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | net_income | 전체 당기순이익 | 3000000000 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | oci | 기타포괄손익 | 0 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_dividends | 자본차감 배당 | 2000000000 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_other_changes | 기타 자본변동 | 2000000000 | KRW | 2021-01-01 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2021 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity | 자본총계 | 30000000000 | KRW | 2021-12-31 | 2021-12-31 | CFS | DEMO-2021-FY | N/A |  |
| 2022 | 자산 = 부채 + 자본 | pass | assets | 자산총계 | 62000000000 | KRW | 2022-12-31 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 자산 = 부채 + 자본 | pass | liabilities | 부채총계 | 27000000000 | KRW | 2022-12-31 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 자산 = 부채 + 자본 | pass | equity | 자본총계 | 35000000000 | KRW | 2022-12-31 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 매출 − 원가 = 총이익 | pass | revenue | 매출액 | 70000000000 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 매출 − 원가 = 총이익 | pass | cost_of_sales | 매출원가 | 52500000000 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 매출 − 원가 = 총이익 | pass | gross_profit | 매출총이익 | 17500000000 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cash_beginning | 기초 현금 | 6000000000 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cfo | 영업활동현금흐름 | 5000000000 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cfi | 투자활동현금흐름 | -3500000000 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cff | 재무활동현금흐름 | -500000000 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 기초 현금 + 현금흐름 = 기말 현금 | pass | fx_effect | 환율변동효과 | 0 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 기초 현금 + 현금흐름 = 기말 현금 | pass | other_cash_effects | 기타 현금조정 | 0 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cash | 현금및현금성자산 | 7000000000 | KRW | 2022-12-31 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_beginning | 기초 자본 | 30000000000 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | net_income | 전체 당기순이익 | 3600000000 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | oci | 기타포괄손익 | 0 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_dividends | 자본차감 배당 | 2000000000 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_other_changes | 기타 자본변동 | 3400000000 | KRW | 2022-01-01 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2022 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity | 자본총계 | 35000000000 | KRW | 2022-12-31 | 2022-12-31 | CFS | DEMO-2022-FY | N/A |  |
| 2023 | 자산 = 부채 + 자본 | pass | assets | 자산총계 | 70000000000 | KRW | 2023-12-31 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 자산 = 부채 + 자본 | pass | liabilities | 부채총계 | 30000000000 | KRW | 2023-12-31 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 자산 = 부채 + 자본 | pass | equity | 자본총계 | 40000000000 | KRW | 2023-12-31 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 매출 − 원가 = 총이익 | pass | revenue | 매출액 | 80000000000 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 매출 − 원가 = 총이익 | pass | cost_of_sales | 매출원가 | 60000000000 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 매출 − 원가 = 총이익 | pass | gross_profit | 매출총이익 | 20000000000 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cash_beginning | 기초 현금 | 7000000000 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cfo | 영업활동현금흐름 | 6000000000 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cfi | 투자활동현금흐름 | -4000000000 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cff | 재무활동현금흐름 | -1000000000 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 기초 현금 + 현금흐름 = 기말 현금 | pass | fx_effect | 환율변동효과 | 0 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 기초 현금 + 현금흐름 = 기말 현금 | pass | other_cash_effects | 기타 현금조정 | 0 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cash | 현금및현금성자산 | 8000000000 | KRW | 2023-12-31 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_beginning | 기초 자본 | 35000000000 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | net_income | 전체 당기순이익 | 4800000000 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | oci | 기타포괄손익 | 0 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_dividends | 자본차감 배당 | 2000000000 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_other_changes | 기타 자본변동 | 2200000000 | KRW | 2023-01-01 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2023 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity | 자본총계 | 40000000000 | KRW | 2023-12-31 | 2023-12-31 | CFS | DEMO-2023-FY | N/A |  |
| 2024 | 자산 = 부채 + 자본 | pass | assets | 자산총계 | 85000000000 | KRW | 2024-12-31 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 자산 = 부채 + 자본 | pass | liabilities | 부채총계 | 40000000000 | KRW | 2024-12-31 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 자산 = 부채 + 자본 | pass | equity | 자본총계 | 45000000000 | KRW | 2024-12-31 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 매출 − 원가 = 총이익 | pass | revenue | 매출액 | 100000000000 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 매출 − 원가 = 총이익 | pass | cost_of_sales | 매출원가 | 75000000000 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 매출 − 원가 = 총이익 | pass | gross_profit | 매출총이익 | 25000000000 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cash_beginning | 기초 현금 | 8000000000 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cfo | 영업활동현금흐름 | 7000000000 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cfi | 투자활동현금흐름 | -5000000000 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cff | 재무활동현금흐름 | -1000000000 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 기초 현금 + 현금흐름 = 기말 현금 | pass | fx_effect | 환율변동효과 | 0 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 기초 현금 + 현금흐름 = 기말 현금 | pass | other_cash_effects | 기타 현금조정 | 0 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cash | 현금및현금성자산 | 9000000000 | KRW | 2024-12-31 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_beginning | 기초 자본 | 40000000000 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | net_income | 전체 당기순이익 | 8000000000 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | oci | 기타포괄손익 | 0 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_dividends | 자본차감 배당 | 2000000000 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_other_changes | 기타 자본변동 | -1000000000 | KRW | 2024-01-01 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2024 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity | 자본총계 | 45000000000 | KRW | 2024-12-31 | 2024-12-31 | CFS | DEMO-2024-FY | N/A |  |
| 2025 | 자산 = 부채 + 자본 | pass | assets | 자산총계 | 100000000000 | KRW | 2025-12-31 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 자산 = 부채 + 자본 | pass | liabilities | 부채총계 | 52000000000 | KRW | 2025-12-31 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 자산 = 부채 + 자본 | pass | equity | 자본총계 | 48000000000 | KRW | 2025-12-31 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 매출 − 원가 = 총이익 | pass | revenue | 매출액 | 120000000000 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 매출 − 원가 = 총이익 | pass | cost_of_sales | 매출원가 | 93000000000 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 매출 − 원가 = 총이익 | pass | gross_profit | 매출총이익 | 27000000000 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cash_beginning | 기초 현금 | 9000000000 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cfo | 영업활동현금흐름 | 4500000000 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cfi | 투자활동현금흐름 | -8000000000 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cff | 재무활동현금흐름 | 4500000000 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 기초 현금 + 현금흐름 = 기말 현금 | pass | fx_effect | 환율변동효과 | 0 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 기초 현금 + 현금흐름 = 기말 현금 | pass | other_cash_effects | 기타 현금조정 | 0 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cash | 현금및현금성자산 | 10000000000 | KRW | 2025-12-31 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_beginning | 기초 자본 | 44000000000 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | net_income | 전체 당기순이익 | 9000000000 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | oci | 기타포괄손익 | 0 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_dividends | 자본차감 배당 | 2000000000 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_other_changes | 기타 자본변동 | -3000000000 | KRW | 2025-01-01 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2025 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity | 자본총계 | 48000000000 | KRW | 2025-12-31 | 2025-12-31 | CFS | DEMO-2025-FY | N/A |  |
| 2026 H1 | 자산 = 부채 + 자본 | pass | assets | 자산총계 | 108000000000 | KRW | 2026-06-30 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 자산 = 부채 + 자본 | pass | liabilities | 부채총계 | 56500000000 | KRW | 2026-06-30 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 자산 = 부채 + 자본 | pass | equity | 자본총계 | 51500000000 | KRW | 2026-06-30 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 매출 − 원가 = 총이익 | pass | revenue | 매출액 | 64000000000 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 매출 − 원가 = 총이익 | pass | cost_of_sales | 매출원가 | 50000000000 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 매출 − 원가 = 총이익 | pass | gross_profit | 매출총이익 | 14000000000 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cash_beginning | 기초 현금 | 10000000000 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cfo | 영업활동현금흐름 | 3000000000 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cfi | 투자활동현금흐름 | -4500000000 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cff | 재무활동현금흐름 | 2500000000 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 기초 현금 + 현금흐름 = 기말 현금 | pass | fx_effect | 환율변동효과 | 0 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 기초 현금 + 현금흐름 = 기말 현금 | pass | other_cash_effects | 기타 현금조정 | 0 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 기초 현금 + 현금흐름 = 기말 현금 | pass | cash | 현금및현금성자산 | 11000000000 | KRW | 2026-06-30 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_beginning | 기초 자본 | 48000000000 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | net_income | 전체 당기순이익 | 4000000000 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | oci | 기타포괄손익 | 0 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_dividends | 자본차감 배당 | 1000000000 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity_other_changes | 기타 자본변동 | 500000000 | KRW | 2026-01-01 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 기초 자본 + 포괄손익 − 배당 + 기타 = 기말 자본 | pass | equity | 자본총계 | 51500000000 | KRW | 2026-06-30 | 2026-06-30 | CFS | DEMO-2026-YTD | N/A |  |

## 주석 점검

| 주제 | 상태 | 내용 | 위치 | 공시 | 원문 |
| --- | --- | --- | --- | --- | --- |
| 감사의견 | 가상 검증 자료 | 실제 주석 원문은 미확보입니다. 실제 기업 분석에서는 관련 공시 원문을 확인해야 합니다. | 가상 자료 — 원문 공시 없음 | DEMO-2025-FY | N/A |
| 차입금·유동성 | 가상 검증 자료 | 실제 주석 원문은 미확보입니다. 실제 기업 분석에서는 관련 공시 원문을 확인해야 합니다. | 가상 자료 — 원문 공시 없음 | DEMO-2025-FY | N/A |
| 채권·재고 | 가상 검증 자료 | 실제 주석 원문은 미확보입니다. 실제 기업 분석에서는 관련 공시 원문을 확인해야 합니다. | 가상 자료 — 원문 공시 없음 | DEMO-2025-FY | N/A |
| 손상·무형자산 | 가상 검증 자료 | 실제 주석 원문은 미확보입니다. 실제 기업 분석에서는 관련 공시 원문을 확인해야 합니다. | 가상 자료 — 원문 공시 없음 | DEMO-2025-FY | N/A |
| 특수관계자·우발사항 | 가상 검증 자료 | 실제 주석 원문은 미확보입니다. 실제 기업 분석에서는 관련 공시 원문을 확인해야 합니다. | 가상 자료 — 원문 공시 없음 | DEMO-2025-FY | N/A |

## 원천 계정

| 분석기간 | 구분 | 내부계정 | 공시계정 | 원천금액 | 단위배수 | 통화 | 재무제표 | 시작일 | 종료일 | 기간종류 | 연결범위 | 귀속 | 계정ID | 원천필드 | 공시번호 | 원문 | 결측사유 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021 | 당기 | revenue | 매출액 | 60000000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:revenue | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | cost_of_sales | 매출원가 | 45000000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:cost_of_sales | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | gross_profit | 매출총이익 | 15000000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:gross_profit | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | operating_profit | 영업이익 | 4200000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:operating_profit | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | net_income | 전체 당기순이익 | 3000000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:net_income | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | parent_net_income | 지배주주 순이익 | 3000000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | parent | demo:parent_net_income | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | assets | 자산총계 | 55000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:assets | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | liabilities | 부채총계 | 25000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:liabilities | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | equity | 자본총계 | 30000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:equity | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | parent_equity | 지배주주 지분 | 30000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | parent | demo:parent_equity | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | current_assets | 유동자산 | 19000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:current_assets | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | current_liabilities | 유동부채 | 16200000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:current_liabilities | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | cash | 현금및현금성자산 | 6000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:cash | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | receivables | 순매출채권 | 7000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:receivables | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | inventory | 재고자산 | 6000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:inventory | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | cfo | 영업활동현금흐름 | 4000000000 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:cfo | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | cfi | 투자활동현금흐름 | -3000000000 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:cfi | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | cff | 재무활동현금흐름 | 0 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:cff | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | fx_effect | 환율변동효과 | 0 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:fx_effect | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | other_cash_effects | 기타 현금조정 | 0 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:other_cash_effects | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | cash_beginning | 기초 현금 | 5000000000 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:cash_beginning | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | capex_ppe | 유형자산 현금취득 | 2500000000 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:capex_ppe | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | capex_intangible | 무형자산 현금취득 | 500000000 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:capex_intangible | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | borrowings | 차입금(리스 제외) | 14000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:borrowings | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | lease_liabilities | 리스부채 | 2000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:lease_liabilities | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | interest_expense | 총이자비용 | 1000000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:interest_expense | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | oci | 기타포괄손익 | 0 | 1 | KRW | SCE | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:oci | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | dividends_paid | 현금배당 지급 | 2000000000 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:dividends_paid | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | equity_dividends | 자본차감 배당 | 2000000000 | 1 | KRW | SCE | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:equity_dividends | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | equity_beginning | 기초 자본 | 27000000000 | 1 | KRW | SCE | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:equity_beginning | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2021 | 당기 | equity_other_changes | 기타 자본변동 | 2000000000 | 1 | KRW | SCE | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:equity_other_changes | thstrm_amount | DEMO-2021-FY | N/A |  |
| 2022 | 당기 | revenue | 매출액 | 70000000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:revenue | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | cost_of_sales | 매출원가 | 52500000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:cost_of_sales | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | gross_profit | 매출총이익 | 17500000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:gross_profit | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | operating_profit | 영업이익 | 4900000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:operating_profit | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | net_income | 전체 당기순이익 | 3600000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:net_income | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | parent_net_income | 지배주주 순이익 | 3600000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | parent | demo:parent_net_income | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | assets | 자산총계 | 62000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:assets | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | liabilities | 부채총계 | 27000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:liabilities | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | equity | 자본총계 | 35000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:equity | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | parent_equity | 지배주주 지분 | 35000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | parent | demo:parent_equity | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | current_assets | 유동자산 | 22500000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:current_assets | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | current_liabilities | 유동부채 | 17600000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:current_liabilities | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | cash | 현금및현금성자산 | 7000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:cash | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | receivables | 순매출채권 | 8500000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:receivables | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | inventory | 재고자산 | 7000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:inventory | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | cfo | 영업활동현금흐름 | 5000000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:cfo | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | cfi | 투자활동현금흐름 | -3500000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:cfi | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | cff | 재무활동현금흐름 | -500000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:cff | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | fx_effect | 환율변동효과 | 0 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:fx_effect | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | other_cash_effects | 기타 현금조정 | 0 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:other_cash_effects | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | cash_beginning | 기초 현금 | 6000000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:cash_beginning | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | capex_ppe | 유형자산 현금취득 | 3000000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:capex_ppe | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | capex_intangible | 무형자산 현금취득 | 500000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:capex_intangible | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | borrowings | 차입금(리스 제외) | 16000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:borrowings | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | lease_liabilities | 리스부채 | 2000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:lease_liabilities | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | interest_expense | 총이자비용 | 1000000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:interest_expense | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | oci | 기타포괄손익 | 0 | 1 | KRW | SCE | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:oci | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | dividends_paid | 현금배당 지급 | 2000000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:dividends_paid | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | equity_dividends | 자본차감 배당 | 2000000000 | 1 | KRW | SCE | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:equity_dividends | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | equity_beginning | 기초 자본 | 30000000000 | 1 | KRW | SCE | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:equity_beginning | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 당기 | equity_other_changes | 기타 자본변동 | 3400000000 | 1 | KRW | SCE | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:equity_other_changes | thstrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | revenue | 매출액 | 60000000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:revenue | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | cost_of_sales | 매출원가 | 45000000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:cost_of_sales | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | gross_profit | 매출총이익 | 15000000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:gross_profit | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | operating_profit | 영업이익 | 4200000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:operating_profit | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | net_income | 전체 당기순이익 | 3000000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:net_income | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | parent_net_income | 지배주주 순이익 | 3000000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | parent | demo:parent_net_income | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | assets | 자산총계 | 55000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:assets | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | liabilities | 부채총계 | 25000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:liabilities | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | equity | 자본총계 | 30000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:equity | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | parent_equity | 지배주주 지분 | 30000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | parent | demo:parent_equity | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | current_assets | 유동자산 | 19000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:current_assets | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | current_liabilities | 유동부채 | 16200000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:current_liabilities | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | cash | 현금및현금성자산 | 6000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:cash | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | receivables | 순매출채권 | 7000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:receivables | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | inventory | 재고자산 | 6000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:inventory | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | cfo | 영업활동현금흐름 | 4000000000 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:cfo | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | cfi | 투자활동현금흐름 | -3000000000 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:cfi | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | cff | 재무활동현금흐름 | 0 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:cff | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | fx_effect | 환율변동효과 | 0 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:fx_effect | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | other_cash_effects | 기타 현금조정 | 0 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:other_cash_effects | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | cash_beginning | 기초 현금 | 5000000000 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:cash_beginning | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | capex_ppe | 유형자산 현금취득 | 2500000000 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:capex_ppe | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | capex_intangible | 무형자산 현금취득 | 500000000 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:capex_intangible | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | borrowings | 차입금(리스 제외) | 14000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:borrowings | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | lease_liabilities | 리스부채 | 2000000000 | 1 | KRW | BS | 2021-12-31 | 2021-12-31 | FY | CFS | total | demo:lease_liabilities | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | interest_expense | 총이자비용 | 1000000000 | 1 | KRW | IS | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:interest_expense | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | oci | 기타포괄손익 | 0 | 1 | KRW | SCE | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:oci | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | dividends_paid | 현금배당 지급 | 2000000000 | 1 | KRW | CF | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:dividends_paid | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | equity_dividends | 자본차감 배당 | 2000000000 | 1 | KRW | SCE | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:equity_dividends | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | equity_beginning | 기초 자본 | 27000000000 | 1 | KRW | SCE | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:equity_beginning | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2022 | 비교기 | equity_other_changes | 기타 자본변동 | 2000000000 | 1 | KRW | SCE | 2021-01-01 | 2021-12-31 | FY | CFS | total | demo:equity_other_changes | frmtrm_amount | DEMO-2022-FY | N/A |  |
| 2023 | 당기 | revenue | 매출액 | 80000000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:revenue | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | cost_of_sales | 매출원가 | 60000000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:cost_of_sales | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | gross_profit | 매출총이익 | 20000000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:gross_profit | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | operating_profit | 영업이익 | 6400000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:operating_profit | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | net_income | 전체 당기순이익 | 4800000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:net_income | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | parent_net_income | 지배주주 순이익 | 4800000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | parent | demo:parent_net_income | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | assets | 자산총계 | 70000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:assets | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | liabilities | 부채총계 | 30000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:liabilities | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | equity | 자본총계 | 40000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:equity | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | parent_equity | 지배주주 지분 | 40000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | parent | demo:parent_equity | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | current_assets | 유동자산 | 26000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:current_assets | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | current_liabilities | 유동부채 | 19500000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:current_liabilities | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | cash | 현금및현금성자산 | 8000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:cash | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | receivables | 순매출채권 | 10000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:receivables | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | inventory | 재고자산 | 8000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:inventory | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | cfo | 영업활동현금흐름 | 6000000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:cfo | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | cfi | 투자활동현금흐름 | -4000000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:cfi | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | cff | 재무활동현금흐름 | -1000000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:cff | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | fx_effect | 환율변동효과 | 0 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:fx_effect | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | other_cash_effects | 기타 현금조정 | 0 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:other_cash_effects | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | cash_beginning | 기초 현금 | 7000000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:cash_beginning | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | capex_ppe | 유형자산 현금취득 | 3500000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:capex_ppe | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | capex_intangible | 무형자산 현금취득 | 500000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:capex_intangible | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | borrowings | 차입금(리스 제외) | 18000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:borrowings | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | lease_liabilities | 리스부채 | 2000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:lease_liabilities | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | interest_expense | 총이자비용 | 1000000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:interest_expense | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | oci | 기타포괄손익 | 0 | 1 | KRW | SCE | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:oci | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | dividends_paid | 현금배당 지급 | 2000000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:dividends_paid | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | equity_dividends | 자본차감 배당 | 2000000000 | 1 | KRW | SCE | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:equity_dividends | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | equity_beginning | 기초 자본 | 35000000000 | 1 | KRW | SCE | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:equity_beginning | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 당기 | equity_other_changes | 기타 자본변동 | 2200000000 | 1 | KRW | SCE | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:equity_other_changes | thstrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | revenue | 매출액 | 70000000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:revenue | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | cost_of_sales | 매출원가 | 52500000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:cost_of_sales | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | gross_profit | 매출총이익 | 17500000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:gross_profit | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | operating_profit | 영업이익 | 4900000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:operating_profit | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | net_income | 전체 당기순이익 | 3600000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:net_income | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | parent_net_income | 지배주주 순이익 | 3600000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | parent | demo:parent_net_income | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | assets | 자산총계 | 62000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:assets | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | liabilities | 부채총계 | 27000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:liabilities | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | equity | 자본총계 | 35000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:equity | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | parent_equity | 지배주주 지분 | 35000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | parent | demo:parent_equity | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | current_assets | 유동자산 | 22500000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:current_assets | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | current_liabilities | 유동부채 | 17600000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:current_liabilities | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | cash | 현금및현금성자산 | 7000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:cash | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | receivables | 순매출채권 | 8500000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:receivables | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | inventory | 재고자산 | 7000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:inventory | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | cfo | 영업활동현금흐름 | 5000000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:cfo | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | cfi | 투자활동현금흐름 | -3500000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:cfi | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | cff | 재무활동현금흐름 | -500000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:cff | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | fx_effect | 환율변동효과 | 0 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:fx_effect | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | other_cash_effects | 기타 현금조정 | 0 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:other_cash_effects | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | cash_beginning | 기초 현금 | 6000000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:cash_beginning | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | capex_ppe | 유형자산 현금취득 | 3000000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:capex_ppe | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | capex_intangible | 무형자산 현금취득 | 500000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:capex_intangible | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | borrowings | 차입금(리스 제외) | 16000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:borrowings | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | lease_liabilities | 리스부채 | 2000000000 | 1 | KRW | BS | 2022-12-31 | 2022-12-31 | FY | CFS | total | demo:lease_liabilities | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | interest_expense | 총이자비용 | 1000000000 | 1 | KRW | IS | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:interest_expense | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | oci | 기타포괄손익 | 0 | 1 | KRW | SCE | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:oci | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | dividends_paid | 현금배당 지급 | 2000000000 | 1 | KRW | CF | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:dividends_paid | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | equity_dividends | 자본차감 배당 | 2000000000 | 1 | KRW | SCE | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:equity_dividends | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | equity_beginning | 기초 자본 | 30000000000 | 1 | KRW | SCE | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:equity_beginning | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2023 | 비교기 | equity_other_changes | 기타 자본변동 | 3400000000 | 1 | KRW | SCE | 2022-01-01 | 2022-12-31 | FY | CFS | total | demo:equity_other_changes | frmtrm_amount | DEMO-2023-FY | N/A |  |
| 2024 | 당기 | revenue | 매출액 | 100000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:revenue | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | cost_of_sales | 매출원가 | 75000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:cost_of_sales | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | gross_profit | 매출총이익 | 25000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:gross_profit | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | operating_profit | 영업이익 | 10000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:operating_profit | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | net_income | 전체 당기순이익 | 8000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:net_income | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | parent_net_income | 지배주주 순이익 | 8000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | parent | demo:parent_net_income | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | assets | 자산총계 | 85000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:assets | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | liabilities | 부채총계 | 40000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:liabilities | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | equity | 자본총계 | 45000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:equity | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | parent_equity | 지배주주 지분 | 45000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | parent | demo:parent_equity | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | current_assets | 유동자산 | 35000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:current_assets | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | current_liabilities | 유동부채 | 26000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:current_liabilities | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | cash | 현금및현금성자산 | 9000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:cash | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | receivables | 순매출채권 | 14000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:receivables | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | inventory | 재고자산 | 12000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:inventory | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | cfo | 영업활동현금흐름 | 7000000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:cfo | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | cfi | 투자활동현금흐름 | -5000000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:cfi | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | cff | 재무활동현금흐름 | -1000000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:cff | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | fx_effect | 환율변동효과 | 0 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:fx_effect | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | other_cash_effects | 기타 현금조정 | 0 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:other_cash_effects | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | cash_beginning | 기초 현금 | 8000000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:cash_beginning | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | capex_ppe | 유형자산 현금취득 | 4500000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:capex_ppe | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | capex_intangible | 무형자산 현금취득 | 500000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:capex_intangible | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | borrowings | 차입금(리스 제외) | 23000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:borrowings | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | lease_liabilities | 리스부채 | 2000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:lease_liabilities | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | interest_expense | 총이자비용 | 1000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:interest_expense | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | oci | 기타포괄손익 | 0 | 1 | KRW | SCE | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:oci | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | dividends_paid | 현금배당 지급 | 2000000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:dividends_paid | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | equity_dividends | 자본차감 배당 | 2000000000 | 1 | KRW | SCE | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:equity_dividends | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | equity_beginning | 기초 자본 | 40000000000 | 1 | KRW | SCE | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:equity_beginning | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 당기 | equity_other_changes | 기타 자본변동 | -1000000000 | 1 | KRW | SCE | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:equity_other_changes | thstrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | revenue | 매출액 | 80000000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:revenue | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | cost_of_sales | 매출원가 | 60000000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:cost_of_sales | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | gross_profit | 매출총이익 | 20000000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:gross_profit | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | operating_profit | 영업이익 | 6400000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:operating_profit | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | net_income | 전체 당기순이익 | 4800000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:net_income | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | parent_net_income | 지배주주 순이익 | 4800000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | parent | demo:parent_net_income | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | assets | 자산총계 | 70000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:assets | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | liabilities | 부채총계 | 30000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:liabilities | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | equity | 자본총계 | 40000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:equity | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | parent_equity | 지배주주 지분 | 40000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | parent | demo:parent_equity | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | current_assets | 유동자산 | 26000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:current_assets | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | current_liabilities | 유동부채 | 19500000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:current_liabilities | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | cash | 현금및현금성자산 | 8000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:cash | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | receivables | 순매출채권 | 10000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:receivables | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | inventory | 재고자산 | 8000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:inventory | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | cfo | 영업활동현금흐름 | 6000000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:cfo | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | cfi | 투자활동현금흐름 | -4000000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:cfi | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | cff | 재무활동현금흐름 | -1000000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:cff | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | fx_effect | 환율변동효과 | 0 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:fx_effect | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | other_cash_effects | 기타 현금조정 | 0 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:other_cash_effects | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | cash_beginning | 기초 현금 | 7000000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:cash_beginning | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | capex_ppe | 유형자산 현금취득 | 3500000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:capex_ppe | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | capex_intangible | 무형자산 현금취득 | 500000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:capex_intangible | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | borrowings | 차입금(리스 제외) | 18000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:borrowings | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | lease_liabilities | 리스부채 | 2000000000 | 1 | KRW | BS | 2023-12-31 | 2023-12-31 | FY | CFS | total | demo:lease_liabilities | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | interest_expense | 총이자비용 | 1000000000 | 1 | KRW | IS | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:interest_expense | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | oci | 기타포괄손익 | 0 | 1 | KRW | SCE | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:oci | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | dividends_paid | 현금배당 지급 | 2000000000 | 1 | KRW | CF | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:dividends_paid | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | equity_dividends | 자본차감 배당 | 2000000000 | 1 | KRW | SCE | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:equity_dividends | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | equity_beginning | 기초 자본 | 35000000000 | 1 | KRW | SCE | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:equity_beginning | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2024 | 비교기 | equity_other_changes | 기타 자본변동 | 2200000000 | 1 | KRW | SCE | 2023-01-01 | 2023-12-31 | FY | CFS | total | demo:equity_other_changes | frmtrm_amount | DEMO-2024-FY | N/A |  |
| 2025 | 당기 | revenue | 매출액 | 120000000000 | 1 | KRW | IS | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:revenue | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | cost_of_sales | 매출원가 | 93000000000 | 1 | KRW | IS | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:cost_of_sales | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | gross_profit | 매출총이익 | 27000000000 | 1 | KRW | IS | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:gross_profit | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | operating_profit | 영업이익 | 10800000000 | 1 | KRW | IS | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:operating_profit | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | net_income | 전체 당기순이익 | 9000000000 | 1 | KRW | IS | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:net_income | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | parent_net_income | 지배주주 순이익 | 9000000000 | 1 | KRW | IS | 2025-01-01 | 2025-12-31 | FY | CFS | parent | demo:parent_net_income | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | assets | 자산총계 | 100000000000 | 1 | KRW | BS | 2025-12-31 | 2025-12-31 | FY | CFS | total | demo:assets | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | liabilities | 부채총계 | 52000000000 | 1 | KRW | BS | 2025-12-31 | 2025-12-31 | FY | CFS | total | demo:liabilities | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | equity | 자본총계 | 48000000000 | 1 | KRW | BS | 2025-12-31 | 2025-12-31 | FY | CFS | total | demo:equity | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | parent_equity | 지배주주 지분 | 48000000000 | 1 | KRW | BS | 2025-12-31 | 2025-12-31 | FY | CFS | parent | demo:parent_equity | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | current_assets | 유동자산 | 49000000000 | 1 | KRW | BS | 2025-12-31 | 2025-12-31 | FY | CFS | total | demo:current_assets | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | current_liabilities | 유동부채 | 33800000000 | 1 | KRW | BS | 2025-12-31 | 2025-12-31 | FY | CFS | total | demo:current_liabilities | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | cash | 현금및현금성자산 | 10000000000 | 1 | KRW | BS | 2025-12-31 | 2025-12-31 | FY | CFS | total | demo:cash | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | receivables | 순매출채권 | 22000000000 | 1 | KRW | BS | 2025-12-31 | 2025-12-31 | FY | CFS | total | demo:receivables | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | inventory | 재고자산 | 17000000000 | 1 | KRW | BS | 2025-12-31 | 2025-12-31 | FY | CFS | total | demo:inventory | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | cfo | 영업활동현금흐름 | 4500000000 | 1 | KRW | CF | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:cfo | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | cfi | 투자활동현금흐름 | -8000000000 | 1 | KRW | CF | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:cfi | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | cff | 재무활동현금흐름 | 4500000000 | 1 | KRW | CF | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:cff | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | fx_effect | 환율변동효과 | 0 | 1 | KRW | CF | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:fx_effect | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | other_cash_effects | 기타 현금조정 | 0 | 1 | KRW | CF | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:other_cash_effects | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | cash_beginning | 기초 현금 | 9000000000 | 1 | KRW | CF | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:cash_beginning | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | capex_ppe | 유형자산 현금취득 | 7500000000 | 1 | KRW | CF | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:capex_ppe | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | capex_intangible | 무형자산 현금취득 | 500000000 | 1 | KRW | CF | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:capex_intangible | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | borrowings | 차입금(리스 제외) | 32000000000 | 1 | KRW | BS | 2025-12-31 | 2025-12-31 | FY | CFS | total | demo:borrowings | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | lease_liabilities | 리스부채 | 2000000000 | 1 | KRW | BS | 2025-12-31 | 2025-12-31 | FY | CFS | total | demo:lease_liabilities | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | interest_expense | 총이자비용 | 1800000000 | 1 | KRW | IS | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:interest_expense | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | oci | 기타포괄손익 | 0 | 1 | KRW | SCE | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:oci | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | dividends_paid | 현금배당 지급 | 2000000000 | 1 | KRW | CF | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:dividends_paid | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | equity_dividends | 자본차감 배당 | 2000000000 | 1 | KRW | SCE | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:equity_dividends | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | equity_beginning | 기초 자본 | 44000000000 | 1 | KRW | SCE | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:equity_beginning | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 당기 | equity_other_changes | 기타 자본변동 | -3000000000 | 1 | KRW | SCE | 2025-01-01 | 2025-12-31 | FY | CFS | total | demo:equity_other_changes | thstrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | revenue | 매출액 | 100000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:revenue | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | cost_of_sales | 매출원가 | 75000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:cost_of_sales | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | gross_profit | 매출총이익 | 25000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:gross_profit | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | operating_profit | 영업이익 | 10000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:operating_profit | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | net_income | 전체 당기순이익 | 8000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:net_income | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | parent_net_income | 지배주주 순이익 | 8000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | parent | demo:parent_net_income | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | assets | 자산총계 | 84000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:assets | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | liabilities | 부채총계 | 40000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:liabilities | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | equity | 자본총계 | 44000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:equity | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | parent_equity | 지배주주 지분 | 44000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | parent | demo:parent_equity | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | current_assets | 유동자산 | 35000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:current_assets | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | current_liabilities | 유동부채 | 26000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:current_liabilities | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | cash | 현금및현금성자산 | 9000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:cash | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | receivables | 순매출채권 | 14000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:receivables | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | inventory | 재고자산 | 12000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:inventory | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | cfo | 영업활동현금흐름 | 7000000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:cfo | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | cfi | 투자활동현금흐름 | -5000000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:cfi | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | cff | 재무활동현금흐름 | -1000000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:cff | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | fx_effect | 환율변동효과 | 0 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:fx_effect | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | other_cash_effects | 기타 현금조정 | 0 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:other_cash_effects | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | cash_beginning | 기초 현금 | 8000000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:cash_beginning | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | capex_ppe | 유형자산 현금취득 | 4500000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:capex_ppe | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | capex_intangible | 무형자산 현금취득 | 500000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:capex_intangible | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | borrowings | 차입금(리스 제외) | 23000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:borrowings | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | lease_liabilities | 리스부채 | 2000000000 | 1 | KRW | BS | 2024-12-31 | 2024-12-31 | FY | CFS | total | demo:lease_liabilities | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | interest_expense | 총이자비용 | 1000000000 | 1 | KRW | IS | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:interest_expense | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | oci | 기타포괄손익 | 0 | 1 | KRW | SCE | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:oci | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | dividends_paid | 현금배당 지급 | 2000000000 | 1 | KRW | CF | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:dividends_paid | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | equity_dividends | 자본차감 배당 | 2000000000 | 1 | KRW | SCE | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:equity_dividends | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | equity_beginning | 기초 자본 | 40000000000 | 1 | KRW | SCE | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:equity_beginning | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2025 | 비교기 | equity_other_changes | 기타 자본변동 | -1000000000 | 1 | KRW | SCE | 2024-01-01 | 2024-12-31 | FY | CFS | total | demo:equity_other_changes | frmtrm_amount | DEMO-2025-FY | N/A |  |
| 2026 H1 | 당기 | revenue | 매출액 | 64000000000 | 1 | KRW | IS | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:revenue | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | cost_of_sales | 매출원가 | 50000000000 | 1 | KRW | IS | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:cost_of_sales | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | gross_profit | 매출총이익 | 14000000000 | 1 | KRW | IS | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:gross_profit | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | operating_profit | 영업이익 | 5200000000 | 1 | KRW | IS | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:operating_profit | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | net_income | 전체 당기순이익 | 4000000000 | 1 | KRW | IS | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:net_income | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | parent_net_income | 지배주주 순이익 | 4000000000 | 1 | KRW | IS | 2026-01-01 | 2026-06-30 | YTD | CFS | parent | demo:parent_net_income | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | assets | 자산총계 | 108000000000 | 1 | KRW | BS | 2026-06-30 | 2026-06-30 | YTD | CFS | total | demo:assets | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | liabilities | 부채총계 | 56500000000 | 1 | KRW | BS | 2026-06-30 | 2026-06-30 | YTD | CFS | total | demo:liabilities | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | equity | 자본총계 | 51500000000 | 1 | KRW | BS | 2026-06-30 | 2026-06-30 | YTD | CFS | total | demo:equity | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | parent_equity | 지배주주 지분 | 51500000000 | 1 | KRW | BS | 2026-06-30 | 2026-06-30 | YTD | CFS | parent | demo:parent_equity | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | current_assets | 유동자산 | 55000000000 | 1 | KRW | BS | 2026-06-30 | 2026-06-30 | YTD | CFS | total | demo:current_assets | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | current_liabilities | 유동부채 | 37000000000 | 1 | KRW | BS | 2026-06-30 | 2026-06-30 | YTD | CFS | total | demo:current_liabilities | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | cash | 현금및현금성자산 | 11000000000 | 1 | KRW | BS | 2026-06-30 | 2026-06-30 | YTD | CFS | total | demo:cash | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | receivables | 순매출채권 | 23500000000 | 1 | KRW | BS | 2026-06-30 | 2026-06-30 | YTD | CFS | total | demo:receivables | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | inventory | 재고자산 | 19000000000 | 1 | KRW | BS | 2026-06-30 | 2026-06-30 | YTD | CFS | total | demo:inventory | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | cfo | 영업활동현금흐름 | 3000000000 | 1 | KRW | CF | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:cfo | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | cfi | 투자활동현금흐름 | -4500000000 | 1 | KRW | CF | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:cfi | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | cff | 재무활동현금흐름 | 2500000000 | 1 | KRW | CF | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:cff | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | fx_effect | 환율변동효과 | 0 | 1 | KRW | CF | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:fx_effect | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | other_cash_effects | 기타 현금조정 | 0 | 1 | KRW | CF | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:other_cash_effects | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | cash_beginning | 기초 현금 | 10000000000 | 1 | KRW | CF | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:cash_beginning | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | capex_ppe | 유형자산 현금취득 | 4000000000 | 1 | KRW | CF | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:capex_ppe | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | capex_intangible | 무형자산 현금취득 | 500000000 | 1 | KRW | CF | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:capex_intangible | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | borrowings | 차입금(리스 제외) | 35000000000 | 1 | KRW | BS | 2026-06-30 | 2026-06-30 | YTD | CFS | total | demo:borrowings | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | lease_liabilities | 리스부채 | 2000000000 | 1 | KRW | BS | 2026-06-30 | 2026-06-30 | YTD | CFS | total | demo:lease_liabilities | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | interest_expense | 총이자비용 | 900000000.0 | 1 | KRW | IS | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:interest_expense | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | oci | 기타포괄손익 | 0 | 1 | KRW | SCE | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:oci | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | dividends_paid | 현금배당 지급 | 1000000000 | 1 | KRW | CF | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:dividends_paid | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | equity_dividends | 자본차감 배당 | 1000000000 | 1 | KRW | SCE | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:equity_dividends | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | equity_beginning | 기초 자본 | 48000000000 | 1 | KRW | SCE | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:equity_beginning | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 당기 | equity_other_changes | 기타 자본변동 | 500000000 | 1 | KRW | SCE | 2026-01-01 | 2026-06-30 | YTD | CFS | total | demo:equity_other_changes | thstrm_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | revenue | 매출액 | 58000000000 | 1 | KRW | IS | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:revenue | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | cost_of_sales | 매출원가 | 44000000000 | 1 | KRW | IS | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:cost_of_sales | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | gross_profit | 매출총이익 | 14000000000 | 1 | KRW | IS | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:gross_profit | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | operating_profit | 영업이익 | 5500000000 | 1 | KRW | IS | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:operating_profit | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | net_income | 전체 당기순이익 | 4300000000 | 1 | KRW | IS | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:net_income | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | parent_net_income | 지배주주 순이익 | 4300000000 | 1 | KRW | IS | 2025-01-01 | 2025-06-30 | YTD | CFS | parent | demo:parent_net_income | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | assets | 자산총계 | 92000000000 | 1 | KRW | BS | 2025-06-30 | 2025-06-30 | YTD | CFS | total | demo:assets | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | liabilities | 부채총계 | 45000000000 | 1 | KRW | BS | 2025-06-30 | 2025-06-30 | YTD | CFS | total | demo:liabilities | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | equity | 자본총계 | 47000000000 | 1 | KRW | BS | 2025-06-30 | 2025-06-30 | YTD | CFS | total | demo:equity | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | parent_equity | 지배주주 지분 | 47000000000 | 1 | KRW | BS | 2025-06-30 | 2025-06-30 | YTD | CFS | parent | demo:parent_equity | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | current_assets | 유동자산 | 55000000000 | 1 | KRW | BS | 2025-06-30 | 2025-06-30 | YTD | CFS | total | demo:current_assets | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | current_liabilities | 유동부채 | 37000000000 | 1 | KRW | BS | 2025-06-30 | 2025-06-30 | YTD | CFS | total | demo:current_liabilities | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | cash | 현금및현금성자산 | 9500000000 | 1 | KRW | BS | 2025-06-30 | 2025-06-30 | YTD | CFS | total | demo:cash | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | receivables | 순매출채권 | 18000000000 | 1 | KRW | BS | 2025-06-30 | 2025-06-30 | YTD | CFS | total | demo:receivables | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | inventory | 재고자산 | 14500000000 | 1 | KRW | BS | 2025-06-30 | 2025-06-30 | YTD | CFS | total | demo:inventory | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | cfo | 영업활동현금흐름 | 2800000000 | 1 | KRW | CF | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:cfo | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | cfi | 투자활동현금흐름 | -3500000000 | 1 | KRW | CF | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:cfi | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | cff | 재무활동현금흐름 | 1200000000 | 1 | KRW | CF | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:cff | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | fx_effect | 환율변동효과 | 0 | 1 | KRW | CF | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:fx_effect | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | other_cash_effects | 기타 현금조정 | 0 | 1 | KRW | CF | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:other_cash_effects | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | cash_beginning | 기초 현금 | 9000000000 | 1 | KRW | CF | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:cash_beginning | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | capex_ppe | 유형자산 현금취득 | 3000000000 | 1 | KRW | CF | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:capex_ppe | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | capex_intangible | 무형자산 현금취득 | 500000000 | 1 | KRW | CF | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:capex_intangible | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | borrowings | 차입금(리스 제외) | 35000000000 | 1 | KRW | BS | 2025-06-30 | 2025-06-30 | YTD | CFS | total | demo:borrowings | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | lease_liabilities | 리스부채 | 2000000000 | 1 | KRW | BS | 2025-06-30 | 2025-06-30 | YTD | CFS | total | demo:lease_liabilities | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | interest_expense | 총이자비용 | 900000000.0 | 1 | KRW | IS | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:interest_expense | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | oci | 기타포괄손익 | 0 | 1 | KRW | SCE | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:oci | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | dividends_paid | 현금배당 지급 | 1000000000 | 1 | KRW | CF | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:dividends_paid | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | equity_dividends | 자본차감 배당 | 1000000000 | 1 | KRW | SCE | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:equity_dividends | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | equity_beginning | 기초 자본 | 45000000000 | 1 | KRW | SCE | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:equity_beginning | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |
| 2026 H1 | 비교기 | equity_other_changes | 기타 자본변동 | -1300000000 | 1 | KRW | SCE | 2025-01-01 | 2025-06-30 | YTD | CFS | total | demo:equity_other_changes | frmtrm_add_amount | DEMO-2026-YTD | N/A |  |

대조 통과는 확보된 자료의 계산식 일치입니다. 미완료 대조·주석은 이상 없음으로 해석하지 않습니다.
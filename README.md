# DART 기업분석실

저장소 이름: `dart-financial-analyst` · 저장소 개요: [REPOSITORY_OVERVIEW.ko.md](REPOSITORY_OVERVIEW.ko.md)

개발/검토 문서: [현재 명세](DEVELOPMENT_SPEC.ko.md), [개선 과제](IMPROVEMENTS.ko.md), [상세 디버깅](DEBUGGING_HISTORY.ko.md), [검증 기업 17개와 근거 수준](VERIFIED_COMPANIES.ko.md), [후속 개발](NEXT_SESSION.ko.md). 최종 제출 실검증은 그중 5개 기업입니다. 이 목록이 모든 대조 완료를 뜻하지 않습니다.

한국 기업의 OpenDART 재무제표를 수집해 과거 계정 변화, 손익·현금흐름·재무상태표 연결, 계산 근거를 확인하는 로컬 웹 앱입니다. **2026-11-07 제출 검증본**입니다. 지원 범위와 미완료 대조를 함께 제공하며, 전체 공시의 감사 시스템은 아닙니다.

최종 검증은 Windows / Python 3.14.4에서 원클릭 첫 설치, 전체 테스트 251개, 금융업 포함 5개 기업·27개 기간의 실공시, Ollama 메모·RSS 선정, HTML·Excel·Markdown·JSON 내보내기로 수행했습니다. 실제 원천의 불일치·자료 부족은 보고서에 그대로 남깁니다. 자세한 증거는 제출본 `validation`과 `reports/verification.json`, 최신 `VERIFICATION.md`를 참조하세요.

생성한 Ollama 메모는 해당 자료의 식별값이 일치할 때 HTML·Excel·Markdown에 포함됩니다. 원천 자료만 담는 Dataset JSON을 가져온 경우 메모는 다시 생성하세요. `requirements-tested.txt`는 검증 환경의 직접 의존성 버전이며, `requirements-lock-windows-py314.txt`는 제출본에 포함한 정확한 환경 기록입니다. 다른 Python/운영체제는 같은 수준의 설치 검증을 수행하지 않았습니다.

## 바로 실행

Python 3.11 이상이 필요합니다. macOS/Linux:

```bash
bash run.sh
```

브라우저에서 http://localhost:8501 을 엽니다. 첫 화면에는 실제 기업과 구분된 가상 검증 자료가 나옵니다.

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

Windows에서는 `DART_Analyst_Start.cmd`를 더블클릭하면 가상환경·필수 패키지·Ollama를 확인한 뒤 앱과 브라우저를 실행합니다. 첫 실행에는 패키지 설치 시간이 필요합니다.

## 실제 기업 조회

1. [OpenDART](https://opendart.fss.or.kr/)에서 인증키를 발급합니다.
2. 왼쪽의 **DART 기업 조회**를 선택하고 인증키와 회사명/종목코드를 입력합니다.
3. 검색한 기업, 3~5개 연간 기간, 연결/별도 기준을 선택해 수집합니다.
4. 상세 기간을 바꿔 계정 비교, 대조 상태, 산식, 원문 출처를 확인합니다.
5. Excel·HTML·Markdown 보고서 및 원천 JSON을 내려받습니다.

인증키는 화면에서 입력하거나 `DART_API_KEY` 환경변수로 설정합니다. 보고서에는 포함하지 않습니다. `.env`는 앱 시작 시 자동으로 읽으며 `.env.example`은 설정 예시입니다. 서버는 기본적으로 본인 컴퓨터의 127.0.0.1에서만 열립니다.

## 구현 기능

- 회사명/종목코드 검색, 최신 이용 가능 사업보고서 기준 다년 조회, 최신 중간보고서 추가.
- 최종 공시의 접수번호와 재무 API 응답 일치 확인. 연결/별도를 자동 혼합하지 않음.
- 원천 전체 계정 보존, 표준 계정 매핑, 현재 공시의 비교금액 우선 사용, 기존 공시와 재작성 차이 표시.
- 매출 성장률, 이익률, 유동·부채비율, 이자보상, 순이익 현금전환, CAPEX·FCF, ROE·ROA, DSO·DIO, 발생액 지표.
- 자산=부채+자본, 매출−원가=총이익, 현금 및 자본 연결 대조. 일치/불일치/자료 부족/기준 불일치를 구분.
- 회계정책, 차입금·유동성, 우발채무·약정, 특수관계자, 감사의견 관련 원문 문단 탐색.
- 근거·산식·비교기·원천 계정이 포함된 Excel·HTML·Markdown 내보내기. HTML은 브라우저 인쇄로 PDF 저장 가능.
- 검증 시나리오: 정상, 재작성, 환율효과 누락, 기말 현금 5억 원 불일치.
- 선택적 Ollama AI 검토 설명. 로컬 모델이 필요하며 사용자가 생성 버튼을 누를 때만 호출합니다.

숫자는 Python `Decimal`로 계산하고, Excel 원천 금액은 큰 정수의 정밀도를 지키기 위해 문자열로 저장합니다. 표시 차트만 부동소수점·억 원 단위를 사용합니다. 비교 가능한 영업이익·순이익이 흑자와 적자 사이에서 바뀌면 요약과 주요 지표에 전환을 표시합니다. AI 검토 메모를 생성하면 로컬 Ollama가 최신 기간의 지표·주석과 업종별 검토 관점을 고릅니다. 메모에는 비교 수치와 공시번호, 업종 배경, 원문에서 확인할 질문을 구분해 표시합니다.

## 지원 범위와 보류 규칙

현재 지원은 **전업종의 12월 결산 원화 공시, 연간 및 누적 중간 실적**입니다. 금융·보험 업종 분류에서도 공시 계정 비교와 회계 대조를 제공합니다. 이자보상배율, DSO·DIO 등 업종에 따라 해석이 달라지는 일부 일반기업용 지표는 적용을 보류합니다.

개요의 **최근 경제 뉴스 · 연합인포맥스**에서 최근 뉴스를 불러올 수 있습니다. IB/기업, 정책/금융, 채권/외환 공식 RSS의 최근 제공분 중 7일 이내 기사를 표시하며, 기업·업종 관련성과 발행일로 정렬합니다. 조회 결과는 5분간 캐시합니다. **Ollama로 핵심 3~5건 선정**을 누르면 모델이 기사와 RSS 제공 핵심 문장을 고릅니다. 발행 시각과 원문 링크를 함께 제공합니다.

- 분기 손익은 누적 필드를 사용합니다. 분기 CF/SCE는 전체계정 API만으로 정확한 기간을 확인하지 못하므로 계산을 보류합니다.
- 연간 기간은 12월 결산 정규 사업연도(1월~12월)를 가정합니다. 단기 사업연도·결산기 변경은 지원하지 않으며, 원문 또는 XBRL 기간 문맥을 추가 확인해야 합니다.
- 중간 재무상태표의 비교금액은 통상 전년 말입니다. 이를 전년 동분기 잔액으로 바꾸지 않습니다.
- 전기 비교금액 재작성은 감지하지만, 정정 전 모든 공시 버전을 내려받는 변경 이력 저장소는 아직 없습니다.
- 비표준·동일 후보 복수·불확실한 계정은 미매핑 상태로 보존합니다. 원천 전체 행을 가져왔다고 모든 계정을 경제적으로 연결한 것은 아닙니다.
- 누락은 0이 아닙니다. 현금의 기타 조정, 배당, 자본 변동의 모든 항목이 확보되지 않으면 대조가 미완료로 남습니다. 실공시에서는 이 상태가 흔할 수 있습니다.
- 차입금의 리스 포함 여부는 별도 확인이 필요합니다. 단순 리스 가산으로 총차입금을 만들지 않습니다.
- 연결 ROE는 지배주주 순이익/평균 지배주주지분으로 계산합니다. 중간 ROE/ROA는 자동 연율화하지 않습니다. DSO는 외상매출 대신 총매출을 사용하는 근사치입니다.
- 주석은 관련 문단 발췌입니다. 모든 표·각주·연결범위 변화·회계정책 변경의 자동 해석, 산업별 분석, 동종기업 비교, 비현금 거래 전체 대사는 후속 범위입니다.
- 주석 발췌 없음은 위험 없음이 아닙니다. 대조 일치도 전체 재무제표의 완전성·감사의견을 뜻하지 않습니다.

저장 JSON 가져오기는 원본 공시를 재조회하지 않습니다. 실제 기업 검토에서는 자료의 출처와 정정 여부를 확인해야 합니다. AI 사용 시 계산 지표와 발췌 문단이 이 컴퓨터에서 실행 중인 Ollama로 전송됩니다.

## 명령행 보고서

화면 없이 가상 자료로 보고서를 생성할 수 있습니다.

```bash
.venv/bin/python -m dart_analyst --output reports/demo
.venv/bin/python -m dart_analyst --scenario cash_mismatch --output reports/mismatch
.venv/bin/python -m dart_analyst --input reports/demo/dataset.json --output reports/reloaded
```

실제 기업은 환경변수에 키를 설정한 후 회사 고유번호(종목코드와 다름)를 전달합니다.

```bash
.venv/bin/python -m dart_analyst --corp-code 00126380 --name 삼성전자 --years 5 --scope CFS --output reports/company
```

기존 출력 폴더의 같은 이름 보고서는 덮어씁니다. `.venv`가 없는 경우 먼저 설치 명령을 실행하세요.

## 검증 및 구조

```bash
.venv/bin/python -m pytest -q
```

테스트는 계산·재작성·기간/통화/귀속·누락·중복 계정, OpenDART 모의 응답, XML/ZIP 처리, 보고서 출력과 UI 흐름을 검증합니다. 실제 OpenDART와 로컬 Ollama도 별도로 검증했습니다. 최근 실공시 결과와 남은 보류 항목은 `VERIFICATION.md`를 참고하세요.

| 파일 | 역할 |
| --- | --- |
| `app.py` | Streamlit 실행 진입점 |
| `dart_analyst/ui.py`, `ui.css` | 화면 구성과 스타일 |
| `dart_analyst/presentation.py` | 금액·상태·표 표시 형식 |
| `dart_analyst/dart_client.py` | OpenDART 수집, 계정 매핑 |
| `dart_analyst/dart_notes.py` | 원문 ZIP/XML 안전 처리와 주석 탐색 |
| `dart_analyst/models.py` | 기간·계정·출처 모델과 JSON 저장 |
| `dart_analyst/engine.py` | 지표, 비교, 회계 연결 계산 |
| `dart_analyst/account_history.py` | 원천 계정별 다년 비교 |
| `dart_analyst/narrative.py` | 근거 기반 요약과 선택 AI 설명 |
| `dart_analyst/exporters.py` | 보고서 출력 |
| `dart_analyst/demo.py` | 명확히 구분된 가상 시나리오 |

공식 API 설명은 [OpenDART 개발가이드](https://opendart.fss.or.kr/guide/main.do)를 참고하세요. API 사양과 실제 기업별 공시 구조가 달라질 수 있으므로, 실제 키로 대표 기업을 검증한 뒤 계정별 매핑 범위를 확장하는 순서가 필요합니다.

구현 세부 계약은 [개발 명세](DEVELOPMENT_SPEC.ko.md), 실행 검증과 예제별 상태는 [검증 기록](VERIFICATION.md)을 참고하세요. `reports/`에 네 가지 가상 시나리오의 보고서를 포함했습니다.

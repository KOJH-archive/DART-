# DART 기업분석실 개발명세서

기준일 2026-11-07. 최종 제출 코드 기준 통합 개정 v2. 이번 개정은 문서 작업이며 앱의 계산 로직을 변경하지 않았습니다.

## 1. 제품 목적과 판정

기업명 또는 종목코드로 OpenDART 공시를 수집하고 다년 계정 비교, 결정적 재무 계산, 회계 대조, 공시 근거와 로컬 AI 검토 메모를 제공하는 로컬 웹 앱입니다. 특정 기업 전용 구현이 아닙니다.

현재는 **지원 범위와 미완료 항목을 명시한 제출 검증본**입니다. 정상 조회·보고서 생성과 모든 계정의 대조 완료는 다릅니다. 테스트 251개와 표본 검증을 모든 기업·주석의 완전성 보증으로 표현하지 않습니다.

관련 문서(앱 루트): IMPROVEMENTS.ko.md, DEBUGGING_HISTORY.ko.md, VERIFIED_COMPANIES.ko.md/JSON, VERIFICATION.md, NEXT_SESSION.ko.md. 통합 이전 명세와 인수인계는 docs/archive에 보존합니다.

## 2. 지원과 검증 범위

- 전업종 중 12월 정규 결산·KRW, 연간 FY와 누적 YTD를 지원합니다.
- 연결 CFS와 별도 OFS는 사용자 선택을 따르며 자동 혼합·대체하지 않습니다. 최신 실제 표본 검증은 주로 CFS입니다.
- 금융·보험도 수집합니다. 다만 업종 코드 64/65/66에는 일반기업용 지표 일부를 적용 보류합니다. 은행·보험 전용 감독 지표는 미구현입니다.
- 비12월 결산, 결산기 변경·단기 사업연도, 다중 통화 분석, 모든 정정 버전 저장, 동종기업 비교, 모든 확장 계정·주석 표 해석은 미지원입니다.
- 기본 127.0.0.1:8501의 단일 사용자 앱입니다. 인터넷 공개·인증·권한관리·다중 사용자 운영은 검증 범위 밖입니다.
- 최초 설치를 확인한 환경은 Windows / Python 3.14.4입니다. requirements가 Python 3.11 이상을 허용하는 것과 다른 환경의 실제 설치 검증은 구별합니다.

## 3. 실행과 설정

실제 개발 앱 루트: `C:\Users\jongh\Downloads\dart-analyst-ui\dart-analyst`. Codex 채팅 폴더와 다릅니다. 확인 당시 이 앱 폴더에는 Git 저장소가 없었습니다.

진입 순서는 DART_Analyst_Start.cmd → run_windows.ps1 → .venv Python → streamlit run app.py → dart_analyst.ui.main()입니다. CMD는 ASCII, PS1은 UTF-8 BOM을 유지합니다.

런처는 Python/Ollama 경로, .env, 가상환경, 의존성 import·버전 범위, 필요 시 설치, Ollama 서비스·모델, 앱 기동을 확인합니다. -CheckOnly는 최초 설치 검증을 대신하지 않습니다. -NoBrowser -Port 8774는 별도 포트 검증용입니다.

설정 키는 DART_API_KEY, OLLAMA_BASE_URL, OLLAMA_MODEL입니다. Ollama 기본값은 http://127.0.0.1:11434 / qwen3.5:4b입니다. Python은 dotenv를 읽지만 런처의 일부 설정은 별도 간이 파서이므로 복잡한 .env 인용·주석 형식의 완전한 일치는 확인하지 않았습니다.

requirements.txt는 허용 범위, requirements-tested.txt는 검증한 직접 버전입니다. 제출본의 requirements-lock-windows-py314.txt는 고정 환경 기록입니다. 실제 런처 첫 설치는 범위 파일을 사용하므로 미래의 전이 의존성이 자동 고정되는 것은 아닙니다.

## 4. 모듈 책임

- app.py: 환경 로드와 진입.
- dart_client.py: 기업 검색·개황·공시 선택·전체계정, _normalize(), _apply_xbrl(), 명시적 부채 구성 검증, 원본 공백 기록.
- xbrl.py: ZIP/XML 수치·QName·문맥·통화·정밀도, ZIP 내부 XSD와 한글 라벨 연결.
- models.py: Dataset/Period/Fact와 JSON 검증.
- engine.py: Decimal 계산, 입력 적합성, 지표·비교·회계 대조·관찰·커버리지.
- account_history.py: 원천 행의 과거 비교·재작성 차이·제한.
- dart_notes.py: 제한적 본문 보정과 주제별 원문 발췌.
- narrative.py / industry_review.py: 규칙 요약, AI 근거 검증·자료 식별, 정적 업종 배경·질문.
- news.py: 연합인포맥스 RSS와 기사·문장 선별.
- presentation.py / ui.py / ui.css: 표시·세션·조회·차트·다운로드.
- exporters.py / __main__.py: 보고서와 CLI 분석·저장.

## 5. 데이터 계약

Dataset은 company/corp_code/stock_code/scope/source_mode/periods/notes/issues/metadata를 가집니다. Period는 label/year/start/end/scope/kind/filing_id, facts(당기), comparatives(현재 공시 비교값), raw_accounts(미매핑 포함 원천), issues를 가집니다.

Fact는 key/name/amount/unit/currency/statement/start/end/period_kind/scope/attribution/account_id/source_id/source_url/source_field/reason/source_details를 가집니다. 금액·배율은 Decimal입니다. None과 공시된 0은 다릅니다.

source_id는 접수번호, source_details는 API·보고서 코드·파일·QName·문맥·축·구성원·원금액·정밀도·교차 검증값입니다. source_field는 API 열 또는 xbrl_fact/xbrl_verified_api 등을 구별합니다.

BS는 시점, IS/CIS/CF/SCE는 흐름입니다. CFS/OFS, 전체/지배주주, FY/YTD, 분기 단독/누적을 혼합하지 않습니다. 기타 조정은 차액으로 만들지 않습니다.

JSON 입력은 10 MiB와 금액·단위·날짜·중복 등의 기본 검증을 적용합니다. 원본을 다시 조회하지 않으며 가져온 자료임을 표시합니다. Dataset JSON은 AI 메모 저장 형식이 아닙니다.

## 6. 수집 계약

API: corpCode.xml, company.json, list.json, fnlttSinglAcntAll.json, fnlttXbrl.xml, document.xml.

search_companies(query) 후 load_company(corp_code, name, stock_code='', years=5, scope='CFS', include_interim=True)를 사용합니다. 기본은 최근 연간 5개와 최신 중간보고서입니다.

기간별 최종 접수번호를 선택합니다. 전체계정의 회사·접수번호가 다르거나 전체계정이 없으면 해당 행을 배제하고 선택한 공시의 XBRL 복구를 시도합니다. 불가 시 기간을 제외하고 metadata.filing_gaps에 선택/API 번호와 사유를 기록합니다. 원본 없는 기간을 오래된 행으로 몰래 대체하지 않습니다.

정상 수집에서 XBRL 자체 요청·파싱이 실패하면 전체계정 결과와 보류 안내를 유지합니다. 전체계정만의 결과와 XBRL 교차 확인 결과는 보증 수준이 다릅니다.

전체계정 연간은 정규 1월~12월을 가정합니다. 중간 IS/CIS는 add_amount 누적 열을 사용합니다. CF/SCE는 API만으로 누적을 단정하지 않으며 XBRL로 실제 기간을 검증합니다. 중간 BS 비교열은 전년 말입니다.

## 7. 계정 매핑과 XBRL 검증

표준 XBRL ID와 승인된 정확 계정명을 사용합니다. 복수 후보·표준 ID/이름 충돌·귀속 불명은 보류합니다. IS/CIS 반복은 동일 개념·통화·단위·구성원, 당기/비교 금액 및 열 존재 여부가 모두 같을 때만 통합하고 원래 행을 보존합니다.

XBRL은 회사 식별자·스킴, scope, 추가 차원 없음, 기타 문맥 내용 없음, KRW, 실제 기간/시점을 확인합니다. 값이 같다는 이유로 서로 다른 차원을 합치지 않습니다.

decimals는 반올림 정밀도이지 배율이 아닙니다. 원본 반올림 구간에 API 값이 들어오면 더 정밀한 API 금액을 사용하고 양쪽 출처를 남깁니다. 명시적 유동·비유동 합계는 구성 개념 각각을 XBRL로 검증합니다. 차입금의 리스 포함 여부는 별도 확인합니다.

회사 확장 계정은 ZIP의 XSD 실제 요소 ID/name/namespace와 한글 표준 라벨을 연결합니다. 회사 namespace와 승인된 단일 정확 라벨을 확인합니다. 승인 범위는 소유주 거래 합계·매각예정 현금 대체·처분집단 현금 순증감입니다. 최신 *_lab-ko.xml과 구형 lab_*-ko_YYYY-MM-DD.xml을 지원합니다. 모든 확장 계정이나 계산 링크베이스의 일반 합산 관계를 지원하는 것은 아닙니다.

## 8. 과거 비교

원천 행의 기본 비교 키는 재무제표 + account_id + account_detail입니다. 미매핑 행도 보존하되 경제적으로 모두 연결됐다고 보증하지 않습니다.

현재 공시 비교열을 우선합니다. 명시적 빈칸·오류는 과거 값으로 덮지 않습니다. 비교열 자체가 없을 때만 호환 과거 자료를 사용합니다. 기존 공시와의 차이·출처·재작성 표시를 보존하지만 모든 정정 버전을 저장하지는 않습니다.

## 9. 계산과 대조

analyze(dataset)는 metrics/comparisons/checks/observations/coverage/account_history를 반환합니다. 산식·입력·출처·기간·단위·상태·보류 사유를 제공합니다.

지표: 성장률, 이익률, 유동·부채비율, 이자보상, CFO/순이익, 차입금−현금, CAPEX/FCF, ROE/ROA, DSO/DIO, 현금흐름식 발생액입니다. 분모 0/음수는 비율을 보류합니다. 전기 0/음수 증감은 차액만 제공합니다. ROE는 같은 귀속의 순이익/평균 지분을 사용합니다. YTD를 연율화하지 않으며 DSO는 총매출 근사치입니다.

대조: 자산=부채+자본, 매출−원가=총이익, 현금 연결, 자본 연결. 자료가 있으면 공시 순증감 연결과 순이익+OCI=총포괄손익이 추가됩니다. 모든 자료의 검사 수가 항상 6개인 것은 아닙니다.

현금 순증감의 환율 포함 범위는 CFO/CFI/CFF/FX와 독립 대조하며 태그 이름만 보고 FX를 재가산하지 않습니다. 명시된 매각예정 조정만 반영하며 워터폴도 실제 입력을 표시합니다. 미확인 기타 조정을 0으로 생성하지 않습니다.

상세 자본 대조가 미완료이고 명시적 소유주 거래 합계가 있으면 기초 자본+총포괄손익+소유주 거래 합계=기말을 별도 기준으로 검증합니다. 합계 통과가 상세 배당·자본 변동의 완전 확보를 뜻하지 않습니다. 전체 SCE 차원 roll-forward는 미구현입니다.

pass는 확보 산식 일치, fail은 허용오차 초과, incomplete는 자료 부족, not_comparable은 기준 불일치입니다. fail을 공시 오류 확정으로 해석하지 않습니다. 지표에는 calculated/missing_source/invalid_denominator/not_applicable 등 별도 상태가 있습니다.

## 10. 원문과 안전 한도

7개 주제: 회계정책, 차입금·유동성, 우발채무·약정, 특수관계자, 감사의견 관련 본문, 사업부문·수익구조, 원가·운전자본. 문단 탐색·발췌이지 감사의견 판정이나 표 전체 수치 대조가 아닙니다.

관찰된 앰퍼샌드·짧은 꺾쇠 본문·TE/TD/TH의 제한된 ENG 따옴표만 보정하고 엄격 XML 파서를 다시 적용합니다. DTD·엔티티·외부 참조·허용되지 않은 경로는 거부합니다.

document.xml: ZIP 30 MiB, 개별 30 MiB, 전체 해제 60 MiB, 파일 100개, 노드 30만, 텍스트 800만자, 발췌 600자, 보정 2,048회. XBRL: ZIP 30 MiB, 멤버 20 MiB, 전체 60 MiB, 파일 100개, 노드 30만, 깊이 128. 두 파서의 멤버 한도를 혼동하지 않습니다.

## 11. Ollama·업종 관점

AI는 버튼으로 /api/chat을 호출하며 결정적 계산을 바꾸지 않습니다. 제공된 지표·주석 ID와 업종 관점 ID를 고르고 앱이 검증 수치와 정적 배경·질문을 조합합니다. 무제한 자유 서술형 기업 분석은 아닙니다.

형식 버전 7, 기본 모델 qwen3.5:4b, timeout 180초입니다. JSON 스키마·참조를 검사하고 근거를 벗어난 항목을 제외하거나 실패 안내를 제공합니다.

전용 관점: 금융/지주, 반도체/전자, 자동차, 유통, 운송/물류, 화학, 금속, 식음료, 수주 산업, 정보서비스. 코드 미대응은 일반 관점입니다. **HD현대일렉트릭의 코드 281 전용 관점은 현재 없습니다.**

commentary_fingerprint()는 Dataset JSON의 SHA-256입니다. commentary_matches()가 메모 버전·자료 식별값·기간을 확인합니다. 자료 연결 검사이지 모델 재현성이나 회계 정확성의 전자서명이 아닙니다. 재수집·가져오기 후에는 메모를 다시 생성할 수 있습니다.

## 12. RSS

연합인포맥스 공식 IB/기업·정책/금융·채권/외환의 최근 7일 피드 제공분을 수집합니다. 회사·업종·거시 키워드로 최대 12건을 고릅니다. URL·날짜·중복과 피드당 2 MiB를 검사하며 UI 캐시는 5분입니다.

모델은 기사 ID와 공급된 문장 번호만 선택합니다. 기사별 가능한 번호를 스키마로 제한하고 3~5건(공급량이 적으면 가용 수)을 표시합니다. 수집/발행 시각·원문·관련성을 구별합니다. 7일 전체 검색이나 실적 원인의 확정이 아닙니다.

뉴스는 일반 보고서 내보내기에 자동 병합되지 않습니다. 제출본 recent-news.html/JSON은 별도 검증 스냅샷입니다.

## 13. 내보내기

HTML/Excel/Markdown은 범위, 지표·제한·산식, 표준/전체 비교, 대조 입력, 주석·출처, 조건부 AI 메모와 문장별 참조 근거를 포함합니다. UI downloads()가 세션 메모를 analysis.ai_commentary로 전달합니다. CLI에는 AI 생성 옵션이 없고 제출 검증 스크립트가 별도로 호출했습니다.

Excel 금액은 정밀도 보존 문자열이며 수식 실행을 차단합니다. HTML은 이스케이프와 DART HTTPS 링크 제한을 적용합니다. Dataset JSON과 계산 결과 JSON은 구분합니다. 긴 원천 상세는 보고서를 크게 만들고 Excel 셀 길이 제한을 받을 수 있습니다.

## 14. 검증·제출 계약

가상 불일치·결측 보존·XBRL 보안/범위/정밀도·계정 비교·요약·UI·내보내기 등 251개 테스트를 통과했습니다. 최종 로그는 validation/pytest-final.txt, 251 passed in 69.68s입니다.

최종 실제 검증 5개 기업·27개 유효 기간의 대조 161건은 122개 일치·2개 불일치·34개 자료 부족·3개 기준 불일치입니다. 이전 단계의 표본을 합쳐 이 수치를 부풀리지 않습니다. 누적 17개 기업의 근거 수준은 등록부에 있습니다.

HD현대일렉트릭 실제 UI에서 검색·6개 기간 선택·AI·다운로드·RSS를 확인했습니다. 별도 복사본의 런처 최초 설치도 확인했고 브라우저 자동 열기는 생략했습니다. HTML은 내장 브라우저 AI 섹션을 확인했으며 전 화면·전 해상도·인쇄 전수 시각 검수는 하지 않았습니다.

ZIP은 앱·공개 보고서·원천 JSON·재현 스크립트·로그·해시를 포함하며 인증키/.env/.venv/캐시는 제외합니다. 문서 개정본은 원래 ZIP과 구분하고 코드가 변경되지 않았음을 표시합니다.

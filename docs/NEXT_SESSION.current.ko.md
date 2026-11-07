# 후속 개발 인수인계

기준일 2026-11-07. 통합 문서 개정 v2. 현재 코드와 최종 제출 코드의 차이는 문서뿐입니다.

## 1. 작업 위치와 우선 읽기

- 앱 루트: C:\Users\jongh\Downloads\dart-analyst-ui\dart-analyst
- 채팅/제출 작업 폴더: C:\Users\jongh\Documents\Codex\2026-11-06\c-users-jongh-downloads-dart-analyst
- 현재 명세: DEVELOPMENT_SPEC.ko.md
- 다음 작업과 완료 조건: IMPROVEMENTS.ko.md
- 문제별 진단/조치: DEBUGGING_HISTORY.ko.md
- 기업별 근거 수준: VERIFIED_COMPANIES.ko.md와 JSON
- 기존 검증 이력: VERIFICATION.md. 최초 161/230/248/250 등의 수치는 과거 시점입니다.
- 통합 이전 명세/인수인계는 docs/archive에 보존했습니다.

확인 당시 앱 폴더에 Git 저장소는 없었습니다. 다른 환경에서는 다시 확인하세요. .env 값을 로그·보고서·도구 출력에 넣지 않습니다.

## 2. 현재 확인된 결과

최종 전체 테스트 251 passed in 69.68s. 주요 모듈 타입 검사 통과. Windows/Python3.14.4의 별도 복사본에서 원클릭 최초 가상환경 생성·의존성 설치·Ollama 확인·앱 시작까지 수행했습니다.

최종 실제 표본은 HD현대일렉트릭, 삼성전자, 기업은행, 이마트, CJ제일제당의 5개 기업·27개 유효 기간입니다. 회계 대조 161건 중 122개 일치·2개 불일치·34개 자료 부족·3개 기준 불일치입니다.

대표 HD현대일렉트릭 실제 UI의 의도적 오류 검출·검색/수집·6개 기간 전환·Ollama 메모·HTML/Excel 다운로드·RSS 로드/모델 선정을 확인했습니다. 로컬 모델은 qwen3.5:4b입니다.

누적 등록은 17개 기업이지만 A 5개/B 5개/C 7개의 증거 수준이 다릅니다. 상세는 등록부를 따릅니다. B의 원래 7개·40개 기간 집계에는 A 일부가 중복됩니다.

## 3. 가장 먼저 할 개발

1. CJ제일제당 20260814001793의 현금 조정 -4,308,982,000원의 계산·표시 관계를 입증합니다. 두 현금 식에 같은 차이가 남습니다. 이름만으로 표준 ID의 의미를 바꾸거나 차액을 조정 Fact로 만들지 마세요.
2. SCE 전체 차원·구성·누적 기간을 모델링합니다. HD현대일렉트릭은 자본 대조 6건이 남습니다. 이마트/기아의 제한된 소유주 합계 대조는 상세 자본 완성을 의미하지 않습니다.
3. 코드 281 전력기기 전용 관점을 추가합니다. 현재 HD현대일렉트릭 AI는 일반 관점을 사용합니다. 은행/보험 전용 계정·지표도 별도 설계가 필요합니다.
4. 원본 없음·금액 충돌·기간 불명·파싱 실패를 구조화하고 승인형 매핑/fixture를 늘립니다.

외부 원본 공백은 이마트2023, 현대글로비스2024, 기업은행2021/2022 등이 확인됐습니다. 최종 공시 원본이 없다는 사실을 옛 자료로 덮지 않습니다.

## 4. 회귀 시 주의할 구현

- _apply_xbrl(): 회사/스킴·기간·범위·추가 차원·KRW, 정밀도 교차 검증.
- 소유주 합계와 매각예정 현금은 XSD 실제 ID/한글 라벨에서 승인된 범위만 매핑합니다. 구형 lab_*-ko_YYYY-MM-DD.xml도 읽습니다.
- CF 순증감 태그가 BeforeEffect여도 실제 값은 FX 포함일 수 있습니다. NAVER의 독립 구성합 검증을 유지하세요.
- 문단의 꺾쇠/앰퍼샌드 및 TE/TD/TH ENG 따옴표는 제한 보정 후 엄격 파싱합니다. 일반 손상 태그·DTD·엔티티는 거부합니다.
- document.xml 개별 30MiB와 XBRL 멤버 20MiB는 별개입니다. 은행의 21,282,590바이트 원문 때문에 전자만 확장했습니다.
- AI 메모는 narrative.commentary_fingerprint()/commentary_matches()로 Dataset/버전/기간에 연결합니다. downloads()가 analysis.ai_commentary를 전달합니다. Dataset JSON에는 메모가 저장되지 않습니다.
- 최근 뉴스는 피드 최근 제공분이며 일반 금융 보고서에 자동 통합되지 않습니다. 제출본 뉴스 HTML은 검증 스냅샷입니다.
- 런처는 기본 포트 8501, 검증은 8773/8774를 사용했습니다. 사용자 기존 세션을 끊거나 초기화하지 마세요.

## 5. 재현

앱 폴더에서 전체 회귀:

    $env:PYTHON_DOTENV_DISABLED='1'
    .\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider

위 변수는 테스트 셸에만 적용합니다. 실제 공시/앱은 별도 셸에서 dotenv를 정상 사용하세요.

런처 경로 확인과 별도 앱 시작:

    cmd.exe /d /c "DART_Analyst_Start.cmd -CheckOnly"
    cmd.exe /d /c "DART_Analyst_Start.cmd -NoBrowser -Port 8774"

UI agent API 검증은 별도 8773 서버에 --server.enableAgentApi=true를 주고 해당 서버의 /_stcore/agent/openapi.json을 먼저 읽습니다. 검증 세션의 인증키 입력값이 포함된 전체 트리를 출력하지 마세요.

제출 패키지 validation/verify_e2e.py와 verify_ui.py는 실공시·로컬 모델을 호출합니다. 기본 회귀/CI에서는 호출하지 않으며 회사/원본의 가용성은 재실행 시 바뀔 수 있습니다.

## 6. 제출물 관리

원래 ZIP: final-delivery/DART_Analyst_Submission_20261107.zip. 문서 개정본은 이름에 docs_v2를 붙여 구분합니다. 원래 ZIP을 덮어쓰지 않습니다. ZIP에는 .env/인증키/.venv/캐시를 넣지 않고 코드 일치·해시·링크·무결성을 확인합니다.

이번 문서 개정에서는 추가 기업 호출·모델 호출·계산 코드 변경을 하지 않았습니다. 기존 251개 통과 로그를 재사용한 것이며 문서 개정을 새 기능 검증으로 표현하지 않습니다.

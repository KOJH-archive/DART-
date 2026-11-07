# 저장소 개요

## 기본 정보

- 저장소 이름: `dart-financial-analyst`
- 제품명: DART 기업분석실
- 목적: OpenDART 공시를 수집하고, 과거 기간별 재무 계정·현금흐름·비율·근거를 함께 검토하는 로컬 Streamlit 분석 도구
- 실행 방식: Windows 원클릭 실행(`DART_Analyst_Start.cmd`) 또는 PowerShell/쉘 런처
- AI 방식: 로컬 Ollama 기반 메모 및 업종 검토
- 외부 전송: DART 조회와 RSS 수집을 제외한 AI 분석은 로컬 Ollama에서 수행
- 기준일: 2026-11-07 제출 검증본

## 저장소에 포함된 핵심 구성

| 영역 | 주요 파일/폴더 | 역할 |
|---|---|---|
| 앱 진입점 | `app.py` | Streamlit 화면, 기업 검색, 기간 선택, 보고서 다운로드 |
| 분석 엔진 | `dart_analyst/` | 수집, 정규화, XBRL/원문 보강, 계산, 검증, AI, RSS, 내보내기 |
| 실행 | `DART_Analyst_Start.cmd`, `run_windows.ps1`, `run.sh` | 환경 준비, 의존성 확인, Ollama/Streamlit 실행 |
| 테스트 | `tests/` | 단위·회귀·계약·내보내기·API 오류 테스트 |
| 문서 | `DEVELOPMENT_SPEC.ko.md`, `IMPROVEMENTS.ko.md`, `DEBUGGING_HISTORY.ko.md`, `NEXT_SESSION.ko.md` | 현재 명세, 잔여 개선, 디버깅 근거, 후속 작업 |
| 검증 기록 | `VERIFIED_COMPANIES.ko.md`, `VERIFIED_COMPANIES.json`, `VERIFICATION.md` | 기업별 증거 수준, 실행 결과, 미완료 대조 |
| 결과 예시 | `reports/` | 기업별 HTML/Markdown/Excel/JSON 예시 및 검증 산출물 |

## 현재 품질 기준

- 최종 코드 회귀 테스트: 251개 통과
- 실공시 최종 검증: 5개 기업, 27개 기간, 161개 대조
- 결과: 통과 122, 실패 2, 불완료 34, 비교불가 3
- 최종 검증 기업: HD현대일렉트릭, 삼성전자, 기업은행, 이마트, CJ제일제당
- 전체 문서화 검증 기업: 17개(증거 수준 A 5개, B 5개, C 7개)
- 지원 원칙: 업종 제한 없이 조회하되, 계정·기간·원문 근거가 부족하면 `불완료` 또는 `비교불가`로 표시

## 중요한 한계

1. 현금흐름표의 특정 계정은 원문 표의 의미·계산 링크까지 확인되지 않으면 자동 대체하지 않습니다.
2. 자본변동표 전체 차원(dimension) 롤포워드와 업종별 금융 규제비율은 아직 제한적입니다.
3. HD현대일렉트릭은 전기장비 전용 업종 렌즈가 없어 일반 업종 렌즈를 사용합니다.
4. AI 메모는 현재 보고서에는 포함되지만 Dataset JSON에는 저장하지 않으며, CLI에서 AI 생성 옵션을 직접 제공하지 않습니다.
5. RSS 뉴스는 별도 스냅샷으로 제공되며 표준 재무 보고서 번들에 자동 병합하지 않습니다.

## 후속 개발 우선순위

- P0: 현금흐름 계산·표시 링크베이스와 분류 오류의 의미 검증
- P0: 자본변동표 누적/차원별 브리지 구현
- P0: 원문 누락·충돌을 구조화하고 대체 공식 원천을 명시적으로 연결
- P1: 전기장비 업종 렌즈, 금융업 전용 계정·비율, 승인된 매핑 버전 관리
- P1: AI 메모·RSS·재무 데이터의 재현 가능한 보고서 번들 저장
- P1: 의존성 완전 잠금, 런처 설정 일관성, CI/릴리스 체크 자동화

## 재현 절차

```powershell
cd C:\Users\jongh\Downloads\dart-analyst-ui\dart-analyst
.\DART_Analyst_Start.cmd
```

검증 환경은 Windows, Python 3.14.4, Ollama 로컬 모델을 기준으로 합니다. 인증키·`.env`·가상환경은 저장소에 커밋하지 않습니다.


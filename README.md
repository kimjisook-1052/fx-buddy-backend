# fx-buddy

원/달러 환율 데이터를 기반으로 질문에 답변하는 AI 챗봇 서비스입니다. "AI Agent 개발: 나만의 AI 비서 구축" 미션의 결과물로, 시계열 데이터를 분석하고 그 결과를 AI 답변에 반영하는 흐름을 구현했습니다.

## 서비스 소개

일반적인 AI 챗봇은 개인의 데이터를 알지 못해 원론적인 답변만 제공합니다. fx-buddy는 한국은행에서 제공하는 원/달러 환율 데이터를 데이터베이스에 저장해두고, 사용자가 "지금 환율 어때?", "송금하기 좋은 시점이야?"와 같은 질문을 하면 저장된 데이터의 요약 정보를 바탕으로 답변합니다. 딸이 미국에서 유학 중이라 환율 변동에 관심이 많다는 개인적인 필요에서 출발한 프로젝트입니다.

## 기술 스택

- **백엔드**: FastAPI (Python)
- **데이터베이스**: Google Firestore
- **AI 모델**: Google Gemini API (gemini-3.6-flash) — 비용 절감을 위해 미션 권장 사양인 OpenAI GPT API 대신 사용
- **배포**: Render (백엔드, Free 요금제)
- **프론트엔드**: HTML/CSS/JavaScript (프레임워크 미사용)
- **데이터 출처**: 한국은행 ECOS API (원/달러 환율, 3.1.1.3 원화의 대미달러), 2023년 1월~현재, 총 895개 데이터

## 배포 주소

| 항목 | 주소 |
|---|---|
| 백엔드 API | https://fx-buddy-backend.onrender.com |
| Swagger UI | https://fx-buddy-backend.onrender.com/docs |
| 프론트엔드 | https://fx-buddy-frontend.vercel.app |

> 참고: Render 무료 요금제는 일정 시간 요청이 없으면 서버가 슬립 상태가 되어, 첫 요청 시 응답까지 최대 50초 정도 걸릴 수 있습니다.

## 프로젝트 구조

저장소는 용도별로 분리되어 있습니다.

- `fx-buddy-upload`: 환율 데이터를 Firestore에 업로드하는 스크립트
- `fx-buddy-backend`: FastAPI 백엔드 서버 코드
- `fx-buddy-frontend`: 정적 프론트엔드 (index.html, app.js, config.js, style.css)

## 로컬 실행 방법

### 백엔드

```
git clone https://github.com/kimjisook-1052/fx-buddy-backend.git
cd fx-buddy-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

프로젝트 루트에 `.env` 파일을 만들고 아래 환경 변수를 채운 뒤 실행합니다.

```
uvicorn main:app --reload
```

실행 후 `http://127.0.0.1:8000/docs`에서 Swagger UI를 확인할 수 있습니다.

### 프론트엔드

`fx-buddy-frontend` 폴더의 `config.js`에서 `API_BASE_URL`을 백엔드 주소로 지정한 뒤, `index.html`을 브라우저로 열면 됩니다.

## 환경 변수 목록

| 변수명 | 설명 |
|---|---|
| `FIREBASE_SERVICE_ACCOUNT_JSON` | Firebase 서비스 계정 키 (JSON 문자열 또는 파일 경로) |
| `GOOGLE_API_KEY` | Gemini API 키 |
| `ALLOWED_ORIGINS` | CORS 허용 도메인 목록 |

## 주요 기능

- **데이터 기반 AI 채팅**: 저장된 환율 데이터 요약을 시스템 프롬프트에 주입하여 답변 생성
- **데이터 관리(CRUD)**: 환율 데이터 추가/조회/수정/삭제
- **대화 기록 저장 및 불러오기**: 대화 저장, 목록 조회, 특정 대화 다시 불러오기
- **배포 및 문서화**: Render 배포, Swagger UI로 API 문서 제공

## 진행 과정

### 1. 데이터 준비
한국은행 ECOS에서 API 키를 발급받아 원/달러 환율 데이터를 CSV로 다운로드하고, Firestore에 업로드했습니다.

### 2. 백엔드 개발
FastAPI로 라우터(data, conversations, chat)와 서비스(firestore_service, gemini_service)를 분리해 구성했습니다. 로컬 환경에서 개발 및 테스트를 완료한 후 Render에 배포했습니다.

### 3. 배포 트러블슈팅
배포 과정에서 다음 문제들을 순차적으로 발견하고 해결했습니다.

- CORS 설정 코드에 오타(`allow_credentials=F`)가 있어 서버가 정상적으로 실행되지 않았습니다. `False`로 수정했습니다.
- Windows PowerShell로 파일을 편집하는 과정에서 한글 주석 부분의 인코딩이 깨졌습니다. UTF-8로 다시 저장해 복구했습니다.
- 코드 수정 중 함수 본문의 들여쓰기가 누락되어 IndentationError가 발생했습니다. 들여쓰기를 맞춰 해결했습니다.

세 가지 문제를 모두 해결한 뒤 백엔드 배포에 성공했고, 루트 엔드포인트(`/`)가 정상적으로 응답하는 것을 확인했습니다.

### 4. 프론트엔드 연동 확인
프론트엔드에서 백엔드 API로 요청을 보내는 과정을 점검했습니다. 브라우저 개발자 도구의 Network 탭으로 확인한 결과, CORS 설정과 서버 통신 자체는 정상적으로 이루어졌습니다.

## 현재 상태

백엔드는 Render에 정상 배포되어 있으며(Live 상태), 프론트엔드와의 통신도 정상적으로 이루어집니다. 다만 테스트 과정에서 Gemini API의 무료 요금제 일일 요청 한도(gemini-3.6-flash 모델 기준 하루 20회)를 초과하여, 챗봇 응답 기능은 할당량이 초기화된 이후 정상 작동을 재확인할 예정입니다.

## 제출 스크린샷

- 데이터 요약이 보이는 채팅 화면 (질문+답변 포함) — 추가 예정
- 데이터 관리 화면 (CRUD 중 1개 동작) — 추가 예정
- 대화 기록 화면 (불러오기 동작) — 추가 예정

## 향후 개선 사항

- Gemini API 할당량 관리 방안 검토 (API 키 교체 또는 유료 전환)
- 서비스 안정성을 위한 에러 핸들링 보강
- 제출용 스크린샷 첨부

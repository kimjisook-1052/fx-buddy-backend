# fx-buddy

원/달러 환율 데이터를 기반으로 질문에 답변하는 AI 챗봇 서비스입니다. "AI Agent 개발: 나만의 AI 비서 구축" 미션의 결과물로, 시계열 데이터를 분석하고 그 결과를 AI 답변에 반영하는 흐름(데이터 요약 → 시스템 프롬프트 주입 → AI 응답)을 구현했습니다.

## 서비스 소개

일반적인 AI 챗봇은 개인의 데이터를 알지 못해 원론적인 답변만 제공합니다. fx-buddy는 한국은행에서 제공하는 원/달러 환율 데이터를 데이터베이스에 저장해두고, 사용자가 "지금 환율 어때?", "송금하기 좋은 시점이야?"와 같은 질문을 하면 저장된 데이터의 요약 정보(기간, 개수, 평균/최대/최소, 최근 추세)를 바탕으로 맞춤형 답변을 제공합니다.

해외에 유학 중인 학생이나 그 가족처럼, 환율 변동에 민감할 수밖에 없는 사람들을 위한 실용적인 필요에서 출발한 프로젝트입니다.

## 배포 주소

| 항목 | 주소 |
|---|---|
| 프론트엔드 | https://fx-buddy-frontend.vercel.app |
| 백엔드 API | https://fx-buddy-backend.onrender.com |
| Swagger UI | https://fx-buddy-backend.onrender.com/docs |

> 참고: Render 무료 요금제는 일정 시간 요청이 없으면 서버가 슬립 상태가 되어, 첫 요청 시 응답까지 최대 50초 정도 걸릴 수 있습니다.

## 기술 스택

| 구분 | 사용 기술 |
|---|---|
| 백엔드 | FastAPI (Python) |
| 데이터베이스 | Google Firestore |
| AI 모델 | Google Gemini API (gemini-3.6-flash) |
| 프론트엔드 | HTML / CSS / JavaScript (프레임워크 미사용) |
| 백엔드 배포 | Render (Free 요금제) |
| 프론트엔드 배포 | Vercel |
| 데이터 출처 | 한국은행 ECOS API (3.1.1.3 원화의 대미달러), 2023년 1월 ~ 현재, 총 895개 |

> 미션 권장 사양은 OpenAI GPT API였으나, 비용 절감을 위해 무료로 사용 가능한 Google Gemini API로 대체했습니다. 이에 따라 환경 변수도 `OPENAI_API_KEY` 대신 `GOOGLE_API_KEY`를 사용합니다.

## 주요 기능

- **데이터 기반 AI 채팅**: 저장된 환율 데이터 요약을 시스템 프롬프트에 주입하여 맞춤형 답변 생성
- **데이터 관리 (CRUD)**: 환율 데이터 추가 / 조회 / 수정 / 삭제
- **대화 기록 저장 및 불러오기**: 대화 저장, 목록 조회, 특정 대화 다시 불러오기
- **배포 및 문서화**: Render / Vercel 배포, Swagger UI로 API 문서 제공

## API 엔드포인트

### 데이터 API

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/api/data` | 새 데이터 추가 |
| GET | `/api/data` | 데이터 목록 조회 |
| PUT | `/api/data/{id}` | 데이터 수정 |
| DELETE | `/api/data/{id}` | 데이터 삭제 |
| GET | `/api/data/summary` | 데이터 요약 (프롬프트 주입용) |

### 대화 기록 API

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/api/conversations` | 대화 저장 |
| GET | `/api/conversations` | 대화 목록 조회 |
| GET | `/api/conversations/{id}` | 특정 대화의 전체 메시지 조회 |
| DELETE | `/api/conversations/{id}` | 대화 삭제 |

### 챗봇 API

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/api/chat` | 데이터 요약 조회 → 시스템 프롬프트 주입 → Gemini API 호출 → 대화 자동 저장 |

전체 명세는 배포된 [Swagger UI](https://fx-buddy-backend.onrender.com/docs)에서 확인할 수 있습니다.

## 프로젝트 구조

용도별로 세 개의 저장소로 분리했습니다.

- `fx-buddy-upload`: 환율 데이터를 Firestore에 업로드하는 스크립트
- `fx-buddy-backend`: FastAPI 백엔드 서버 코드 (routers: data, conversations, chat / services: firestore_service, gemini_service)
- `fx-buddy-frontend`: 정적 프론트엔드 (index.html, app.js, config.js, style.css)

## 로컬 실행 방법

### 백엔드

```bash
git clone https://github.com/kimjisook-1052/fx-buddy-backend.git
cd fx-buddy-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

프로젝트 루트에 `.env` 파일을 만들고 아래 환경 변수를 채운 뒤 실행합니다.

```bash
uvicorn main:app --reload
```

실행 후 http://127.0.0.1:8000/docs 에서 Swagger UI를 확인할 수 있습니다.

### 프론트엔드

`fx-buddy-frontend` 폴더의 `config.js`에서 `API_BASE_URL`을 백엔드 주소로 지정한 뒤, `index.html`을 브라우저로 열면 됩니다.

## 환경 변수 목록

| 변수명 | 설명 |
|---|---|
| `FIREBASE_SERVICE_ACCOUNT_JSON` | Firebase 서비스 계정 키 (JSON 문자열 또는 파일 경로) |
| `GOOGLE_API_KEY` | Gemini API 키 |
| `ALLOWED_ORIGINS` | CORS 허용 도메인 목록 |

## 진행 과정 및 트러블슈팅

**1. 데이터 준비**
한국은행 ECOS에서 API 키를 발급받아 원/달러 환율 데이터를 CSV로 다운로드하고, Firestore에 업로드했습니다.

**2. 백엔드 개발**
FastAPI로 라우터(data, conversations, chat)와 서비스(firestore_service, gemini_service)를 분리해 구성했습니다. 로컬 환경에서 개발 및 테스트를 완료한 후 Render에 배포했습니다.

**3. 배포 트러블슈팅**

배포 및 운영 과정에서 다음 문제들을 순차적으로 발견하고 해결했습니다.

- CORS 설정 코드에 오타(`allow_credentials=F`)가 있어 서버가 정상적으로 실행되지 않았던 문제를 `False`로 수정하여 해결
- Windows PowerShell로 파일을 편집하는 과정에서 깨진 한글 주석 인코딩을 UTF-8로 다시 저장해 복구
- 함수 본문의 들여쓰기 누락으로 발생한 `IndentationError` 해결
- Gemini API 패키지를 지원 종료된 `google-generativeai`에서 `google-genai`로 교체
- 채팅 요청 시 발생한 `CORS policy` 에러의 근본 원인을 분석한 결과, 실제로는 CORS 설정 문제가 아니라 Gemini API 호출 실패(일시적 과부하로 인한 503 오류) 시 예외 처리가 없어 서버 응답이 비정상 종료되며 CORS 헤더가 누락된 것이 원인이었음을 확인. `/api/chat` 라우터에 예외 처리(try/except)를 추가해, Gemini API 오류 발생 시에도 정상적인 오류 응답(CORS 헤더 포함)을 반환하도록 수정하여 해결

**4. 최종 통신 확인**
브라우저 개발자 도구의 Network 탭과 Render 서버 로그를 함께 확인하여, CORS 사전 요청(OPTIONS)과 실제 요청(POST) 모두 정상 응답하는 것을 확인했습니다.

## 현재 상태

백엔드는 Render에, 프론트엔드는 Vercel에 정상 배포되어 있으며(모두 Live 상태), 두 서비스 간 통신과 데이터 기반 AI 채팅, 데이터 관리(CRUD), 대화 기록 저장/불러오기 기능 모두 정상 작동을 확인했습니다.

## 제출 스크린샷

**데이터 요약이 보이는 채팅 화면 (질문 + 답변)**

<img width="1909" height="1070" alt="chat-with-summary" src="https://github.com/user-attachments/assets/9e41b184-5b87-4768-aae8-07710a18fa1a" />




**데이터 관리 화면 (데이터 추가 동작)**

<img width="1915" height="1076" alt="data-management" src="https://github.com/user-attachments/assets/fd19d321-9b4d-479b-98dc-63dcc20aa7cf" />




**대화 기록 화면 (불러오기 동작)**

<img width="1916" height="1072" alt="conversation-history" src="https://github.com/user-attachments/assets/337d31af-e982-464d-b6cb-3bdde0717bf5" />



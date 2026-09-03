import os

import firebase_admin
from firebase_admin import credentials
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routers import data, conversations, chat

# --- Firebase 초기화 ---
import json

firebase_config = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "serviceAccountKey.json")

if firebase_config.strip().startswith("{"):
# 배포 환경(Render): 환경변수에 JSON 문자열이 있는 경우
    cred_dict = json.loads(firebase_config)
    cred = credentials.Certificate(cred_dict)
else:
# 로컬 환경: 환경변수에 파일 경로가 있는 경우
        cred = credentials.Certificate(firebase_config)

firebase_admin.initialize_app(cred)

# --- FastAPI 앱 생성 ---
app = FastAPI(
    title="fx-buddy API",
    description="원/달러 환율 데이터를 기반으로 답변하는 AI 비서 API",
    version="1.0.0",
)

# --- CORS 설정 ---
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 라우터 등록 ---
app.include_router(data.router, prefix="/api/data", tags=["data"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["conversations"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])


@app.get("/")
def root():
    
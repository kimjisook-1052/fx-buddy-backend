import os

import firebase_admin
from firebase_admin import credentials
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routers import data, conversations, chat

# --- Firebase ì´ˆê¸°??---
import json

firebase_config = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "serviceAccountKey.json")

if firebase_config.strip().startswith("{"):
    # ë°°í¬ ?˜ê²½(Render): ?˜ê²½ë³€?˜ì— JSON ?´ìš© ?ì²´ê°€ ?¤ì–´?ˆëŠ” ê²½ìš°
    cred_dict = json.loads(firebase_config)
    cred = credentials.Certificate(cred_dict)
else:
    # ë¡œì»¬ ?˜ê²½: ?˜ê²½ë³€?˜ì— ?Œì¼ ê²½ë¡œê°€ ?¤ì–´?ˆëŠ” ê²½ìš°
    cred = credentials.Certificate(firebase_config)

firebase_admin.initialize_app(cred)

# --- FastAPI ???ì„± ---
app = FastAPI(
    title="fx-buddy API",
    description="???¬ëŸ¬ ?˜ìœ¨ ?°ì´?°ë? ê¸°ë°˜?¼ë¡œ ?µë??˜ëŠ” AI ë¹„ì„œ API",
    version="1.0.0",
)

# --- CORS ?¤ì • ---
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ?¼ìš°???±ë¡ ---
app.include_router(data.router, prefix="/api/data", tags=["data"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["conversations"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])


@app.get("/")
def root():
    return {"message": "fx-buddy APIê°€ ?•ìƒ?ìœ¼ë¡??¤í–‰ ì¤‘ì…?ˆë‹¤.", "docs": "/docs"}

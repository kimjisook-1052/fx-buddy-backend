from pydantic import BaseModel
from typing import Optional, List


# --- 환율 데이터 ---
class DataItemCreate(BaseModel):
    date: str
    value: float
    memo: Optional[str] = ""


class DataItemUpdate(BaseModel):
    date: Optional[str] = None
    value: Optional[float] = None
    memo: Optional[str] = None


class DataItemOut(BaseModel):
    id: str
    date: str
    value: float
    memo: Optional[str] = ""


# --- 대화 기록 ---
class Message(BaseModel):
    role: str  # "user" 또는 "assistant"
    content: str


class ConversationCreate(BaseModel):
    title: Optional[str] = "새 대화"
    messages: List[Message] = []


class ConversationOut(BaseModel):
    id: str
    title: str
    messages: List[Message]


# --- 채팅 ---
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

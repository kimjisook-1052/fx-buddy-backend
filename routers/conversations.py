from fastapi import APIRouter, HTTPException
from typing import List
from firebase_admin import firestore

from services.firestore_service import get_db
from models import ConversationCreate, ConversationOut

router = APIRouter()


@router.post("", response_model=ConversationOut)
def create_conversation(conv: ConversationCreate):
    """대화 저장 (수동 저장용, 보통은 /api/chat 에서 자동 저장됨)"""
    db = get_db()
    doc_ref = db.collection("conversations").document()
    data = conv.dict()
    data["created_at"] = firestore.SERVER_TIMESTAMP
    doc_ref.set(data)
    return ConversationOut(id=doc_ref.id, title=conv.title, messages=conv.messages)


@router.get("", response_model=List[ConversationOut])
def list_conversations():
    """대화 목록 조회 (최신순)"""
    db = get_db()
    docs = db.collection("conversations").order_by(
        "created_at", direction=firestore.Query.DESCENDING
    ).stream()
    result = []
    for d in docs:
        data = d.to_dict()
        result.append(ConversationOut(
            id=d.id,
            title=data.get("title", "제목 없음"),
            messages=data.get("messages", []),
        ))
    return result


@router.get("/{conv_id}", response_model=ConversationOut)
def get_conversation(conv_id: str):
    """특정 대화의 전체 메시지 조회 (대화 불러오기)"""
    db = get_db()
    doc = db.collection("conversations").document(conv_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다.")
    data = doc.to_dict()
    return ConversationOut(
        id=doc.id,
        title=data.get("title", "제목 없음"),
        messages=data.get("messages", []),
    )


@router.delete("/{conv_id}")
def delete_conversation(conv_id: str):
    """대화 삭제"""
    db = get_db()
    doc_ref = db.collection("conversations").document(conv_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="대화를 찾을 수 없습니다.")
    doc_ref.delete()
    return {"message": "삭제되었습니다.", "id": conv_id}

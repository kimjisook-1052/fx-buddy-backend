from fastapi import APIRouter
from firebase_admin import firestore

from services.firestore_service import get_db
from services.gemini_service import ask_gemini
from models import ChatRequest
from routers.data import get_summary

router = APIRouter()


@router.post("")
def chat(req: ChatRequest):
    """
    동작 흐름:
    1. 데이터 요약 조회 (/api/data/summary 로직 재사용)
    2. 요약을 시스템 프롬프트에 삽입
    3. GPT API 호출
    4. 대화 내용을 conversations에 자동 저장
    """
    db = get_db()

    # 1. 데이터 요약 조회
    summary = get_summary()

    # 2. 시스템 프롬프트에 요약 삽입 (컨텍스트 주입)
    system_prompt = f"""당신은 원/달러 환율 데이터 분석 비서입니다.

[사용자 데이터 요약]
- 데이터 기간: {summary['period']}
- 총 레코드: {summary['count']}개
- 평균 환율: {summary['metrics']['average']}원
- 최고 환율: {summary['metrics']['max']}원
- 최저 환율: {summary['metrics']['min']}원
- 최근 트렌드: {summary['trend']}

위 데이터를 기반으로 사용자의 질문에 맞춤형으로 답변하세요.
사용자는 미국에 유학 중인 자녀에게 정기적으로 학비를 송금하고 있어서,
지금이 송금하기 유리한 시점인지 궁금해합니다. 데이터 근거를 들어 답변하세요."""

    # 기존 대화 이어가기 (conversation_id가 있으면)
    messages_history = []
    conv_ref = None
    if req.conversation_id:
        conv_ref = db.collection("conversations").document(req.conversation_id)
        conv_doc = conv_ref.get()
        if conv_doc.exists:
            messages_history = conv_doc.to_dict().get("messages", [])

    # 3. GPT 호출
    from fastapi import HTTPException

    try:
        ai_reply = ask_gemini(system_prompt, messages_history, req.message)
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail="AI 응답 생성 중 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
    )

    # 4. 대화 자동 저장
    new_messages = messages_history + [
        {"role": "user", "content": req.message},
        {"role": "assistant", "content": ai_reply},
    ]

    if conv_ref is not None:
        conv_ref.update({"messages": new_messages})
        conv_id = req.conversation_id
    else:
        conv_ref = db.collection("conversations").document()
        conv_ref.set({
            "title": req.message[:20],
            "messages": new_messages,
            "created_at": firestore.SERVER_TIMESTAMP,
        })
        conv_id = conv_ref.id

    return {
        "reply": ai_reply,
        "conversation_id": conv_id,
    }

from fastapi import APIRouter, HTTPException
from typing import List

from services.firestore_service import get_db
from models import DataItemCreate, DataItemUpdate, DataItemOut

router = APIRouter()


@router.post("", response_model=DataItemOut)
def create_data(item: DataItemCreate):
    """새 환율 데이터 추가"""
    db = get_db()
    doc_ref = db.collection("data").document()
    doc_ref.set(item.dict())
    return DataItemOut(id=doc_ref.id, **item.dict())


@router.get("", response_model=List[DataItemOut])
def list_data():
    """전체 환율 데이터 목록 조회 (날짜순)"""
    db = get_db()
    docs = db.collection("data").order_by("date").stream()
    result = []
    for d in docs:
        data = d.to_dict()
        result.append(DataItemOut(
            id=d.id,
            date=data.get("date", ""),
            value=data.get("value", 0),
            memo=data.get("memo", ""),
        ))
    return result


@router.put("/{item_id}", response_model=DataItemOut)
def update_data(item_id: str, item: DataItemUpdate):
    """특정 데이터 수정"""
    db = get_db()
    doc_ref = db.collection("data").document(item_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")

    update_fields = {k: v for k, v in item.dict().items() if v is not None}
    doc_ref.update(update_fields)

    updated = doc_ref.get().to_dict()
    return DataItemOut(
        id=item_id,
        date=updated.get("date", ""),
        value=updated.get("value", 0),
        memo=updated.get("memo", ""),
    )


@router.delete("/{item_id}")
def delete_data(item_id: str):
    """특정 데이터 삭제"""
    db = get_db()
    doc_ref = db.collection("data").document(item_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")
    doc_ref.delete()
    return {"message": "삭제되었습니다.", "id": item_id}


@router.get("/summary")
def get_summary():
    """데이터 요약(프롬프트 주입용) - 기간/개수/평균/최대/최소/추세"""
    db = get_db()
    docs = list(db.collection("data").order_by("date").stream())
    if not docs:
        raise HTTPException(status_code=404, detail="데이터가 없습니다.")

    values = [d.to_dict().get("value", 0) for d in docs]
    dates = [d.to_dict().get("date", "") for d in docs]

    count = len(values)
    average = round(sum(values) / count, 2)
    maximum = max(values)
    minimum = min(values)
    period = f"{dates[0]} ~ {dates[-1]}"

    # 최근 30일 평균 vs 그 이전 30일 평균으로 추세 판단
    window = 30
    if count >= window * 2:
        recent_avg = sum(values[-window:]) / window
        prev_avg = sum(values[-2 * window:-window]) / window
        diff = recent_avg - prev_avg
        if diff > 1:
            trend = f"상승 (최근 {window}일 평균이 이전 대비 {diff:+.1f}원)"
        elif diff < -1:
            trend = f"하락 (최근 {window}일 평균이 이전 대비 {diff:+.1f}원)"
        else:
            trend = "보합"
    else:
        trend = "데이터가 적어 추세 계산이 어렵습니다."

    return {
        "period": period,
        "count": count,
        "metrics": {
            "average": average,
            "max": maximum,
            "min": minimum,
        },
        "trend": trend,
    }

from firebase_admin import firestore


def get_db():
    """Firestore 클라이언트를 반환합니다. main.py에서 firebase_admin이 이미 초기화된 상태여야 해요."""
    return firestore.client()

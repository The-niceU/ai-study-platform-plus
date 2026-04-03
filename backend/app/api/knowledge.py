from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.document import Document
from app.models.knowledge_item import KnowledgeItem
from app.models.user import User
from app.services.knowledge_builder import build_knowledge_items_for_document
from app.schemas.knowledge import KnowledgeItemResponse, KnowledgeSearchRequest

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.post("/generate/{document_id}")
def generate_knowledge_items(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id, Document.user_id == current_user.id)
        .first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")

    db.query(KnowledgeItem).filter(KnowledgeItem.document_id == document_id).delete()
    db.commit()

    created_count = build_knowledge_items_for_document(document_id, current_user.id, db)

    return {
        "message": "知识点生成成功",
        "document_id": document_id,
        "created_count": created_count,
    }


@router.get("/", response_model=list[KnowledgeItemResponse])
def list_knowledge_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = (
        db.query(KnowledgeItem)
        .filter(KnowledgeItem.user_id == current_user.id)
        .order_by(KnowledgeItem.created_at.desc())
        .all()
    )
    return items

@router.post("/search", response_model=list[KnowledgeItemResponse])
def search_knowledge_items(
    data: KnowledgeSearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = data.query.strip()
    if not query:
        return []

    items = (
        db.query(KnowledgeItem)
        .filter(KnowledgeItem.user_id == current_user.id)
        .all()
    )

    query_lower = query.lower()

    scored_items = []
    for item in items:
        score = 0
        title = (item.title or "").lower()
        summary = (item.summary or "").lower()
        topic = (item.topic or "").lower()

        if query_lower in title:
            score += 3
        if query_lower in summary:
            score += 2
        if query_lower in topic:
            score += 1

        query_words = query_lower.split()
        for word in query_words:
            if word and word in title:
                score += 2
            if word and word in summary:
                score += 1

        if score > 0:
            scored_items.append((score, item))

    scored_items.sort(key=lambda x: x[0], reverse=True)

    return [item for _, item in scored_items[:20]]
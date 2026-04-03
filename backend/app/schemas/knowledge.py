from datetime import datetime
from pydantic import BaseModel


class KnowledgeItemResponse(BaseModel):
    id: int
    user_id: int
    document_id: int
    chunk_id: int
    title: str
    summary: str
    topic: str | None = None
    difficulty: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class KnowledgeSearchRequest(BaseModel):
    query: str
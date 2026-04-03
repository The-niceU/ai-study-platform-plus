from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_id = Column(Integer, ForeignKey("chunks.id"), nullable=False)

    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    topic = Column(String(100), nullable=True)
    difficulty = Column(String(50), nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User")
    document = relationship("Document")
    chunk = relationship("Chunk")
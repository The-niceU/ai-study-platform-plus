from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.services.embedding_service import encode_query, encode_texts
from app.services.vector_store import build_faiss_index, search_similar
from app.models.document import Document
from app.models.knowledge_item import KnowledgeItem

def rebuild_chunk_index(db: Session):
    chunks = db.query(Chunk).order_by(Chunk.id.asc()).all()
    if not chunks:
        return 0

    texts = [chunk.content for chunk in chunks]
    vectors = encode_texts(texts)

    metadata = []
    for chunk in chunks:
        document = db.query(Document).filter(Document.id == chunk.document_id).first()
        knowledge_item = (
            db.query(KnowledgeItem)
            .filter(KnowledgeItem.chunk_id == chunk.id)
            .first()
        )

        metadata.append(
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "file_name": document.file_name if document else "未知文件",
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "page_num": chunk.page_num,
                "knowledge_item_id": knowledge_item.id if knowledge_item else None,
                "knowledge_title": knowledge_item.title if knowledge_item else None,
                "knowledge_summary": knowledge_item.summary if knowledge_item else None,
                "topic": knowledge_item.topic if knowledge_item else None,
                "difficulty": knowledge_item.difficulty if knowledge_item else None,
            }
        )

    build_faiss_index(vectors, metadata)
    return len(chunks)


def retrieve_chunks(query: str, top_k: int = 5):
    query_vector = encode_query(query)
    return search_similar(query_vector, top_k=top_k)
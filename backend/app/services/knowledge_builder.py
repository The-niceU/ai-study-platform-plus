import json
from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.chunk import Chunk
from app.models.document import Document
from app.models.knowledge_item import KnowledgeItem

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)


def extract_knowledge_from_text(text: str):
    prompt = f"""
你是一个知识抽取助手。请从下面的课程资料片段中提取一个结构化知识点。

要求：
1. 返回 JSON 格式
2. 必须包含以下字段：
   - title: 知识点标题，简洁明确，不超过20字
   - summary: 知识点摘要，用1到3句话概括
   - topic: 所属主题，尽量简洁，例如 "Linear Algebra"、"Python"、"RAG"
   - difficulty: 难度，只能是 "basic"、"intermediate"、"advanced" 三者之一
3. 不要输出 JSON 以外的任何内容
4. 如果片段信息不足，也尽量给出合理概括

资料片段：
{text}
"""

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一个课程知识点结构化抽取助手，只能输出 JSON。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    try:
        result = json.loads(content)
        return {
            "title": result.get("title", "").strip(),
            "summary": result.get("summary", "").strip(),
            "topic": result.get("topic", "").strip(),
            "difficulty": result.get("difficulty", "basic").strip(),
        }
    except Exception:
        return {
            "title": text[:30].replace("\n", " ").strip() or "未命名知识点",
            "summary": text[:200].replace("\n", " ").strip(),
            "topic": "General",
            "difficulty": "basic",
        }


def build_knowledge_items_for_document(document_id: int, user_id: int, db: Session):
    chunks = (
        db.query(Chunk)
        .filter(Chunk.document_id == document_id)
        .order_by(Chunk.chunk_index.asc())
        .all()
    )

    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        return 0

    created_count = 0

    for chunk in chunks:
        text = chunk.content.strip()
        if not text:
            continue

        knowledge = extract_knowledge_from_text(text)

        title = knowledge["title"] or f"{document.file_name} - chunk {chunk.chunk_index}"
        summary = knowledge["summary"] or text[:200].replace("\n", " ").strip()
        topic = knowledge["topic"] or document.file_name
        difficulty = knowledge["difficulty"] or "basic"

        item = KnowledgeItem(
            user_id=user_id,
            document_id=document_id,
            chunk_id=chunk.id,
            title=title,
            summary=summary,
            topic=topic,
            difficulty=difficulty,
        )
        db.add(item)
        created_count += 1

    db.commit()
    return created_count
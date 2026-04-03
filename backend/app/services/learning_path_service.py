import json
from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.knowledge_item import KnowledgeItem

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)


def select_relevant_knowledge_items(topic: str, user_id: int, db: Session):
    items = (
        db.query(KnowledgeItem)
        .filter(KnowledgeItem.user_id == user_id)
        .all()
    )

    topic_lower = topic.strip().lower()

    matched_items = []
    for item in items:
        item_topic = (item.topic or "").lower()
        item_title = (item.title or "").lower()
        item_summary = (item.summary or "").lower()

        score = 0
        if topic_lower in item_topic:
            score += 3
        if topic_lower in item_title:
            score += 2
        if topic_lower in item_summary:
            score += 1

        if score > 0:
            matched_items.append((score, item))

    matched_items.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in matched_items[:6]]


def generate_learning_path_with_llm(topic: str, items: list[KnowledgeItem]):
    knowledge_text = []
    for idx, item in enumerate(items, start=1):
        knowledge_text.append(
            f"[知识点{idx}] id={item.id}\n"
            f"title={item.title}\n"
            f"summary={item.summary}\n"
            f"topic={item.topic}\n"
            f"difficulty={item.difficulty}\n"
        )

    joined_text = "\n".join(knowledge_text)

    prompt = f"""
你是一个学习路径规划助手。请基于给定知识点，为用户主题“{topic}”生成一个循序渐进的学习路径。

要求：
1. 返回 JSON
2. JSON 格式必须为：
{{
  "topic": "主题名",
  "steps": [
    {{
      "step": 1,
      "phase": "基础",
      "title": "步骤标题",
      "description": "这一阶段学习什么，为什么先学这个",
      "recommended_question": "这一阶段适合继续追问的一个问题",
      "suggested_action": "建议的学习动作，比如先阅读、再提问、再整理",
      "knowledge_item_id": 1
    }}
  ]
}}
3. step 从 1 开始递增
4. phase 尽量使用：基础 / 核心 / 应用 / 提升
5. 每一步尽量关联一个最合适的 knowledge_item_id
6. 不要输出 JSON 以外的任何内容
7. 路径应体现合理学习顺序，而不是简单重复原文

可用知识点如下：
{joined_text}
"""

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一个学习路径规划助手，只能输出 JSON。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()

    try:
        data = json.loads(content)
        return data
    except Exception:
        fallback_steps = []
        for idx, item in enumerate(items, start=1):
            fallback_steps.append(
                {
                    "step": idx,
                    "phase": "基础" if idx == 1 else "核心" if idx <= 3 else "应用",
                    "title": item.title,
                    "description": item.summary,
                    "recommended_question": f"这个知识点的核心概念是什么？",
                    "suggested_action": "先阅读知识点摘要，再结合问答页面继续提问。",
                    "knowledge_item_id": item.id,
                }
            )

        return {
            "topic": topic,
            "steps": fallback_steps,
        }


def build_learning_path(topic: str, user_id: int, db: Session):
    selected_items = select_relevant_knowledge_items(topic, user_id, db)

    if not selected_items:
        return {
            "topic": topic,
            "steps": [
                {
                    "step": 1,
                    "phase": "基础",
                    "title": "暂无匹配知识点",
                    "description": "当前知识库中没有找到与该主题相关的知识点，请先上传相关资料并生成知识点。",
                    "recommended_question": "这个主题需要先补充哪些基础资料？",
                    "suggested_action": "先上传相关文档，再生成知识点并重新尝试。",
                    "knowledge_item_id": None,
                }
            ],
        }

    return generate_learning_path_with_llm(topic, selected_items)
from pydantic import BaseModel


class LearningPathRequest(BaseModel):
    topic: str


class LearningStep(BaseModel):
    step: int
    phase: str
    title: str
    description: str
    recommended_question: str | None = None
    suggested_action: str | None = None
    knowledge_item_id: int | None = None


class LearningPathResponse(BaseModel):
    topic: str
    steps: list[LearningStep]
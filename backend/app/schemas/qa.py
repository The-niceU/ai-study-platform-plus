from pydantic import BaseModel


class QARequest(BaseModel):
    query: str
    top_k: int = 3


class QAResponse(BaseModel):
    answer: str
    sources: list[dict]


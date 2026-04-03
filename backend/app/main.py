from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.documents import router as documents_router
from app.api.health import router as health_router
from app.core.database import Base, engine
from app.models.document import Document
from app.models.user import User
from app.models.chunk import Chunk
from app.api.search import router as search_router
from app.api.qa import router as qa_router
from app.api.knowledge import router as knowledge_router
from app.models.knowledge_item import KnowledgeItem
from app.api.learning_path import router as learning_path_router

app = FastAPI(title="AI Study Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(qa_router, prefix="/api")
app.include_router(knowledge_router, prefix="/api")
app.include_router(learning_path_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "AI Study Platform backend is running"}
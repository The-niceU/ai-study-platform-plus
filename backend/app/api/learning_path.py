from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.learning_path import LearningPathRequest, LearningPathResponse
from app.services.learning_path_service import build_learning_path

router = APIRouter(prefix="/learning-path", tags=["learning-path"])


@router.post("/", response_model=LearningPathResponse)
def generate_learning_path(
    data: LearningPathRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return build_learning_path(data.topic, current_user.id, db)
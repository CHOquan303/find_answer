"""全文搜索路由。"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, selectinload

from .. import models
from ..deps import get_db

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("")
def search(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    pattern = f"%{q}%"
    questions = (
        db.query(models.Question)
        .options(selectinload(models.Question.author))
        .filter(
            models.Question.title.ilike(pattern)
            | models.Question.content.ilike(pattern)
        )
        .order_by(models.Question.created_at.desc())
        .limit(50)
        .all()
    )
    return {
        "items": [
            {
                "id": x.id,
                "title": x.title,
                "status": x.status,
                "created_at": x.created_at,
            }
            for x in questions
        ]
    }

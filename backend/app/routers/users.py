"""用户路由。"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..deps import get_current_user, get_db
from ..services.confidence import confidence_score, confidence_title

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=schemas.UserMe)
def me(user=Depends(get_current_user), db: Session = Depends(get_db)):
    score = confidence_score(db, user)
    return schemas.UserMe(
        id=user.id,
        username=user.username,
        real_name=user.real_name,
        grade=user.grade,
        is_name_verified=user.is_name_verified,
        is_full_verified=user.is_full_verified,
        is_admin=user.is_admin,
        confidence_score=score,
        confidence_title=confidence_title(score),
    )

"""回答相关路由：点赞、举报、追问。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_current_user, get_db

router = APIRouter(prefix="/api/answers", tags=["answers"])


@router.post("/{answer_id}/like")
def like_answer(
    answer_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)
):
    a = db.get(models.Answer, answer_id)
    if not a:
        raise HTTPException(404, "回答不存在")

    existing = (
        db.query(models.Like)
        .filter(models.Like.user_id == user.id, models.Like.answer_id == answer_id)
        .first()
    )
    if existing:
        db.delete(existing)
        db.commit()
        liked = False
    else:
        db.add(models.Like(user_id=user.id, answer_id=answer_id))
        db.commit()
        liked = True

    like_count = (
        db.query(models.Like).filter(models.Like.answer_id == answer_id).count()
    )
    return {"liked": liked, "like_count": like_count}


@router.post("/{answer_id}/report", status_code=201)
def report_answer(
    answer_id: int,
    data: schemas.ReportCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    a = db.get(models.Answer, answer_id)
    if not a:
        raise HTTPException(404, "回答不存在")

    db.add(
        models.Report(
            reporter_id=user.id,
            answer_id=answer_id,
            reason=data.reason,
            status=models.ReportStatus.PENDING.value,
        )
    )
    db.commit()
    return {"reported": True}


@router.post("/{answer_id}/replies", response_model=schemas.ReplyOut, status_code=201)
def create_reply(
    answer_id: int,
    data: schemas.ReplyCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    a = db.get(models.Answer, answer_id)
    if not a:
        raise HTTPException(404, "回答不存在")

    if data.parent_id is not None:
        parent = db.get(models.Reply, data.parent_id)
        if not parent or parent.answer_id != answer_id:
            raise HTTPException(400, "无效的父回复")

    r = models.Reply(
        answer_id=answer_id,
        author_id=user.id,
        parent_id=data.parent_id,
        content=data.content,
    )
    db.add(r)
    db.commit()
    db.refresh(r)
    return schemas.ReplyOut(
        id=r.id,
        content=r.content,
        author=schemas.UserBrief.model_validate(user),
        parent_id=r.parent_id,
        created_at=r.created_at,
        children=[],
    )

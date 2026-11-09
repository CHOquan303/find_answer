"""问题相关路由（含提交回答、采纳、标注已解决）。"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from .. import models, schemas
from ..deps import get_db, require_answerer, require_asker

router = APIRouter(prefix="/api/questions", tags=["questions"])

PAGE_SIZE = 20


def _question_out(q: models.Question, answer_count: int = 0) -> schemas.QuestionOut:
    return schemas.QuestionOut(
        id=q.id,
        title=q.title,
        content=q.content,
        status=q.status,
        category_id=q.category_id,
        author=schemas.UserBrief.model_validate(q.author),
        answer_count=answer_count,
        created_at=q.created_at,
    )


def _reply_out(r: models.Reply) -> schemas.ReplyOut:
    return schemas.ReplyOut(
        id=r.id,
        content=r.content,
        author=schemas.UserBrief.model_validate(r.author),
        parent_id=r.parent_id,
        created_at=r.created_at,
        children=[_reply_out(c) for c in r.children],
    )


def _answer_out(a: models.Answer) -> schemas.AnswerOut:
    return schemas.AnswerOut(
        id=a.id,
        content=a.content,
        is_accepted=a.is_accepted,
        author=schemas.UserBrief.model_validate(a.author),
        like_count=len(a.likes),
        created_at=a.created_at,
        replies=[_reply_out(r) for r in a.replies if r.parent_id is None],
    )


@router.get("")
def list_questions(
    page: int = Query(1, ge=1),
    category: Optional[int] = None,
    status: Optional[str] = None,
    sort: str = "latest",
    db: Session = Depends(get_db),
):
    base = db.query(models.Question).options(selectinload(models.Question.author))
    if category:
        base = base.filter(models.Question.category_id == category)
    if status == "resolved":
        base = base.filter(models.Question.status == models.QuestionStatus.RESOLVED.value)
    elif status == "unresolved":
        base = base.filter(
            models.Question.status.in_(
                [
                    models.QuestionStatus.PENDING.value,
                    models.QuestionStatus.ANSWERED.value,
                ]
            )
        )
    total = base.count()

    if sort == "hot":
        cnt = (
            db.query(models.Answer.question_id, func.count(models.Answer.id).label("c"))
            .group_by(models.Answer.question_id)
            .subquery()
        )
        rows = (
            base.outerjoin(cnt, models.Question.id == cnt.c.question_id)
            .order_by(
                func.coalesce(cnt.c.c, 0).desc(), models.Question.created_at.desc()
            )
            .offset((page - 1) * PAGE_SIZE)
            .limit(PAGE_SIZE)
            .all()
        )
    else:
        rows = (
            base.order_by(models.Question.created_at.desc())
            .offset((page - 1) * PAGE_SIZE)
            .limit(PAGE_SIZE)
            .all()
        )

    qids = [q.id for q in rows]
    counts = dict(
        db.query(models.Answer.question_id, func.count(models.Answer.id))
        .filter(models.Answer.question_id.in_(qids))
        .group_by(models.Answer.question_id)
        .all()
    )

    return {
        "items": [_question_out(q, counts.get(q.id, 0)) for q in rows],
        "total": total,
        "page": page,
    }


@router.get("/{question_id}", response_model=schemas.QuestionDetail)
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = (
        db.query(models.Question)
        .options(
            selectinload(models.Question.author),
            selectinload(models.Question.answers).selectinload(models.Answer.author),
            selectinload(models.Question.answers)
            .selectinload(models.Answer.replies)
            .selectinload(models.Reply.author),
            selectinload(models.Question.answers).selectinload(models.Answer.likes),
        )
        .filter(models.Question.id == question_id)
        .first()
    )
    if not q:
        raise HTTPException(404, "问题不存在")
    return schemas.QuestionDetail(
        id=q.id,
        title=q.title,
        content=q.content,
        status=q.status,
        category_id=q.category_id,
        author=schemas.UserBrief.model_validate(q.author),
        answer_count=len(q.answers),
        created_at=q.created_at,
        answers=[_answer_out(a) for a in q.answers],
    )


@router.post("", response_model=schemas.QuestionOut, status_code=201)
def create_question(
    data: schemas.QuestionCreate,
    user=Depends(require_asker),
    db: Session = Depends(get_db),
):
    q = models.Question(
        author_id=user.id,
        category_id=data.category_id,
        title=data.title,
        content=data.content,
        status=models.QuestionStatus.PENDING.value,
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return _question_out(q, 0)


@router.post("/{question_id}/answers", response_model=schemas.AnswerOut, status_code=201)
def create_answer(
    question_id: int,
    data: schemas.AnswerCreate,
    user=Depends(require_answerer),
    db: Session = Depends(get_db),
):
    q = db.get(models.Question, question_id)
    if not q:
        raise HTTPException(404, "问题不存在")

    a = models.Answer(question_id=question_id, author_id=user.id, content=data.content)
    db.add(a)
    db.flush()  # 先生成 a.id，供通知引用
    if q.status == models.QuestionStatus.PENDING.value:
        q.status = models.QuestionStatus.ANSWERED.value
    if q.author_id != user.id:
        db.add(
            models.Notification(
                user_id=q.author_id,
                type="new_answer",
                question_id=q.id,
                answer_id=a.id,
            )
        )
    db.commit()
    db.refresh(a)
    return _answer_out(a)


@router.patch(
    "/{question_id}/answers/{answer_id}/accept", response_model=schemas.AnswerOut
)
def accept_answer(
    question_id: int,
    answer_id: int,
    user=Depends(require_asker),
    db: Session = Depends(get_db),
):
    q = db.get(models.Question, question_id)
    if not q:
        raise HTTPException(404, "问题不存在")
    if q.author_id != user.id:
        raise HTTPException(403, "只有提问者能采纳回答")
    a = db.get(models.Answer, answer_id)
    if not a or a.question_id != question_id:
        raise HTTPException(404, "回答不存在")
    a.is_accepted = True
    db.commit()
    db.refresh(a)
    return _answer_out(a)


@router.patch("/{question_id}/resolve", response_model=schemas.QuestionOut)
def resolve_question(
    question_id: int,
    user=Depends(require_asker),
    db: Session = Depends(get_db),
):
    q = db.get(models.Question, question_id)
    if not q:
        raise HTTPException(404, "问题不存在")
    if q.author_id != user.id:
        raise HTTPException(403, "只有提问者能标注已解决")
    q.status = models.QuestionStatus.RESOLVED.value
    db.commit()
    db.refresh(q)
    return _question_out(q, len(q.answers))

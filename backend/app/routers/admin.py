"""管理后台路由。"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db, require_admin
from ..services.roster import import_roster

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/roster")
async def upload_roster(
    file: UploadFile = File(...),
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    content = await file.read()
    count = import_roster(db, content)
    return {"imported": count}


@router.post("/categories", response_model=schemas.CategoryOut, status_code=201)
def create_category(
    data: schemas.CategoryCreate,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    c = models.Category(name=data.name, sort_order=data.sort_order)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int, admin=Depends(require_admin), db: Session = Depends(get_db)
):
    c = db.get(models.Category, category_id)
    if not c:
        raise HTTPException(404, "分类不存在")
    db.delete(c)
    db.commit()
    return {"deleted": True}


@router.delete("/questions/{question_id}")
def delete_question(
    question_id: int, admin=Depends(require_admin), db: Session = Depends(get_db)
):
    q = db.get(models.Question, question_id)
    if not q:
        raise HTTPException(404, "问题不存在")
    db.delete(q)
    db.commit()
    return {"deleted": True}


@router.delete("/answers/{answer_id}")
def delete_answer(
    answer_id: int, admin=Depends(require_admin), db: Session = Depends(get_db)
):
    a = db.get(models.Answer, answer_id)
    if not a:
        raise HTTPException(404, "回答不存在")
    db.delete(a)
    db.commit()
    return {"deleted": True}


@router.get("/reports", response_model=list[schemas.ReportOut])
def list_reports(admin=Depends(require_admin), db: Session = Depends(get_db)):
    return (
        db.query(models.Report)
        .order_by(models.Report.status, models.Report.created_at.desc())
        .all()
    )


@router.patch("/reports/{report_id}", response_model=schemas.ReportOut)
def review_report(
    report_id: int,
    data: schemas.ReportReviewIn,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    r = db.get(models.Report, report_id)
    if not r:
        raise HTTPException(404, "举报不存在")
    valid = (models.ReportStatus.CONFIRMED.value, models.ReportStatus.DISMISSED.value)
    if data.status not in valid:
        raise HTTPException(400, "状态只能为 confirmed 或 dismissed")
    r.status = data.status
    db.commit()
    db.refresh(r)
    return r

"""认证：注册与登录。"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..security import create_access_token, hash_password, verify_password
from ..services.roster import verify_student
from ..utils import utcnow

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _verify_hint(name_ok: bool, full_ok: bool) -> str:
    if full_ok:
        return "核验通过，已开通提问和回答权限"
    if name_ok:
        return "核验通过，已开通提问权限"
    return "核验未通过，仅可浏览"


@router.post(
    "/register", response_model=schemas.RegisterOut, status_code=status.HTTP_201_CREATED
)
def register(data: schemas.RegisterIn, db: Session = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.username == data.username).first()
    if exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "用户名已被占用")

    name_ok, full_ok = verify_student(db, data.real_name, data.student_id)

    user = models.User(
        username=data.username,
        password_hash=hash_password(data.password),
        real_name=data.real_name,
        student_id=data.student_id,
        grade=data.grade,
        is_name_verified=name_ok,
        is_full_verified=full_ok,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return schemas.RegisterOut(
        id=user.id,
        username=user.username,
        is_name_verified=user.is_name_verified,
        is_full_verified=user.is_full_verified,
        verify_hint=_verify_hint(name_ok, full_ok),
    )


@router.post("/login", response_model=schemas.TokenOut)
def login(data: schemas.LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "用户名或密码错误")

    user.last_active_at = utcnow()
    db.commit()
    return schemas.TokenOut(access_token=create_access_token(user.id))

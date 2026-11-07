"""FastAPI 依赖注入。"""

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User
from .security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "登录已过期，请重新登录")
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "用户不存在")
    return user


def require_asker(user: User = Depends(get_current_user)) -> User:
    if not (user.is_name_verified or user.is_full_verified or user.is_admin):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "完成名单核验后才能提问")
    return user


def require_answerer(user: User = Depends(get_current_user)) -> User:
    if not (user.is_full_verified or user.is_admin):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "完成姓名+学号核验后才能回答")
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "需要管理员权限")
    return user

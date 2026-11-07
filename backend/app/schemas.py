"""Pydantic 请求/响应模型。"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ---- Auth ----
class RegisterIn(BaseModel):
    username: str
    password: str
    real_name: str
    student_id: Optional[str] = None
    grade: Optional[str] = None


class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---- User ----
class UserBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    real_name: str
    grade: Optional[str] = None
    is_admin: bool


class RegisterOut(BaseModel):
    id: int
    username: str
    is_name_verified: bool
    is_full_verified: bool
    verify_hint: str


class UserMe(BaseModel):
    id: int
    username: str
    real_name: str
    grade: Optional[str] = None
    is_name_verified: bool
    is_full_verified: bool
    is_admin: bool
    confidence_score: int
    confidence_title: str


# ---- Category ----
class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CategoryCreate(BaseModel):
    name: str
    sort_order: int = 0


# ---- Reply ----
class ReplyCreate(BaseModel):
    content: str
    parent_id: Optional[int] = None


class ReplyOut(BaseModel):
    id: int
    content: str
    author: UserBrief
    parent_id: Optional[int] = None
    created_at: datetime
    children: list[ReplyOut] = []


# ---- Answer ----
class AnswerCreate(BaseModel):
    content: str


class AnswerOut(BaseModel):
    id: int
    content: str
    is_accepted: bool
    author: UserBrief
    like_count: int
    created_at: datetime
    replies: list[ReplyOut] = []


# ---- Question ----
class QuestionCreate(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None


class QuestionOut(BaseModel):
    id: int
    title: str
    content: str
    status: str
    category_id: Optional[int] = None
    author: UserBrief
    answer_count: int
    created_at: datetime


class QuestionDetail(QuestionOut):
    answers: list[AnswerOut] = []


# ---- Report ----
class ReportCreate(BaseModel):
    reason: str


class ReportReviewIn(BaseModel):
    status: str  # confirmed / dismissed


class ReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    answer_id: int
    reason: str
    status: str
    created_at: datetime


# ---- Notification ----
class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
    question_id: Optional[int] = None
    answer_id: Optional[int] = None
    is_read: bool
    created_at: datetime


# 解析前向引用（ReplyOut 自引用、QuestionDetail→AnswerOut 等）
ReplyOut.model_rebuild()
AnswerOut.model_rebuild()
QuestionDetail.model_rebuild()

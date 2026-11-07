"""SQLAlchemy ORM 模型 —— 对应设计稿中的 9 张表。

类型一律使用通用类型（String/Text/Integer/Boolean/DateTime），
按 PostgreSQL 语义编写，便于日后从 SQLite 迁移。
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Grade(str, Enum):
    """年级，决定置信度基础分。"""

    FRESHMAN = "freshman"    # 大一
    SOPHOMORE = "sophomore"  # 大二
    JUNIOR = "junior"        # 大三
    SENIOR = "senior"        # 大四


class QuestionStatus(str, Enum):
    """问题三态。"""

    PENDING = "pending"      # 待回答
    ANSWERED = "answered"    # 已回答
    RESOLVED = "resolved"    # 已解决


class ReportStatus(str, Enum):
    """举报处理状态。"""

    PENDING = "pending"      # 待审核
    CONFIRMED = "confirmed"  # 确认违规
    DISMISSED = "dismissed"  # 驳回


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    real_name: Mapped[str] = mapped_column(String(50), nullable=False)
    student_id: Mapped[Optional[str]] = mapped_column(String(30))
    grade: Mapped[Optional[str]] = mapped_column(String(20))  # Grade 枚举值，注册时自选
    is_name_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_full_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    last_active_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    questions: Mapped[list[Question]] = relationship(back_populates="author")
    answers: Mapped[list[Answer]] = relationship(back_populates="author")


class Roster(Base):
    """CSV 名单，注册核验的「标准答案库」。"""

    __tablename__ = "roster"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    real_name: Mapped[str] = mapped_column(String(50), nullable=False)
    student_id: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    questions: Mapped[list[Question]] = relationship(back_populates="category")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default=QuestionStatus.PENDING.value
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    author: Mapped[User] = relationship(back_populates="questions")
    category: Mapped[Optional[Category]] = relationship(back_populates="questions")
    answers: Mapped[list[Answer]] = relationship(back_populates="question")


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    question: Mapped[Question] = relationship(back_populates="answers")
    author: Mapped[User] = relationship(back_populates="answers")
    replies: Mapped[list[Reply]] = relationship(back_populates="answer")
    likes: Mapped[list[Like]] = relationship(back_populates="answer")
    reports: Mapped[list[Report]] = relationship(back_populates="answer")


class Reply(Base):
    """追问/回复，parent_id 递归支持多层。"""

    __tablename__ = "replies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id", ondelete="CASCADE"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("replies.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    answer: Mapped[Answer] = relationship(back_populates="replies")
    author: Mapped[User] = relationship()
    parent: Mapped[Optional[Reply]] = relationship(
        remote_side="Reply.id", back_populates="children"
    )
    children: Mapped[list[Reply]] = relationship(back_populates="parent")


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint("user_id", "answer_id", name="uq_like_user_answer"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    user: Mapped[User] = relationship()
    answer: Mapped[Answer] = relationship(back_populates="likes")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id", ondelete="CASCADE"), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default=ReportStatus.PENDING.value
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    reporter: Mapped[User] = relationship()
    answer: Mapped[Answer] = relationship(back_populates="reports")


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # 如 new_answer
    question_id: Mapped[Optional[int]] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"))
    answer_id: Mapped[Optional[int]] = mapped_column(ForeignKey("answers.id", ondelete="CASCADE"))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    user: Mapped[User] = relationship()

"""置信度计算（实时，不落库冗余字段）。"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import Answer, Like, Report, ReportStatus, User
from ..utils import utcnow

GRADE_BASE = {
    "freshman": 0,    # 大一
    "sophomore": 35,  # 大二
    "junior": 55,     # 大三
    "senior": 70,     # 大四
}

TITLES = [
    (75, "🥇 权威解答"),
    (55, "🥈 值得信赖"),
    (35, "🥉 靠谱新人"),
]


def confidence_score(db: Session, user: User) -> int:
    base = GRADE_BASE.get(user.grade, 0)

    # 活跃衰减：90 天未活跃后，每满 30 天衰减 5%
    if user.last_active_at:
        days = (utcnow() - user.last_active_at).days
        if days > 90:
            base *= 0.95 ** ((days - 90) // 30)

    accepted = (
        db.query(func.count(Answer.id))
        .filter(Answer.author_id == user.id, Answer.is_accepted.is_(True))
        .scalar()
        or 0
    )
    like_count = (
        db.query(func.count(Like.id))
        .join(Answer, Like.answer_id == Answer.id)
        .filter(Answer.author_id == user.id)
        .scalar()
        or 0
    )
    mark = (
        db.query(func.count(Report.id))
        .join(Answer, Report.answer_id == Answer.id)
        .filter(
            Answer.author_id == user.id,
            Report.status == ReportStatus.CONFIRMED.value,
        )
        .scalar()
        or 0
    )

    interaction = min(accepted * 5 + like_count // 3, 30) - mark
    interaction = min(interaction, 30)

    return int(base + interaction)


def confidence_title(score: int) -> str:
    for threshold, title in TITLES:
        if score >= threshold:
            return title
    return "无称号"

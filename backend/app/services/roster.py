"""名单（roster）相关：CSV 导入与注册核验。"""

import csv
import io
from typing import Optional

from sqlalchemy.orm import Session

from ..models import Roster


def import_roster(db: Session, csv_content: bytes) -> int:
    """全量替换名单：清空后按 CSV 导入，返回导入条数。

    CSV 列名兼容「姓名/name」「学号/student_id」。
    """
    text = csv_content.decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text)))

    db.query(Roster).delete()
    count = 0
    for row in rows:
        name = (row.get("姓名") or row.get("name") or "").strip()
        sid = (row.get("学号") or row.get("student_id") or "").strip()
        if not name or not sid:
            continue
        db.add(Roster(real_name=name, student_id=sid))
        count += 1
    db.commit()
    return count


def verify_student(
    db: Session, real_name: str, student_id: Optional[str]
) -> tuple[bool, bool]:
    """返回 (is_name_verified, is_full_verified)。"""
    if not real_name:
        return False, False

    name_ok = (
        db.query(Roster).filter(Roster.real_name == real_name).first() is not None
    )
    full_ok = False
    if name_ok and student_id:
        full_ok = (
            db.query(Roster)
            .filter(Roster.real_name == real_name, Roster.student_id == student_id)
            .first()
            is not None
        )
    return name_ok, full_ok

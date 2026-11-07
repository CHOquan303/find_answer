"""通用工具函数。"""

from datetime import datetime, timezone


def utcnow() -> datetime:
    """返回 naive UTC 当前时间（与数据库存储约定一致）。"""
    return datetime.now(timezone.utc).replace(tzinfo=None)

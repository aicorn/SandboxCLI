"""时间戳值对象"""
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, field_validator


class Timestamp(BaseModel):
    """不可变的时间戳值对象"""
    value: datetime

    model_config = {"frozen": True}

    @field_validator("value", mode="before")
    @classmethod
    def _ensure_timezone(cls, v: datetime) -> datetime:
        """确保时间戳有时区信息"""
        if isinstance(v, datetime):
            if v.tzinfo is None:
                return v.replace(tzinfo=timezone.utc)
        return v

    @classmethod
    def now(cls) -> "Timestamp":
        """创建当前时间戳"""
        return cls(value=datetime.now(timezone.utc))

    @classmethod
    def from_datetime(cls, dt: datetime) -> "Timestamp":
        """从datetime对象创建时间戳"""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return cls(value=dt)

    @classmethod
    def from_iso_string(cls, iso_string: str) -> "Timestamp":
        """从ISO格式字符串创建时间戳"""
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        return cls(value=dt)

    def to_iso_string(self) -> str:
        """转换为ISO格式字符串"""
        return self.value.isoformat()

    def __str__(self) -> str:
        return self.to_iso_string()

    def __repr__(self) -> str:
        return f"Timestamp('{self.to_iso_string()}')"

"""超时配置值对象"""
from typing import Optional

from pydantic import BaseModel, field_validator


class Timeout(BaseModel):
    """超时配置值对象"""
    seconds: int = 30

    model_config = {"frozen": True}

    @field_validator("seconds")
    @classmethod
    def _validate_seconds(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Timeout must be at least 1 second")
        if v > 3600:
            raise ValueError("Timeout cannot exceed 3600 seconds (1 hour)")
        return v

    @classmethod
    def default(cls) -> "Timeout":
        """创建默认超时配置"""
        return cls(seconds=30)

    @classmethod
    def from_seconds(cls, seconds: int) -> "Timeout":
        """从秒数创建超时配置"""
        return cls(seconds=seconds)

    def __str__(self) -> str:
        return f"{self.seconds}s"

    def __repr__(self) -> str:
        return f"Timeout(seconds={self.seconds})"

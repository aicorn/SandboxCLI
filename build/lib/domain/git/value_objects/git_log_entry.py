"""Git日志条目值对象"""
from typing import Optional

from pydantic import BaseModel, Field


class GitLogEntry(BaseModel):
    """Git日志条目值对象"""
    hash: str
    short_hash: str
    author: str
    author_email: str
    date: str
    message: str
    refs: Optional[str] = None

    model_config = {"frozen": True}

    @classmethod
    def from_full_hash(cls, hash: str, **kwargs) -> "GitLogEntry":
        """从完整hash创建"""
        return cls(hash=hash, short_hash=hash[:7], **kwargs)

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "hash": self.hash,
            "short_hash": self.short_hash,
            "author": self.author,
            "author_email": self.author_email,
            "date": self.date,
            "message": self.message,
            "refs": self.refs,
        }

    def __str__(self) -> str:
        return f"{self.short_hash} - {self.message}"

    def __repr__(self) -> str:
        return f"GitLogEntry(hash='{self.short_hash}', message='{self.message[:30]}...')"

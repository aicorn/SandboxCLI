"""Git提交实体"""
from typing import Optional

from pydantic import BaseModel, Field

from ..value_objects import GitLogEntry


class Commit(BaseModel):
    """Git提交实体"""
    hash: str
    log: GitLogEntry

    model_config = {"frozen": True}

    @property
    def commit_hash(self) -> str:
        """获取提交哈希"""
        return self.hash

    @classmethod
    def from_log_entry(cls, log: GitLogEntry) -> "Commit":
        """从日志条目创建提交"""
        return cls(hash=log.hash, log=log)

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "hash": self.hash,
            "log": self.log.to_dict(),
        }

    def __str__(self) -> str:
        return self.hash[:7]

    def __repr__(self) -> str:
        return f"Commit(hash='{self.hash[:7]}', message='{self.log.message[:30]}...')"

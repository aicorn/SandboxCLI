"""分支信息值对象"""
from typing import Optional

from pydantic import BaseModel, Field


class BranchInfo(BaseModel):
    """分支信息值对象"""
    name: str
    is_remote: bool = False
    is_current: bool = False
    upstream: Optional[str] = None
    ahead: int = 0
    behind: int = 0

    model_config = {"frozen": True}

    def has_upstream(self) -> bool:
        """判断是否有上游分支"""
        return self.upstream is not None

    def is_ahead_of_upstream(self) -> bool:
        """判断是否领先上游分支"""
        return self.ahead > 0

    def is_behind_upstream(self) -> bool:
        """判断是否落后上游分支"""
        return self.behind > 0

    def is_tracked(self) -> bool:
        """判断是否是跟踪分支"""
        return self.has_upstream()

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "name": self.name,
            "is_remote": self.is_remote,
            "is_current": self.is_current,
            "upstream": self.upstream,
            "ahead": self.ahead,
            "behind": self.behind,
        }

    def __str__(self) -> str:
        prefix = "remotes/" if self.is_remote else ""
        suffix = " *" if self.is_current else ""
        return f"{prefix}{self.name}{suffix}"

    def __repr__(self) -> str:
        return f"BranchInfo(name='{self.name}', is_current={self.is_current})"

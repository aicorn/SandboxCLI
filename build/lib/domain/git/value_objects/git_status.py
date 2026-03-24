"""Git状态值对象"""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class GitStatus(BaseModel):
    """Git状态值对象"""
    branch: str
    is_clean: bool = True
    staged_files: List[str] = Field(default_factory=list)
    modified_files: List[str] = Field(default_factory=list)
    untracked_files: List[str] = Field(default_factory=list)
    ahead: int = 0
    behind: int = 0

    model_config = {"frozen": True}

    def has_changes(self) -> bool:
        """判断是否有未提交的更改"""
        return not self.is_clean

    def has_staged_changes(self) -> bool:
        """判断是否有暂存的更改"""
        return len(self.staged_files) > 0

    def has_unstaged_changes(self) -> bool:
        """判断是否有未暂存的更改"""
        return len(self.modified_files) > 0

    def has_untracked_files(self) -> bool:
        """判断是否有未跟踪的文件"""
        return len(self.untracked_files) > 0

    def is_ahead(self) -> bool:
        """判断是否领先远程"""
        return self.ahead > 0

    def is_behind(self) -> bool:
        """判断是否落后远程"""
        return self.behind > 0

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "branch": self.branch,
            "is_clean": self.is_clean,
            "staged_files": self.staged_files,
            "modified_files": self.modified_files,
            "untracked_files": self.untracked_files,
            "ahead": self.ahead,
            "behind": self.behind,
        }

"""Git仓库实体"""
from typing import List, Optional

from pydantic import BaseModel, Field

from ..value_objects import BranchInfo, GitStatus


class Repository(BaseModel):
    """Git仓库实体"""
    path: str
    current_branch: Optional[str] = None
    branches: List[BranchInfo] = Field(default_factory=list)
    status: Optional[GitStatus] = None

    model_config = {"frozen": True}

    @property
    def repo_path(self) -> str:
        """获取仓库路径"""
        return self.path

    @property
    def has_changes(self) -> bool:
        """判断是否有未提交的更改"""
        return self.status is not None and self.status.has_changes()

    def get_current_branch_name(self) -> Optional[str]:
        """获取当前分支名称"""
        return self.current_branch

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "path": self.path,
            "current_branch": self.current_branch,
            "branches": [b.to_dict() for b in self.branches],
            "status": self.status.to_dict() if self.status else None,
        }

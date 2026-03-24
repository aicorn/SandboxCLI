"""Git仓库聚合"""
from typing import Dict, List, Optional

from ..entities import Branch, Commit, Repository
from ..value_objects import BranchInfo, GitLogEntry, GitStatus


class RepositoryAggregate:
    """Git仓库聚合根"""

    def __init__(self, repository: Repository):
        self._repository = repository

    @property
    def repository(self) -> Repository:
        """获取仓库实体"""
        return self._repository

    @property
    def repo_path(self) -> str:
        """获取仓库路径"""
        return self._repository.path

    def get_current_branch(self) -> Optional[str]:
        """获取当前分支"""
        return self._repository.current_branch

    def get_status(self) -> Optional[GitStatus]:
        """获取Git状态"""
        return self._repository.status

    def get_branches(self) -> List[BranchInfo]:
        """获取所有分支"""
        return self._repository.branches

    def get_local_branches(self) -> List[BranchInfo]:
        """获取本地分支"""
        return [b for b in self._repository.branches if not b.is_remote]

    def get_remote_branches(self) -> List[BranchInfo]:
        """获取远程分支"""
        return [b for b in self._repository.branches if b.is_remote]

    def has_changes(self) -> bool:
        """判断是否有未提交的更改"""
        return self._repository.has_changes()

    def is_clean(self) -> bool:
        """判断工作区是否干净"""
        return self._repository.status is not None and self._repository.status.is_clean

    def to_dict(self) -> Dict:
        """转换为字典"""
        return self._repository.to_dict()

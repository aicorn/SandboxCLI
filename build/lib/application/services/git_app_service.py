"""Git应用服务"""
from typing import Dict, List, Optional

from ...domain.git import GitService, RepositoryAggregate
from ...domain.shared import Result
from ..commands.git import PullCodeCommand, SwitchBranchCommand
from ..queries.git import GetBranchesQuery, GetGitLogQuery, GetGitStatusQuery


class GitAppService:
    """Git应用服务"""

    def __init__(self):
        self._current_repo: Optional[RepositoryAggregate] = None

    def get_git_status(self, query: GetGitStatusQuery) -> Result[Dict]:
        """获取Git状态"""
        if not self._current_repo or self._current_repo.repo_path != query.repo_path:
            self._current_repo = GitService.create_repository(query.repo_path)
        
        status = self._current_repo.get_status()
        if status:
            return Result.ok(status.to_dict())
        return Result.ok(None)

    def get_git_log(self, query: GetGitLogQuery) -> Result[List]:
        """获取Git日志"""
        # 实际日志获取需要通过基础设施层实现
        return Result.ok([])

    def get_branches(self, query: GetBranchesQuery) -> Result[List]:
        """获取分支列表"""
        if not self._current_repo or self._current_repo.repo_path != query.repo_path:
            self._current_repo = GitService.create_repository(query.repo_path)
        
        branches = self._current_repo.get_branches()
        return Result.ok([b.to_dict() for b in branches])

    def switch_branch(self, command: SwitchBranchCommand) -> Result[None]:
        """切换分支"""
        validation = GitService.validate_branch_name(command.branch_name)
        if validation.is_failure():
            return Result.fail(validation.error)
        
        # 实际分支切换需要通过基础设施层实现
        return Result.ok(None)

    def pull_code(self, command: PullCodeCommand) -> Result[None]:
        """拉取代码"""
        # 实际代码拉取需要通过基础设施层实现
        return Result.ok(None)

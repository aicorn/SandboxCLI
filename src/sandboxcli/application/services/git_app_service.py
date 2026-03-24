"""Git应用服务"""
from typing import Dict, List, Optional

from ...domain.configuration.value_objects import GitConfig
from ...domain.git import CloneService, GitService, RepositoryAggregate
from ...domain.git.entities import CloneOperation
from ...domain.git.value_objects import CloneResult
from ...domain.shared import Result
from ..commands.git import CloneRepositoryCommand, PullCodeCommand, SwitchBranchCommand
from ..queries.git import GetBranchesQuery, GetGitLogQuery, GetGitStatusQuery


class GitAppService:
    """Git应用服务"""

    def __init__(self):
        self._current_repo: Optional[RepositoryAggregate] = None
        self._git_config: Optional[GitConfig] = None
        self._clone_operation: Optional[CloneOperation] = None

    def set_git_config(self, config: GitConfig) -> None:
        """设置Git配置
        
        Args:
            config: Git配置
        """
        self._git_config = config

    def get_git_config(self) -> Optional[GitConfig]:
        """获取Git配置"""
        return self._git_config

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

    def clone_repository(
        self,
        command: CloneRepositoryCommand,
        git_config: Optional[GitConfig] = None,
    ) -> Result[CloneOperation]:
        """克隆仓库
        
        Args:
            command: 克隆仓库命令
            git_config: Git配置（可选）
            
        Returns:
            Result: 克隆操作结果
        """
        # 使用提供的配置或服务配置
        config = git_config or self._git_config
        
        # 如果没有配置，创建空配置
        if not config:
            config = GitConfig.empty()
        
        # 验证Git配置
        validate_config_result = CloneService.validate_git_config(config)
        if not validate_config_result.is_success():
            # 如果没有使用配置中的Git凭据，则不需要验证配置
            if not command.use_config_git:
                config = GitConfig.empty()
            else:
                return Result.fail(validate_config_result.error)
        
        # 创建克隆选项
        options_result = CloneService.create_clone_options_from_config(
            config=config,
            override_url=command.url,
            target_dir=command.target_dir,
            branch=command.branch,
            depth=command.depth,
        )
        
        if not options_result.is_success():
            return Result.fail(options_result.error)
        
        # 创建克隆操作
        operation = CloneService.create_clone_operation(
            url=command.url,
            target_dir=command.target_dir,
            branch=command.branch,
            depth=command.depth,
            recursive=command.recursive,
        )
        
        self._clone_operation = operation
        return Result.ok(operation)

    def get_clone_operation(self) -> Optional[CloneOperation]:
        """获取当前克隆操作"""
        return self._clone_operation

    def execute_clone(
        self,
        command: CloneRepositoryCommand,
        git_config: Optional[GitConfig] = None,
    ) -> Result[CloneResult]:
        """执行克隆操作
        
        注意：实际的克隆执行需要通过基础设施层（Remote Adapter）来实现。
        此方法只负责领域逻辑验证和操作创建。
        
        Args:
            command: 克隆仓库命令
            git_config: Git配置
            
        Returns:
            Result: 克隆结果
        """
        # 先创建克隆操作
        clone_result = self.clone_repository(command, git_config)
        if not clone_result.is_success():
            return Result.fail(clone_result.error)
        
        operation = clone_result.value
        
        # 标记开始执行
        operation.start()
        
        # TODO: 通过基础设施层执行实际的git clone命令
        # 这里需要注入RemoteAdapter来执行远程命令
        # remote_adapter.execute_clone(operation, git_config)
        
        # 暂时返回待执行状态
        return Result.ok(CloneResult.success(
            message="克隆操作已创建，等待执行",
            cloned_path=command.target_dir or command.url.split("/")[-1].replace(".git", ""),
            remote_url=command.url,
            branch=command.branch,
        ))

"""Git应用服务"""
from typing import Dict, List, Optional, TYPE_CHECKING

from ...domain.configuration.value_objects import GitConfig
from ...domain.git import CloneService, GitService, RepositoryAggregate
from ...domain.git.entities import CloneOperation
from ...domain.git.value_objects import CloneResult
from ...domain.shared import Result
from ...domain.command import CommandInput
from ...infrastructure.persistence.config.config_repository import ConfigRepository
from ...infrastructure.remote.adapter.factory import RemoteAdapterFactory
from ..commands.git import CloneRepositoryCommand, PullCodeCommand, SwitchBranchCommand
from ..queries.git import GetBranchesQuery, GetGitLogQuery, GetGitStatusQuery

if TYPE_CHECKING:
    from ...infrastructure.remote.adapter.remote_adapter import RemoteAdapter


class GitAppService:
    """Git应用服务"""

    def __init__(self):
        self._current_repo: Optional[RepositoryAggregate] = None
        self._git_config: Optional[GitConfig] = None
        self._clone_operation: Optional[CloneOperation] = None
        self._config_repository = ConfigRepository()
        self._config = self._config_repository.load()
        self._remote_client: Optional["RemoteAdapter"] = None
        # 加载git_config
        self._load_git_config()
    
    def _load_git_config(self) -> None:
        """从配置项中加载Git配置"""
        git_item = self._config.get_item("git_config")
        if git_item and git_item.value:
            try:
                from sandboxcli.domain.configuration.value_objects import (
                    GitConfig, GitRepoUrl, GitAuthType, SSHKey, GitCredential
                )
                value = git_item.value
                self._git_config = GitConfig(
                    repo_url=GitRepoUrl(url=value.get("repo_url", {}).get("url", "")) if value.get("repo_url") else GitRepoUrl(url=""),
                    auth_type=GitAuthType(auth_type=value.get("auth_type", {}).get("auth_type", "none")) if value.get("auth_type") else GitAuthType(auth_type="none"),
                    ssh_key=SSHKey(key_path=value.get("ssh_key", {}).get("key_path", ""), key_content=value.get("ssh_key", {}).get("key_content", ""), has_passphrase=value.get("ssh_key", {}).get("has_passphrase", False)) if value.get("ssh_key") else SSHKey(key_path=""),
                    credential=GitCredential.create(
                        username=value.get("credential", {}).get("username", ""),
                        email=value.get("credential", {}).get("email", ""),
                        password=value.get("credential", {}).get("password", ""),
                    ) if value.get("credential") else GitCredential.create("", "", ""),
                    default_branch=value.get("default_branch", "main"),
                    description=value.get("description", "Git配置"),
                )
            except Exception:
                pass

    def _get_base_url(self) -> Optional[str]:
        """从配置中获取base_url"""
        if self._config.server_address and self._config.server_address.base_url:
            return self._config.server_address.base_url
        return None

    def _get_timeout(self) -> int:
        """从配置中获取超时时间"""
        if self._config.timeout:
            return self._config.timeout.seconds
        return 30

    def _get_remote_client(self) -> Optional["RemoteAdapter"]:
        """获取或创建远程客户端"""
        if self._remote_client is None:
            base_url = self._get_base_url()
            if base_url:
                self._remote_client = RemoteAdapterFactory.create_sandbox_client(
                    base_url=base_url,
                    timeout=self._get_timeout(),
                )
        return self._remote_client

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
        # 如果不使用配置中的Git凭据，直接创建克隆操作（跳过验证）
        if not command.use_config_git:
            operation = CloneService.create_clone_operation(
                url=command.url,
                target_dir=command.target_dir,
                branch=command.branch,
                depth=command.depth,
                recursive=command.recursive,
            )
            self._clone_operation = operation
            return Result.ok(operation)
        
        # 使用提供的配置或服务配置
        config = git_config or self._git_config
        
        # 如果没有配置，创建空配置
        if not config:
            config = GitConfig.empty()
        
        # 验证Git配置
        validate_config_result = CloneService.validate_git_config(config)
        if not validate_config_result.is_success:
            # 配置验证失败，但用户可能没有配置git，使用空配置继续
            config = GitConfig.empty()
        
        # 创建克隆选项（即使使用空配置也能创建options）
        options_result = CloneService.create_clone_options_from_config(
            config=config,
            override_url=command.url,
            target_dir=command.target_dir,
            branch=command.branch,
            depth=command.depth,
        )
        
        if not options_result.is_success:
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
        
        通过远程沙盒执行git clone命令
        
        Args:
            command: 克隆仓库命令
            git_config: Git配置
            
        Returns:
            Result: 克隆结果
        """
        # 先创建克隆操作
        clone_result = self.clone_repository(command, git_config)
        if not clone_result.is_success:
            return Result.fail(clone_result.error)
        
        operation = clone_result.value
        
        # 标记开始执行
        operation.start()
        
        # 检查是否有远程服务器配置
        base_url = self._get_base_url()
        
        if base_url:
            # 使用远程沙盒执行git clone命令
            client = self._get_remote_client()
            
            if not client:
                return Result.fail("无法连接到沙盒服务器")
            
            # 构建git clone命令
            clone_cmd = ["git", "clone"]
            if command.branch:
                clone_cmd.extend(["--branch", command.branch])
            if command.depth:
                clone_cmd.extend(["--depth", str(command.depth)])
            if command.recursive:
                clone_cmd.append("--recursive")
            clone_cmd.append(command.url)
            if command.target_dir:
                clone_cmd.append(command.target_dir)
            
            # 执行远程命令
            command_input = CommandInput(
                command="git",
                args=clone_cmd[1:],  # 去掉"git"，因为execute_command会添加
                working_directory=None,
            )
            
            try:
                command_output = client.execute_command(command_input)
                
                if command_output.exit_code == 0:
                    # 克隆成功
                    cloned_path = command.target_dir or command.url.split("/")[-1].replace(".git", "")
                    success_result = CloneResult.success(
                        message=f"成功克隆仓库到: {cloned_path}",
                        cloned_path=cloned_path,
                        remote_url=command.url,
                        branch=command.branch or "main",
                    )
                    operation.complete(success_result)
                    return Result.ok(success_result)
                else:
                    # 克隆失败
                    error_msg = command_output.stderr or "未知错误"
                    operation.fail(error_msg)
                    return Result.fail(f"克隆失败: {error_msg}")
            except Exception as e:
                operation.fail(str(e))
                return Result.fail(f"执行克隆命令失败: {str(e)}")
        else:
            # 没有配置base_url，无法执行远程命令
            operation.fail("No server address configured. Please configure sandbox server first.")
            return Result.fail("没有配置沙盒服务器地址，无法执行远程克隆命令")

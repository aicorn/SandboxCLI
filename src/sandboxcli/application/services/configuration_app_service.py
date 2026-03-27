"""配置应用服务"""
from typing import Optional

from ...domain.configuration import ConfigAggregate, ConfigService
from ...domain.configuration.value_objects import GitConfig
from ...domain.shared import Result
from ..commands.configuration import InteractiveConfigCommand, UpdateConfigCommand
from ..queries.configuration import GetConfigQuery


class ConfigurationAppService:
    """配置应用服务"""

    def __init__(self, config_aggregate: ConfigAggregate):
        self._config = config_aggregate
        self._git_config: Optional[GitConfig] = None
        # 从配置聚合中加载git_config
        self._load_git_config()

    def _load_git_config(self) -> None:
        """从配置聚合中加载Git配置"""
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
                    ssh_key=SSHKey(key_path=value.get("ssh_key", {}).get("key_path", "")) if value.get("ssh_key") else SSHKey(key_path=""),
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

    def get_config(self, query: GetConfigQuery) -> Result[dict]:
        """获取配置"""
        snapshot = self._config.create_snapshot()

        # 从items中提取git_config并提升到顶层
        if "items" in snapshot and snapshot["items"]:
            for item in snapshot["items"]:
                if item.get("key") == "git_config":
                    snapshot["git_config"] = item.get("value")
                    break
            # 提取git_config后移除items字段
            del snapshot["items"]

        # 处理敏感信息和简化输出
        if not query.include_sensitive:
            # 隐藏git_config中的敏感信息
            if "git_config" in snapshot and snapshot["git_config"]:
                git_cfg = snapshot["git_config"]
                if "credential" in git_cfg and git_cfg["credential"]:
                    git_cfg["credential"]["password"] = "***"
                if "ssh_key" in git_cfg and git_cfg["ssh_key"]:
                    if "key_content" in git_cfg["ssh_key"]:
                        git_cfg["ssh_key"]["key_content"] = "***"

        # 移除description字段以简化输出
        snapshot = self._remove_descriptions(snapshot)

        return Result.ok(snapshot)

    def _remove_descriptions(self, data: dict) -> dict:
        """递归移除字典中的description字段，并简化单键值对"""
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                if key == "description":
                    continue
                elif isinstance(value, (dict, list)):
                    result[key] = self._remove_descriptions(value)
                else:
                    result[key] = value
            # 简化单键值对：如果字典只有一个非description的键，直接返回其值
            if len(result) == 1:
                for key, value in result.items():
                    if isinstance(value, (dict, list)):
                        return self._remove_descriptions(value)
                    return value
            return result
        elif isinstance(data, list):
            return [self._remove_descriptions(item) for item in data]
        return data

    def get_git_config(self) -> Optional[GitConfig]:
        """获取Git配置"""
        return self._git_config

    def set_git_config(self, git_config: GitConfig) -> None:
        """设置Git配置"""
        self._git_config = git_config
        # 将Git配置保存到config_items中
        self._config.update_item("git_config", git_config.to_dict())

    def update_config(self, command: UpdateConfigCommand) -> Result[None]:
        """更新配置"""
        if command.has_base_url_update():
            result = ConfigService.update_base_url(self._config, command.base_url)
            if result.is_failure():
                return result
        
        if command.has_server_update():
            host = command.server_host or self._config.config.server_address.host if self._config.config.server_address else ""
            port = command.server_port or self._config.config.server_address.port if self._config.config.server_address else 22
            result = ConfigService.update_server_address(self._config, host, port)
            if result.is_failure():
                return result

        if command.has_username_update():
            result = ConfigService.update_username(self._config, command.username)
            if result.is_failure():
                return result

        if command.has_timeout_update():
            result = ConfigService.update_timeout(self._config, command.timeout)
            if result.is_failure():
                return result

        if command.has_working_directory_update():
            # 使用 ConfigAggregate 的方法更新工作目录，会触发事件
            self._config.update_working_directory(command.working_directory)

        if command.has_custom_config_update():
            self._config.update_item(command.config_key, command.config_value)

        return Result.ok(None)

    def validate_config(self) -> Result[bool]:
        """验证配置"""
        return ConfigService.validate_config(self._config)

    def interactive_config(self, command: InteractiveConfigCommand) -> Result[dict]:
        """交互式配置"""
        # 交互式配置的具体实现由CLI层处理
        return Result.ok(self._config.create_snapshot())

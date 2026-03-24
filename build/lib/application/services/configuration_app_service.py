"""配置应用服务"""
from ...domain.configuration import ConfigAggregate, ConfigService
from ...domain.shared import Result
from ..commands.configuration import InteractiveConfigCommand, UpdateConfigCommand
from ..queries.configuration import GetConfigQuery


class ConfigurationAppService:
    """配置应用服务"""

    def __init__(self, config_aggregate: ConfigAggregate):
        self._config = config_aggregate

    def get_config(self, query: GetConfigQuery) -> Result[dict]:
        """获取配置"""
        snapshot = self._config.create_snapshot()
        if not query.include_sensitive:
            # 移除敏感信息
            if "credential" in snapshot:
                snapshot["credential"] = "***"
        return Result.ok(snapshot)

    def update_config(self, command: UpdateConfigCommand) -> Result[None]:
        """更新配置"""
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

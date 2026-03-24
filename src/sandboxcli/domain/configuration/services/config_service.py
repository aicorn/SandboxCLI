"""配置领域服务"""
from typing import Optional

from ...shared import Result
from ..aggregates.config_aggregate import ConfigAggregate
from ..entities.config import Config
from ..value_objects import ServerAddress, Timeout


class ConfigService:
    """配置管理和验证服务"""

    @staticmethod
    def create_default_config() -> ConfigAggregate:
        """创建默认配置"""
        config = Config()
        return ConfigAggregate(config)

    @staticmethod
    def validate_server_address(host: str, port: int) -> Result[ServerAddress]:
        """验证并创建服务器地址"""
        try:
            address = ServerAddress(host=host, port=port)
            return Result.ok(address)
        except Exception as e:
            return Result.fail(f"Invalid server address: {str(e)}")

    @staticmethod
    def validate_timeout(seconds: int) -> Result[Timeout]:
        """验证并创建超时配置"""
        try:
            timeout = Timeout.from_seconds(seconds)
            return Result.ok(timeout)
        except Exception as e:
            return Result.fail(f"Invalid timeout: {str(e)}")

    @staticmethod
    def validate_username(username: str) -> Result[str]:
        """验证用户名"""
        if not username or not username.strip():
            return Result.fail("Username cannot be empty")
        return Result.ok(username.strip())

    @staticmethod
    def validate_config(config: ConfigAggregate) -> Result[bool]:
        """验证配置完整性"""
        if not config.config.server_address:
            return Result.fail("Server address is not configured")
        
        if not config.config.username:
            return Result.fail("Username is not configured")
        
        return Result.ok(True)

    @staticmethod
    def update_server_address(
        config: ConfigAggregate, host: str, port: int = 22
    ) -> Result[None]:
        """更新服务器地址"""
        validation_result = ConfigService.validate_server_address(host, port)
        if validation_result.is_failure():
            return Result.fail(validation_result.error)
        
        config.config.update_server_address(host, port)
        return Result.ok(None)

    @staticmethod
    def update_timeout(config: ConfigAggregate, seconds: int) -> Result[None]:
        """更新超时配置"""
        validation_result = ConfigService.validate_timeout(seconds)
        if validation_result.is_failure():
            return Result.fail(validation_result.error)
        
        config.config.update_timeout(seconds)
        return Result.ok(None)

    @staticmethod
    def update_username(config: ConfigAggregate, username: str) -> Result[None]:
        """更新用户名"""
        validation_result = ConfigService.validate_username(username)
        if validation_result.is_failure():
            return Result.fail(validation_result.error)
        
        config.config.update_username(username)
        return Result.ok(None)

    @staticmethod
    def update_base_url(config: ConfigAggregate, base_url: str) -> Result[None]:
        """更新 AIO Sandbox HTTP API 地址"""
        if not base_url or not base_url.strip():
            return Result.fail("Base URL cannot be empty")
        
        base_url = base_url.strip()
        # 验证 URL 格式
        if not base_url.startswith(("http://", "https://")):
            return Result.fail("Base URL must start with http:// or https://")
        
        config.config.update_server_address(host=None, port=8080, base_url=base_url)
        return Result.ok(None)

"""更新配置命令"""
from typing import Optional

from pydantic import BaseModel, Field


class UpdateConfigCommand(BaseModel):
    """更新配置命令"""
    config_id: str = "default"
    server_host: Optional[str] = None
    server_port: Optional[int] = None
    username: Optional[str] = None
    timeout: Optional[int] = None
    config_key: Optional[str] = None
    config_value: Optional[str] = None

    model_config = {"frozen": True}

    def has_server_update(self) -> bool:
        """判断是否有服务器配置更新"""
        return self.server_host is not None or self.server_port is not None

    def has_username_update(self) -> bool:
        """判断是否有用户名更新"""
        return self.username is not None

    def has_timeout_update(self) -> bool:
        """判断是否有超时更新"""
        return self.timeout is not None

    def has_custom_config_update(self) -> bool:
        """判断是否有自定义配置更新"""
        return self.config_key is not None and self.config_value is not None

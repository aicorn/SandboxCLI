"""服务器地址值对象"""
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator


class ServerAddress(BaseModel):
    """服务器地址值对象 - 支持 SSH 和 HTTP API 两种连接方式"""
    host: Optional[str] = None
    port: int = 22
    base_url: Optional[str] = None  # AIO Sandbox HTTP API 地址

    model_config = {"frozen": True}

    @field_validator("host")
    @classmethod
    def _validate_host(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Host cannot be empty")
        return v.strip() if v else v

    @field_validator("port")
    @classmethod
    def _validate_port(cls, v: int) -> int:
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v

    @field_validator("base_url")
    @classmethod
    def _validate_base_url(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Base URL cannot be empty")
        return v.strip() if v else v

    @model_validator(mode="before")
    @classmethod
    def _validate_connection_type(cls, data):
        """验证连接类型：SSH 或 HTTP API"""
        # 如果提供了 base_url，优先使用 HTTP API
        if isinstance(data, dict):
            base_url = data.get("base_url")
            host = data.get("host")

            if base_url and not host:
                # 使用 HTTP API 方式
                return data
            elif host and not base_url:
                # 使用 SSH 方式
                return data
            elif not host and not base_url:
                raise ValueError("Either host or base_url must be provided")
            else:
                raise ValueError("Cannot specify both host and base_url")
        return data

    def is_http_mode(self) -> bool:
        """是否使用 HTTP API 模式"""
        return self.base_url is not None

    def is_ssh_mode(self) -> bool:
        """是否使用 SSH 模式"""
        return self.host is not None and self.base_url is None

    def __str__(self) -> str:
        if self.base_url:
            return self.base_url
        return f"{self.host}:{self.port}"

    def __repr__(self) -> str:
        if self.base_url:
            return f"ServerAddress(base_url='{self.base_url}')"
        return f"ServerAddress(host='{self.host}', port={self.port})"

    def to_dict(self) -> dict:
        """转换为字典"""
        result = {}
        if self.host:
            result["host"] = self.host
        if self.port != 22:
            result["port"] = self.port
        if self.base_url:
            result["base_url"] = self.base_url
        return result

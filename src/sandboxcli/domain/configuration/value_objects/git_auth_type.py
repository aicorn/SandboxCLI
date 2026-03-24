"""Git认证方式值对象"""
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class GitAuthTypeEnum(str, Enum):
    """Git认证方式枚举"""
    NONE = "none"      # 无认证
    HTTPS = "https"    # HTTPS用户名密码
    SSH = "ssh"        # SSH密钥


class GitAuthType(BaseModel):
    """Git认证方式值对象
    
    用于描述Git操作的认证方式。
    """
    auth_type: GitAuthTypeEnum = GitAuthTypeEnum.NONE
    description: Optional[str] = None
    
    model_config = {"frozen": True}
    
    @field_validator("auth_type", mode="before")
    @classmethod
    def _normalize_auth_type(cls, v):
        """标准化认证类型值"""
        if isinstance(v, str):
            return v.lower()
        return v
    
    def is_none(self) -> bool:
        """是否无需认证"""
        return self.auth_type == GitAuthTypeEnum.NONE
    
    def is_https(self) -> bool:
        """是否使用HTTPS认证"""
        return self.auth_type == GitAuthTypeEnum.HTTPS
    
    def is_ssh(self) -> bool:
        """是否使用SSH认证"""
        return self.auth_type == GitAuthTypeEnum.SSH
    
    @staticmethod
    def none() -> "GitAuthType":
        """无需认证"""
        return GitAuthType(auth_type=GitAuthTypeEnum.NONE, description="无认证")
    
    @staticmethod
    def https() -> "GitAuthType":
        """HTTPS认证"""
        return GitAuthType(auth_type=GitAuthTypeEnum.HTTPS, description="HTTPS用户名密码认证")
    
    @staticmethod
    def ssh() -> "GitAuthType":
        """SSH认证"""
        return GitAuthType(auth_type=GitAuthTypeEnum.SSH, description="SSH密钥认证")
    
    def __str__(self) -> str:
        return self.auth_type.value
    
    def __repr__(self) -> str:
        return f"GitAuthType(auth_type={self.auth_type.value})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "auth_type": self.auth_type.value,
            "description": self.description,
        }

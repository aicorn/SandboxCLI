"""沙盒类型值对象"""
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class SandboxTypeEnum(str, Enum):
    """沙盒类型枚举"""
    AIO = "aio"  # AIO Sandbox (HTTP API)
    SSH = "ssh"  # SSH 连接
    CUSTOM = "custom"  # 自定义沙盒


class SandboxType(BaseModel):
    """沙盒类型值对象
    
    用于描述使用的沙盒类型，控制指令调用基础设施层中哪个部分的代码。
    例如：使用 AIO Sandbox 还是 SSH 沙盒。
    """
    type: SandboxTypeEnum = SandboxTypeEnum.AIO
    description: Optional[str] = None
    
    model_config = {"frozen": True}
    
    @field_validator("type", mode="before")
    @classmethod
    def _normalize_type(cls, v):
        """标准化类型值"""
        if isinstance(v, str):
            return v.lower()
        return v
    
    def is_aio(self) -> bool:
        """是否为 AIO 沙盒"""
        return self.type == SandboxTypeEnum.AIO
    
    def is_ssh(self) -> bool:
        """是否为 SSH 沙盒"""
        return self.type == SandboxTypeEnum.SSH
    
    def is_custom(self) -> bool:
        """是否为自定义沙盒"""
        return self.type == SandboxTypeEnum.CUSTOM
    
    @staticmethod
    def default_aio() -> "SandboxType":
        """默认 AIO 沙盒类型"""
        return SandboxType(type=SandboxTypeEnum.AIO, description="AIO Sandbox (HTTP API)")
    
    @staticmethod
    def default_ssh() -> "SandboxType":
        """默认 SSH 沙盒类型"""
        return SandboxType(type=SandboxTypeEnum.SSH, description="SSH 连接")
    
    def __str__(self) -> str:
        return self.type.value
    
    def __repr__(self) -> str:
        return f"SandboxType(type={self.type.value})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "type": self.type.value,
            "description": self.description,
        }
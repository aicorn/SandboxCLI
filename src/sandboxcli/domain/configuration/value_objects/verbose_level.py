"""Verbose调试级别值对象"""
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class VerboseLevelEnum(str, Enum):
    """Verbose调试级别枚举"""
    OFF = "off"      # 关闭：不输出任何调试信息
    ERROR = "error"  # 错误：仅输出错误信息
    INFO = "info"    # 信息：输出常规调试信息
    DEBUG = "debug"  # 调试：输出详细调试信息（包括通信过程）


class VerboseLevel(BaseModel):
    """Verbose调试级别值对象
    
    用于控制调试信息的输出级别。
    """
    level: VerboseLevelEnum = VerboseLevelEnum.OFF
    description: Optional[str] = None
    
    model_config = {"frozen": True}
    
    @field_validator("level", mode="before")
    @classmethod
    def _normalize_level(cls, v):
        """标准化级别值"""
        if isinstance(v, str):
            return v.lower()
        return v
    
    def is_off(self) -> bool:
        """是否关闭"""
        return self.level == VerboseLevelEnum.OFF
    
    def is_error(self) -> bool:
        """是否仅输出错误"""
        return self.level == VerboseLevelEnum.ERROR
    
    def is_info(self) -> bool:
        """是否输出信息"""
        return self.level == VerboseLevelEnum.INFO
    
    def is_debug(self) -> bool:
        """是否输出调试信息"""
        return self.level == VerboseLevelEnum.DEBUG
    
    @staticmethod
    def off() -> "VerboseLevel":
        """关闭调试输出"""
        return VerboseLevel(level=VerboseLevelEnum.OFF, description="关闭调试输出")
    
    @staticmethod
    def error() -> "VerboseLevel":
        """仅输出错误信息"""
        return VerboseLevel(level=VerboseLevelEnum.ERROR, description="仅输出错误信息")
    
    @staticmethod
    def info() -> "VerboseLevel":
        """输出常规调试信息"""
        return VerboseLevel(level=VerboseLevelEnum.INFO, description="输出常规调试信息")
    
    @staticmethod
    def debug() -> "VerboseLevel":
        """输出详细调试信息"""
        return VerboseLevel(level=VerboseLevelEnum.DEBUG, description="输出详细调试信息")
    
    def __str__(self) -> str:
        return self.level.value
    
    def __repr__(self) -> str:
        return f"VerboseLevel(level={self.level.value})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "level": self.level.value,
            "description": self.description,
        }

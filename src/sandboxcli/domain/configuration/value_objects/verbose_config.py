"""Verbose调试配置值对象"""
from typing import Optional

from pydantic import BaseModel, field_validator

from .verbose_level import VerboseLevel, VerboseLevelEnum


class VerboseConfig(BaseModel):
    """Verbose调试配置值对象
    
    用于控制调试信息的输出级别、格式等配置。
    默认值为关闭状态（OFF级别）。
    """
    level: VerboseLevelEnum = VerboseLevelEnum.OFF
    enable_timestamp: bool = True
    enable_color: bool = True
    
    model_config = {"frozen": True}
    
    @field_validator("level", mode="before")
    @classmethod
    def _normalize_level(cls, v):
        """标准化级别值"""
        if isinstance(v, str):
            return v.lower()
        return v
    
    @classmethod
    def default(cls) -> "VerboseConfig":
        """创建默认Verbose配置（关闭状态）"""
        return cls(
            level=VerboseLevelEnum.OFF,
            enable_timestamp=True,
            enable_color=True
        )
    
    @classmethod
    def from_level(cls, level: VerboseLevelEnum) -> "VerboseConfig":
        """从级别创建配置"""
        return cls(level=level)
    
    @classmethod
    def from_dict(cls, data: dict) -> "VerboseConfig":
        """从字典创建配置"""
        return cls(
            level=data.get("level", VerboseLevelEnum.OFF),
            enable_timestamp=data.get("enable_timestamp", True),
            enable_color=data.get("enable_color", True)
        )
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "level": self.level.value,
            "enable_timestamp": self.enable_timestamp,
            "enable_color": self.enable_color
        }
    
    def to_verbose_level(self) -> VerboseLevel:
        """转换为 VerboseLevel 对象"""
        return VerboseLevel(level=self.level)
    
    def is_enabled(self) -> bool:
        """是否启用（级别高于OFF）"""
        return self.level != VerboseLevelEnum.OFF
    
    def __str__(self) -> str:
        return f"VerboseConfig(level={self.level.value})"
    
    def __repr__(self) -> str:
        return f"VerboseConfig(level={self.level.value}, enable_timestamp={self.enable_timestamp}, enable_color={self.enable_color})"

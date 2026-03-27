"""工作目录值对象"""
from typing import Optional

from pydantic import BaseModel, field_validator


class WorkingDirectory(BaseModel):
    """工作目录配置值对象
    
    用于统一管理Git操作和命令执行的工作目录基准目录。
    默认值为 "."（当前目录）。
    """
    path: str = "."
    isDefault: bool = True

    model_config = {"frozen": True}

    @field_validator("path")
    @classmethod
    def _validate_path(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Working directory path cannot be empty")
        # 移除末尾的斜杠，保持路径一致性
        v = v.rstrip("/\\")
        if not v:
            v = "."
        return v

    @classmethod
    def default(cls) -> "WorkingDirectory":
        """创建默认工作目录配置"""
        return cls(path=".", isDefault=True)

    @classmethod
    def from_path(cls, path: str) -> "WorkingDirectory":
        """从路径创建工作目录配置
        
        Args:
            path: 工作目录路径
            
        Returns:
            WorkingDirectory 实例，isDefault 设为 False
        """
        return cls(path=path, isDefault=False)

    def __str__(self) -> str:
        return self.path

    def __repr__(self) -> str:
        return f"WorkingDirectory(path={self.path!r}, isDefault={self.isDefault})"

    def to_dict(self) -> dict:
        """转换为字典"""
        return {"path": self.path, "isDefault": self.isDefault}

    @classmethod
    def from_dict(cls, data: dict) -> "WorkingDirectory":
        """从字典创建"""
        return cls(
            path=data.get("path", "."),
            isDefault=data.get("isDefault", True)
        )
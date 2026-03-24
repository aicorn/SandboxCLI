"""Git凭据值对象"""
from typing import Optional

from pydantic import BaseModel, field_validator


class GitCredential(BaseModel):
    """Git凭据值对象
    
    用于描述Git操作所需的用户凭据信息。
    包括用户名和邮箱。
    """
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None  # HTTPS认证时使用
    description: Optional[str] = None
    
    model_config = {"frozen": True}
    
    @field_validator("username", "email", mode="before")
    @classmethod
    def _normalize_field(cls, v):
        """标准化字段"""
        if v is None:
            return None
        return v.strip()
    
    def is_empty(self) -> bool:
        """是否为空（未设置）"""
        return not bool(self.username) and not bool(self.email)
    
    def has_password(self) -> bool:
        """是否设置了密码"""
        return bool(self.password)
    
    def __str__(self) -> str:
        return f"GitCredential(username={self.username}, email={self.email})"
    
    def __repr__(self) -> str:
        return f"GitCredential(username={self.username}, email={self.email}, has_password={self.has_password()})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "username": self.username,
            "email": self.email,
            "has_password": self.has_password(),
            "description": self.description,
        }
    
    @staticmethod
    def empty() -> "GitCredential":
        """创建空凭据"""
        return GitCredential(description="未设置Git凭据")
    
    @staticmethod
    def create(username: str, email: str, password: Optional[str] = None) -> "GitCredential":
        """创建Git凭据"""
        return GitCredential(
            username=username,
            email=email,
            password=password,
            description=f"Git凭据: {username}"
        )

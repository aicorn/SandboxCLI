"""SSH密钥值对象"""
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, field_validator


class SSHKey(BaseModel):
    """SSH密钥值对象
    
    用于描述SSH认证所需的私钥。
    支持两种方式：密钥内容或密钥文件路径。
    """
    key_path: Optional[str] = None      # SSH密钥文件路径
    key_content: Optional[str] = None   # SSH密钥内容（Base64编码或直接内容）
    passphrase: Optional[str] = None    # 密钥 passphrase（可选）
    description: Optional[str] = None
    
    model_config = {"frozen": True}
    
    @field_validator("key_path", mode="before")
    @classmethod
    def _normalize_key_path(cls, v):
        """标准化密钥路径"""
        if v is None:
            return None
        return v.strip()
    
    def is_empty(self) -> bool:
        """是否为空（未设置）"""
        return not bool(self.key_path) and not bool(self.key_content)
    
    def has_passphrase(self) -> bool:
        """是否设置了 passphrase"""
        return bool(self.passphrase)
    
    def get_key_source(self) -> str:
        """获取密钥来源类型"""
        if self.key_content:
            return "content"
        elif self.key_path:
            return "path"
        return "none"
    
    def resolve_key_path(self) -> Optional[Path]:
        """解析密钥文件路径"""
        if self.key_path:
            return Path(self.key_path)
        return None
    
    def __str__(self) -> str:
        if self.key_path:
            return f"SSHKey(path={self.key_path})"
        elif self.key_content:
            return "SSHKey(content=***)"
        return "SSHKey(empty)"
    
    def __repr__(self) -> str:
        return f"SSHKey(key_path={self.key_path}, has_content={bool(self.key_content)})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "key_path": self.key_path,
            "key_content": "***" if self.key_content else None,
            "has_passphrase": self.has_passphrase(),
            "description": self.description,
        }
    
    @staticmethod
    def empty() -> "SSHKey":
        """创建空SSH密钥"""
        return SSHKey(description="未设置SSH密钥")
    
    @staticmethod
    def from_path(path: str, passphrase: Optional[str] = None) -> "SSHKey":
        """从路径创建SSH密钥"""
        return SSHKey(
            key_path=path,
            passphrase=passphrase,
            description=f"SSH密钥: {path}"
        )
    
    @staticmethod
    def from_content(content: str, passphrase: Optional[str] = None) -> "SSHKey":
        """从内容创建SSH密钥"""
        return SSHKey(
            key_content=content,
            passphrase=passphrase,
            description="SSH密钥(内联)"
        )

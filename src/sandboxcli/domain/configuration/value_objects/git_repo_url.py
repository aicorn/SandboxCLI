"""Git仓库URL值对象"""
from typing import Optional

from pydantic import BaseModel, field_validator


class GitRepoUrl(BaseModel):
    """Git仓库URL值对象
    
    用于描述远程Git仓库的URL地址。
    支持HTTP、HTTPS、SSH协议。
    """
    url: str
    description: Optional[str] = None
    
    model_config = {"frozen": True}
    
    @field_validator("url", mode="before")
    @classmethod
    def _normalize_url(cls, v):
        """标准化URL"""
        if v is None:
            return ""
        return v.strip()
    
    def is_empty(self) -> bool:
        """是否为空URL"""
        return not bool(self.url)
    
    def is_https(self) -> bool:
        """是否HTTPS协议"""
        return self.url.startswith("https://")
    
    def is_http(self) -> bool:
        """是否HTTP协议"""
        return self.url.startswith("http://")
    
    def is_ssh(self) -> bool:
        """是否SSH协议"""
        return self.url.startswith("git@") or self.url.endswith(".git")
    
    def get_repo_name(self) -> Optional[str]:
        """获取仓库名称"""
        if not self.url:
            return None
        # 从URL中提取仓库名
        parts = self.url.rstrip("/").split("/")
        if parts:
            repo = parts[-1]
            if repo.endswith(".git"):
                return repo[:-4]
            return repo
        return None
    
    def __str__(self) -> str:
        return self.url
    
    def __repr__(self) -> str:
        return f"GitRepoUrl(url={self.url})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "url": self.url,
            "description": self.description,
        }
    
    @staticmethod
    def empty() -> "GitRepoUrl":
        """创建空URL"""
        return GitRepoUrl(url="", description="未设置")

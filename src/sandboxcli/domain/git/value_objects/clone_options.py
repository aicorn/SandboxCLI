"""Git克隆选项值对象"""
from typing import List, Optional

from pydantic import BaseModel, field_validator


class CloneOptions(BaseModel):
    """Git克隆选项值对象
    
    用于描述Git克隆操作的配置选项。
    """
    url: str                           # 远程仓库URL
    target_dir: Optional[str] = None   # 目标目录
    branch: Optional[str] = None       # 指定分支
    depth: Optional[int] = None        # 浅克隆深度
    recursive: bool = False           # 是否递归克隆子模块
    working_directory: str = "."      # 工作目录（用于确定克隆时的基准目录）
    description: Optional[str] = None
    
    model_config = {"frozen": True}
    
    @field_validator("url", mode="before")
    @classmethod
    def _normalize_url(cls, v):
        """标准化URL"""
        if v is None:
            return ""
        return v.strip()
    
    @field_validator("target_dir", mode="before")
    @classmethod
    def _normalize_target_dir(cls, v):
        """标准化目标目录"""
        if v is None:
            return None
        return v.strip()
    
    @field_validator("branch", mode="before")
    @classmethod
    def _normalize_branch(cls, v):
        """标准化分支名"""
        if v is None:
            return None
        return v.strip()
    
    def is_shallow_clone(self) -> bool:
        """是否为浅克隆"""
        return self.depth is not None and self.depth > 0
    
    def get_git_args(self) -> List[str]:
        """获取git clone命令参数列表"""
        args = []
        
        if self.depth is not None and self.depth > 0:
            args.extend(["--depth", str(self.depth)])
        
        if self.branch:
            args.extend(["--branch", self.branch])
        
        if self.recursive:
            args.append("--recursive")
        
        args.append(self.url)
        
        if self.target_dir:
            args.append(self.target_dir)
        
        return args
    
    def __str__(self) -> str:
        return f"CloneOptions(url={self.url}, branch={self.branch}, depth={self.depth})"
    
    def __repr__(self) -> str:
        return f"CloneOptions(url={self.url}, target_dir={self.target_dir}, branch={self.branch}, depth={self.depth}, recursive={self.recursive})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "url": self.url,
            "target_dir": self.target_dir,
            "branch": self.branch,
            "depth": self.depth,
            "recursive": self.recursive,
            "working_directory": self.working_directory,
            "description": self.description,
        }
    
    @staticmethod
    def create(url: str, **kwargs) -> "CloneOptions":
        """创建克隆选项"""
        return CloneOptions(url=url, **kwargs)

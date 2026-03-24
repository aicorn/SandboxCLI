"""克隆仓库命令"""
from typing import Optional

from pydantic import BaseModel, Field


class CloneRepositoryCommand(BaseModel):
    """克隆仓库命令
    
    用于执行Git仓库克隆操作的应用层命令。
    """
    url: str = Field(..., description="远程仓库URL")
    target_dir: Optional[str] = Field(None, description="目标目录")
    branch: Optional[str] = Field(None, description="指定分支")
    depth: Optional[int] = Field(None, description="浅克隆深度")
    recursive: bool = Field(False, description="是否递归克隆子模块")
    use_config_git: bool = Field(True, description="是否使用配置中的Git凭据")
    
    model_config = {"frozen": True}
    
    @property
    def has_depth(self) -> bool:
        """是否指定了浅克隆"""
        return self.depth is not None and self.depth > 0
    
    @property
    def is_shallow_clone(self) -> bool:
        """是否为浅克隆"""
        return self.has_depth
    
    def __str__(self) -> str:
        return f"CloneRepositoryCommand(url={self.url}, branch={self.branch}, depth={self.depth})"
    
    def __repr__(self) -> str:
        return f"CloneRepositoryCommand(url={self.url}, target_dir={self.target_dir}, branch={self.branch}, depth={self.depth}, recursive={self.recursive})"

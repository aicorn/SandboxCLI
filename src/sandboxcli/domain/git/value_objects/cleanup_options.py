"""Git清理选项值对象"""
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class CleanupType(str, Enum):
    """Git清理类型枚举"""
    CLEAN_WORKSPACE = "workspace"    # 清理工作区（删除未跟踪文件）
    CLEAN_BRANCHES = "branches"       # 清理已合并的本地分支
    CLEAN_TAGS = "tags"               # 清理本地标签
    CLEAN_ALL = "all"                 # 清理所有（工作区+分支+标签）


class CleanupOptions(BaseModel):
    """Git清理选项值对象
    
    用于描述Git仓库清理操作的配置选项。
    """
    cleanup_type: CleanupType = CleanupType.CLEAN_WORKSPACE  # 清理类型
    force: bool = False                                           # 是否强制执行（跳过确认）
    repo_path: str = "."                                           # 仓库路径（可选，默认当前目录）
    description: Optional[str] = None
    
    model_config = {"frozen": True}
    
    @field_validator("repo_path", mode="before")
    @classmethod
    def _normalize_repo_path(cls, v):
        """标准化仓库路径"""
        if v is None:
            return "."
        return v.strip() if v.strip() else "."
    
    def is_force(self) -> bool:
        """是否为强制执行"""
        return self.force
    
    def is_clean_workspace(self) -> bool:
        """是否清理工作区"""
        return self.cleanup_type in [CleanupType.CLEAN_WORKSPACE, CleanupType.CLEAN_ALL]
    
    def is_clean_branches(self) -> bool:
        """是否清理分支"""
        return self.cleanup_type in [CleanupType.CLEAN_BRANCHES, CleanupType.CLEAN_ALL]
    
    def is_clean_tags(self) -> bool:
        """是否清理标签"""
        return self.cleanup_type in [CleanupType.CLEAN_TAGS, CleanupType.CLEAN_ALL]
    
    def get_git_clean_args(self) -> list:
        """获取git clean命令参数列表"""
        args = ["git", "-C", self.repo_path, "clean"]
        
        if self.force:
            args.append("-f")
        
        # 删除目录
        args.append("-d")
        
        return args
    
    def get_git_branch_delete_args(self) -> list:
        """获取删除已合并分支的命令参数列表"""
        # 获取已合并的分支（排除main和当前分支）
        return ["git", "-C", self.repo_path, "branch", "--merged"]
    
    def __str__(self) -> str:
        return f"CleanupOptions(type={self.cleanup_type}, force={self.force}, repo_path={self.repo_path})"
    
    def __repr__(self) -> str:
        return f"CleanupOptions(cleanup_type={self.cleanup_type}, force={self.force}, repo_path={self.repo_path})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "cleanup_type": self.cleanup_type.value,
            "force": self.force,
            "repo_path": self.repo_path,
            "description": self.description,
        }
    
    @staticmethod
    def create(cleanup_type: CleanupType = CleanupType.CLEAN_WORKSPACE, 
              force: bool = False, 
              repo_path: str = ".",
              **kwargs) -> "CleanupOptions":
        """创建清理选项"""
        return CleanupOptions(
            cleanup_type=cleanup_type,
            force=force,
            repo_path=repo_path,
            **kwargs
        )
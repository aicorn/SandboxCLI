"""清理仓库命令"""
from typing import Optional

from pydantic import BaseModel, Field

from sandboxcli.domain.git.value_objects import CleanupType


class CleanRepositoryCommand(BaseModel):
    """清理仓库命令
    
    用于执行Git仓库清理操作的应用层命令。
    """
    cleanup_type: CleanupType = Field(CleanupType.CLEAN_WORKSPACE, description="清理类型")
    force: bool = Field(False, description="是否强制执行（跳过确认）")
    repo_path: str = Field(".", description="仓库路径")
    
    model_config = {"frozen": True}
    
    @property
    def is_workspace_cleanup(self) -> bool:
        """是否清理工作区"""
        return self.cleanup_type in [CleanupType.CLEAN_WORKSPACE, CleanupType.CLEAN_ALL]
    
    @property
    def is_branches_cleanup(self) -> bool:
        """是否清理分支"""
        return self.cleanup_type in [CleanupType.CLEAN_BRANCHES, CleanupType.CLEAN_ALL]
    
    @property
    def is_tags_cleanup(self) -> bool:
        """是否清理标签"""
        return self.cleanup_type in [CleanupType.CLEAN_TAGS, CleanupType.CLEAN_ALL]
    
    @property
    def is_workspace_clean(self) -> bool:
        """是否清理工作区（别名）"""
        return self.is_workspace_cleanup
    
    @property
    def is_all_cleanup(self) -> bool:
        """是否清理所有"""
        return self.cleanup_type == CleanupType.CLEAN_ALL
    
    def __str__(self) -> str:
        return f"CleanRepositoryCommand(type={self.cleanup_type}, force={self.force}, repo_path={self.repo_path})"
    
    def __repr__(self) -> str:
        return f"CleanRepositoryCommand(cleanup_type={self.cleanup_type}, force={self.force}, repo_path={self.repo_path})"
"""Git清理结果值对象"""
from typing import List, Optional

from pydantic import BaseModel


class CleanupResult(BaseModel):
    """Git清理结果值对象
    
    用于描述Git仓库清理操作的结果。
    """
    success: bool                                      # 是否成功
    message: str                                       # 结果消息
    cleaned_files: List[str] = []                     # 已清理的文件列表
    deleted_branches: List[str] = []                  # 已删除的分支列表
    deleted_tags: List[str] = []                      # 已删除的标签列表
    error: Optional[str] = None                       # 错误信息（失败时）
    
    model_config = {"frozen": True}
    
    def is_success(self) -> bool:
        """是否成功"""
        return self.success
    
    def is_failed(self) -> bool:
        """是否失败"""
        return not self.success
    
    def has_cleaned_files(self) -> bool:
        """是否有清理的文件"""
        return len(self.cleaned_files) > 0
    
    def has_deleted_branches(self) -> bool:
        """是否有删除的分支"""
        return len(self.deleted_branches) > 0
    
    def has_deleted_tags(self) -> bool:
        """是否有删除的标签"""
        return len(self.deleted_tags) > 0
    
    def get_total_cleaned(self) -> int:
        """获取总共清理的项目数"""
        return len(self.cleaned_files) + len(self.deleted_branches) + len(self.deleted_tags)
    
    def __str__(self) -> str:
        if self.success:
            return f"CleanupResult(success=True, cleaned={self.get_total_cleaned()})"
        return f"CleanupResult(success=False, message={self.message})"
    
    def __repr__(self) -> str:
        return f"CleanupResult(success={self.success}, message={self.message}, cleaned_files={len(self.cleaned_files)}, deleted_branches={len(self.deleted_branches)}, deleted_tags={len(self.deleted_tags)})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "success": self.success,
            "message": self.message,
            "cleaned_files": self.cleaned_files,
            "deleted_branches": self.deleted_branches,
            "deleted_tags": self.deleted_tags,
            "error": self.error,
        }
    
    @staticmethod
    def success(
        message: str,
        cleaned_files: List[str] = None,
        deleted_branches: List[str] = None,
        deleted_tags: List[str] = None,
    ) -> "CleanupResult":
        """创建成功结果"""
        return CleanupResult(
            success=True,
            message=message,
            cleaned_files=cleaned_files or [],
            deleted_branches=deleted_branches or [],
            deleted_tags=deleted_tags or [],
        )
    
    @staticmethod
    def failed(message: str, error: Optional[str] = None) -> "CleanupResult":
        """创建失败结果"""
        return CleanupResult(
            success=False,
            message=message,
            error=error,
        )
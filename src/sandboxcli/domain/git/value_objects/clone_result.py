"""Git克隆结果值对象"""
from typing import Optional

from pydantic import BaseModel


class CloneResult(BaseModel):
    """Git克隆结果值对象
    
    用于描述Git克隆操作的结果。
    """
    success: bool                        # 是否成功
    message: str                         # 结果消息
    cloned_path: Optional[str] = None   # 克隆到的本地路径
    commit_hash: Optional[str] = None   # 最新提交哈希（成功时）
    branch: Optional[str] = None        # 当前分支
    remote_url: Optional[str] = None   # 远程仓库URL
    error: Optional[str] = None         # 错误信息（失败时）
    
    model_config = {"frozen": True}
    
    def is_success(self) -> bool:
        """是否成功"""
        return self.success
    
    def is_failed(self) -> bool:
        """是否失败"""
        return not self.success
    
    def __str__(self) -> str:
        if self.success:
            return f"CloneResult(success=True, path={self.cloned_path})"
        return f"CloneResult(success=False, message={self.message})"
    
    def __repr__(self) -> str:
        return f"CloneResult(success={self.success}, message={self.message}, cloned_path={self.cloned_path}, commit_hash={self.commit_hash})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "success": self.success,
            "message": self.message,
            "cloned_path": self.cloned_path,
            "commit_hash": self.commit_hash,
            "branch": self.branch,
            "remote_url": self.remote_url,
            "error": self.error,
        }
    
    @staticmethod
    def success(
        message: str,
        cloned_path: str,
        commit_hash: Optional[str] = None,
        branch: Optional[str] = None,
        remote_url: Optional[str] = None,
    ) -> "CloneResult":
        """创建成功结果"""
        return CloneResult(
            success=True,
            message=message,
            cloned_path=cloned_path,
            commit_hash=commit_hash,
            branch=branch,
            remote_url=remote_url,
        )
    
    @staticmethod
    def failed(message: str, error: Optional[str] = None) -> "CloneResult":
        """创建失败结果"""
        return CloneResult(
            success=False,
            message=message,
            error=error,
        )

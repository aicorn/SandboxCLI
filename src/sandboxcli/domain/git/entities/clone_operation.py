"""Git克隆操作实体"""
from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, Field

from ..value_objects import CloneOptions, CloneResult


class CloneOperation(BaseModel):
    """Git克隆操作实体
    
    用于跟踪Git仓库克隆操作的状态和结果。
    这是一个聚合根，包含克隆操作的所有相关信息。
    """
    operation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    options: CloneOptions
    result: Optional[CloneResult] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = "pending"  # pending, running, success, failed
    
    model_config = {"frozen": False}  # Allow mutation for status updates
    
    def start(self) -> None:
        """开始克隆操作"""
        self.status = "running"
        self.started_at = datetime.utcnow()
    
    def complete(self, result: CloneResult) -> None:
        """完成克隆操作"""
        self.result = result
        self.status = "success" if result.success else "failed"
        self.completed_at = datetime.utcnow()
    
    def fail(self, error: str) -> None:
        """克隆操作失败"""
        self.result = CloneResult.failed(message=error, error=error)
        self.status = "failed"
        self.completed_at = datetime.utcnow()
    
    @property
    def is_running(self) -> bool:
        """是否正在运行"""
        return self.status == "running"
    
    @property
    def is_success(self) -> bool:
        """是否成功"""
        return self.status == "success"
    
    @property
    def is_failed(self) -> bool:
        """是否失败"""
        return self.status == "failed"
    
    @property
    def is_pending(self) -> bool:
        """是否等待中"""
        return self.status == "pending"
    
    @property
    def is_completed(self) -> bool:
        """是否已完成"""
        return self.status in ("success", "failed")
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """获取操作耗时（秒）"""
        if self.started_at and self.completed_at:
            delta = self.completed_at - self.started_at
            return delta.total_seconds()
        return None
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "operation_id": self.operation_id,
            "options": self.options.to_dict(),
            "result": self.result.to_dict() if self.result else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "status": self.status,
            "duration_seconds": self.duration_seconds,
        }
    
    @staticmethod
    def create(options: CloneOptions) -> "CloneOperation":
        """创建新的克隆操作"""
        return CloneOperation(
            operation_id=str(uuid.uuid4()),
            options=options,
            status="pending",
        )

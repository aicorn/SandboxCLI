"""工作目录变更事件"""
from datetime import datetime, timezone
from typing import Optional

from pydantic import Field, model_validator

from ...shared.events.domain_event import DomainEvent


class WorkingDirectoryChangedEvent(DomainEvent):
    """工作目录变更事件
    
    当配置中的工作目录被修改时触发此事件。
    """
    old_path: str = Field(default=".")
    new_path: str = Field(default=".")
    changed_by: str = "user"  # user/system

    @model_validator(mode='before')
    @classmethod
    def _skip_parent_validation(cls, data):
        """跳过父类验证，直接使用传入的数据"""
        # 让 Pydantic 正常处理字段验证
        return data

    @classmethod
    def create(
        cls,
        old_path: str,
        new_path: str,
        changed_by: str = "user"
    ) -> "WorkingDirectoryChangedEvent":
        """创建工作目录变更事件
        
        Args:
            old_path: 旧的工作目录路径
            new_path: 新的工作目录路径
            changed_by: 变更操作者 (user/system)
            
        Returns:
            WorkingDirectoryChangedEvent 实例
        """
        return cls(
            old_path=old_path,
            new_path=new_path,
            changed_by=changed_by
        )

    def get_event_type(self) -> str:
        """获取事件类型"""
        return "WorkingDirectoryChangedEvent"

    def get_aggregate_id(self) -> str:
        """获取聚合根ID"""
        return "config"

    @property
    def has_changed(self) -> bool:
        """工作目录是否真正发生变化"""
        return self.old_path != self.new_path

    def get_change_message(self) -> str:
        """获取变更消息"""
        if self.has_changed:
            return f"工作目录已从 {self.old_path} 变更为 {self.new_path}"
        return "工作目录未发生变化"

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "event_type": self.get_event_type(),
            "event_id": self.event_id,
            "occurred_on": self.occurred_on.isoformat(),
            "old_path": self.old_path,
            "new_path": self.new_path,
            "changed_by": self.changed_by,
        }
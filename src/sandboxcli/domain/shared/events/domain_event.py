"""领域事件基类"""
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict

from pydantic import BaseModel, Field


class DomainEvent(BaseModel, ABC):
    """领域事件基类"""
    event_id: str = Field(default_factory=lambda: str(datetime.now(timezone.utc).timestamp()))
    occurred_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: str = ""

    model_config = {"frozen": True}

    @abstractmethod
    def get_event_type(self) -> str:
        """获取事件类型"""
        pass

    @abstractmethod
    def get_aggregate_id(self) -> str:
        """获取聚合根ID"""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.model_dump()

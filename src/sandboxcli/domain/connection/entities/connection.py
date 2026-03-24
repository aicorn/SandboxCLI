"""连接实体"""
import uuid
from typing import Optional

from pydantic import BaseModel, Field

from ...shared import Timestamp
from ..value_objects import AuthCredential, ConnectionConfig, ConnectionStatus


class Connection(BaseModel):
    """连接会话实体"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    config: ConnectionConfig
    credential: Optional[AuthCredential] = None
    status: ConnectionStatus = Field(default_factory=ConnectionStatus)
    connected_at: Optional[Timestamp] = None
    disconnected_at: Optional[Timestamp] = None

    model_config = {"frozen": False}

    @classmethod
    def create(cls, config: ConnectionConfig, credential: AuthCredential = None) -> "Connection":
        """创建连接"""
        return cls(config=config, credential=credential)

    @property
    def session_id(self) -> str:
        """获取会话ID"""
        return self.id

    def connect(self) -> None:
        """连接"""
        self.status = self.status.mark_connected("Connected")
        self.connected_at = Timestamp.now()
        self.disconnected_at = None

    def disconnect(self) -> None:
        """断开连接"""
        self.status = self.status.mark_disconnected("Disconnected")
        self.disconnected_at = Timestamp.now()

    def set_error(self, message: str) -> None:
        """设置错误"""
        self.status = self.status.mark_error(message)

    def set_connecting(self, message: str = "Connecting...") -> None:
        """设置正在连接"""
        self.status = self.status.mark_connecting(message)

    def get_duration(self) -> Optional[float]:
        """获取连接时长（秒）"""
        if self.connected_at:
            end_time = self.disconnected_at.value if self.disconnected_at else Timestamp.now().value
            return (end_time - self.connected_at.value).total_seconds()
        return None

    def __str__(self) -> str:
        return f"Connection(id='{self.id}', status='{self.status}', config={self.config})"

    def __repr__(self) -> str:
        return f"Connection(id='{self.id}', status={self.status}, config={self.config})"

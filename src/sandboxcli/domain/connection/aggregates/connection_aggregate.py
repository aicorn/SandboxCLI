"""连接聚合"""
from typing import Optional

from ..entities import Connection
from ..value_objects import AuthCredential, ConnectionConfig, ConnectionStatus


class ConnectionAggregate:
    """连接聚合根"""

    def __init__(self, connection: Connection):
        self._connection = connection

    @property
    def connection(self) -> Connection:
        """获取连接实体"""
        return self._connection

    @property
    def session_id(self) -> str:
        """获取会话ID"""
        return self._connection.session_id

    def is_connected(self) -> bool:
        """判断是否已连接"""
        return self._connection.status.is_connected()

    def is_disconnected(self) -> bool:
        """判断是否已断开"""
        return self._connection.status.is_disconnected()

    def is_connecting(self) -> bool:
        """判断是否正在连接"""
        return self._connection.status.is_connecting()

    def is_error(self) -> bool:
        """判断是否有错误"""
        return self._connection.status.is_error()

    def get_config(self) -> ConnectionConfig:
        """获取连接配置"""
        return self._connection.config

    def get_credential(self) -> Optional[AuthCredential]:
        """获取认证凭据"""
        return self._connection.credential

    def get_status(self) -> ConnectionStatus:
        """获取连接状态"""
        return self._connection.status

    def get_duration(self) -> Optional[float]:
        """获取连接时长"""
        return self._connection.get_duration()

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self._connection.id,
            "config": self._connection.config.to_dict(),
            "credential": self._connection.credential.to_dict() if self._connection.credential else None,
            "status": str(self._connection.status),
            "connected_at": str(self._connection.connected_at) if self._connection.connected_at else None,
        }

"""连接状态值对象"""
from enum import Enum

from pydantic import BaseModel


class ConnectionStatusEnum(str, Enum):
    """连接状态枚举"""
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    CONNECTING = "CONNECTING"
    ERROR = "ERROR"


class ConnectionStatus(BaseModel):
    """连接状态值对象"""
    status: ConnectionStatusEnum = ConnectionStatusEnum.DISCONNECTED
    message: str = ""

    model_config = {"frozen": True}

    def is_connected(self) -> bool:
        """判断是否已连接"""
        return self.status == ConnectionStatusEnum.CONNECTED

    def is_disconnected(self) -> bool:
        """判断是否已断开"""
        return self.status == ConnectionStatusEnum.DISCONNECTED

    def is_connecting(self) -> bool:
        """判断是否正在连接"""
        return self.status == ConnectionStatusEnum.CONNECTING

    def is_error(self) -> bool:
        """判断是否有错误"""
        return self.status == ConnectionStatusEnum.ERROR

    def mark_connected(self, message: str = "") -> "ConnectionStatus":
        """标记为已连接"""
        return ConnectionStatus(status=ConnectionStatusEnum.CONNECTED, message=message)

    def mark_disconnected(self, message: str = "") -> "ConnectionStatus":
        """标记为已断开"""
        return ConnectionStatus(status=ConnectionStatusEnum.DISCONNECTED, message=message)

    def mark_connecting(self, message: str = "") -> "ConnectionStatus":
        """标记为正在连接"""
        return ConnectionStatus(status=ConnectionStatusEnum.CONNECTING, message=message)

    def mark_error(self, message: str) -> "ConnectionStatus":
        """标记为错误"""
        return ConnectionStatus(status=ConnectionStatusEnum.ERROR, message=message)

    def __str__(self) -> str:
        return self.status.value

    def __repr__(self) -> str:
        return f"ConnectionStatus(status={self.status.value}, message='{self.message}')"

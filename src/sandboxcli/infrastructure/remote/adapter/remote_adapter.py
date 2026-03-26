"""远程通信适配器 - 抽象接口

定义与远程沙盒系统通信的抽象接口，支持多种连接方式（SSH、HTTP API）。
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ....domain.command.value_objects import CommandInput, CommandOutput
from ....domain.connection.value_objects import ConnectionConfig


class RemoteAdapter(ABC):
    """远程通信适配器基类 - 定义与远程沙盒通信的接口"""

    def __init__(self, config: ConnectionConfig):
        """初始化适配器

        Args:
            config: 连接配置
        """
        self._config = config
        self._connected = False

    @property
    def config(self) -> ConnectionConfig:
        """获取连接配置"""
        return self._config

    @property
    def is_connected(self) -> bool:
        """是否已连接"""
        return self._connected

    @abstractmethod
    def connect(self) -> bool:
        """建立连接

        Returns:
            连接是否成功
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """断开连接"""
        pass

    @abstractmethod
    def execute_command(self, command_input: CommandInput) -> CommandOutput:
        """执行命令

        Args:
            command_input: 命令输入

        Returns:
            命令输出
        """
        pass

    @abstractmethod
    def get_sandbox_info(self) -> Dict[str, Any]:
        """获取沙盒信息

        Returns:
            沙盒信息字典
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """健康检查

        Returns:
            服务是否健康
        """
        pass

    def __enter__(self) -> "RemoteAdapter":
        """上下文管理器入口"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """上下文管理器出口"""
        self.disconnect()

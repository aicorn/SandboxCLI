"""日志模块

提供统一的日志记录功能。
"""
import logging
import sys
from enum import Enum
from typing import Optional


class LogLevel(Enum):
    """日志级别"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class Logger:
    """日志记录器

    提供统一的日志记录接口，支持多种输出格式和级别。
    """

    _instance: Optional["Logger"] = None

    def __init__(
        self,
        name: str = "sandboxcli",
        level: LogLevel = LogLevel.INFO,
        format_string: Optional[str] = None,
    ):
        """初始化日志记录器

        Args:
            name: 日志记录器名称
            level: 日志级别
            format_string: 日志格式字符串
        """
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level.value)

        # 清除已有的处理器
        self._logger.handlers.clear()

        # 设置默认格式
        if format_string is None:
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        formatter = logging.Formatter(format_string)

        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

    @classmethod
    def get_instance(
        cls,
        name: str = "sandboxcli",
        level: LogLevel = LogLevel.INFO,
    ) -> "Logger":
        """获取日志记录器单例

        Args:
            name: 日志记录器名称
            level: 日志级别

        Returns:
            日志记录器实例
        """
        if cls._instance is None:
            cls._instance = cls(name=name, level=level)
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """重置单例"""
        cls._instance = None

    def debug(self, message: str) -> None:
        """记录调试信息"""
        self._logger.debug(message)

    def info(self, message: str) -> None:
        """记录一般信息"""
        self._logger.info(message)

    def warning(self, message: str) -> None:
        """记录警告信息"""
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """记录错误信息"""
        self._logger.error(message)

    def critical(self, message: str) -> None:
        """记录严重错误信息"""
        self._logger.critical(message)

    def set_level(self, level: LogLevel) -> None:
        """设置日志级别"""
        self._logger.setLevel(level.value)

    def add_file_handler(
        self,
        file_path: str,
        level: LogLevel = LogLevel.DEBUG,
        format_string: Optional[str] = None,
    ) -> None:
        """添加文件处理器

        Args:
            file_path: 日志文件路径
            level: 文件日志级别
            format_string: 日志格式字符串
        """
        if format_string is None:
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        formatter = logging.Formatter(format_string)

        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        file_handler.setLevel(level.value)
        file_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)


# 全局日志记录器
_default_logger = Logger.get_instance()


def get_logger(name: str = "sandboxcli") -> Logger:
    """获取日志记录器

    Args:
        name: 日志记录器名称

    Returns:
        日志记录器
    """
    return Logger.get_instance(name=name)


# 便捷函数
def debug(message: str) -> None:
    """记录调试信息"""
    _default_logger.debug(message)


def info(message: str) -> None:
    """记录一般信息"""
    _default_logger.info(message)


def warning(message: str) -> None:
    """记录警告信息"""
    _default_logger.warning(message)


def error(message: str) -> None:
    """记录错误信息"""
    _default_logger.error(message)


def critical(message: str) -> None:
    """记录严重错误信息"""
    _default_logger.critical(message)

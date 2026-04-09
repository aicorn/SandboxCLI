"""日志模块

提供统一的日志记录功能。
"""
import logging
import sys
from datetime import datetime
from enum import Enum
from typing import Optional


class LogLevel(Enum):
    """日志级别"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class VerboseLogger:
    """Verbose调试日志记录器
    
    根据VerboseConfig配置输出调试信息。
    支持时间戳和彩色输出。
    """
    
    # ANSI颜色码
    COLOR_RESET = "\033[0m"
    COLOR_RED = "\033[91m"
    COLOR_YELLOW = "\033[93m"
    COLOR_GREEN = "\033[92m"
    COLOR_BLUE = "\033[94m"
    COLOR_GRAY = "\033[90m"
    
    LEVEL_COLORS = {
        "DEBUG": COLOR_BLUE,
        "INFO": COLOR_GREEN,
        "WARNING": COLOR_YELLOW,
        "ERROR": COLOR_RED,
    }
    
    def __init__(
        self,
        level: str = "off",
        enable_timestamp: bool = True,
        enable_color: bool = True,
    ):
        """初始化VerboseLogger
        
        Args:
            level: 调试级别 (off/error/info/debug)
            enable_timestamp: 是否显示时间戳
            enable_color: 是否使用彩色输出
        """
        self._level = level.lower()
        self._enable_timestamp = enable_timestamp
        self._enable_color = enable_color
    
    @property
    def level(self) -> str:
        """获取调试级别"""
        return self._level
    
    def _should_log(self, message_level: str) -> bool:
        """判断是否应该记录日志"""
        level_order = {"debug": 0, "info": 1, "error": 2, "off": 3}
        message_level_value = level_order.get(message_level.lower(), 3)
        current_level_value = level_order.get(self._level, 3)
        return message_level_value >= current_level_value
    
    def _format_message(self, level: str, message: str) -> str:
        """格式化日志消息"""
        parts = []
        
        # 添加时间戳
        if self._enable_timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            parts.append(f"[{timestamp}]")
        
        # 添加级别
        level_str = level.upper()
        if self._enable_color and level_str in self.LEVEL_COLORS:
            color = self.LEVEL_COLORS[level_str]
            parts.append(f"{color}{level_str}{self.COLOR_RESET}")
        else:
            parts.append(level_str)
        
        # 添加消息
        parts.append(message)
        
        return " ".join(parts)
    
    def debug(self, message: str) -> None:
        """记录调试信息"""
        if self._should_log("debug"):
            formatted = self._format_message("debug", message)
            print(formatted)
    
    def info(self, message: str) -> None:
        """记录一般信息"""
        if self._should_log("info"):
            formatted = self._format_message("info", message)
            print(formatted)
    
    def error(self, message: str) -> None:
        """记录错误信息"""
        if self._should_log("error"):
            formatted = self._format_message("error", message)
            print(formatted, file=sys.stderr)
    
    def log(self, message: str) -> None:
        """记录信息（根据当前级别）"""
        if self._level == "debug":
            self.debug(message)
        elif self._level == "info":
            self.info(message)
        elif self._level == "error":
            self.error(message)
    
    def set_level(self, level: str) -> None:
        """设置调试级别"""
        self._level = level.lower()
    
    def is_enabled(self) -> bool:
        """是否启用"""
        return self._level != "off"


# 全局VerboseLogger实例
_verbose_logger = VerboseLogger()


def get_verbose_logger(
    level: str = "off",
    enable_timestamp: bool = True,
    enable_color: bool = True,
) -> VerboseLogger:
    """获取VerboseLogger实例
    
    Args:
        level: 调试级别
        enable_timestamp: 是否显示时间戳
        enable_color: 是否使用彩色输出
    
    Returns:
        VerboseLogger实例
    """
    global _verbose_logger
    _verbose_logger = VerboseLogger(
        level=level,
        enable_timestamp=enable_timestamp,
        enable_color=enable_color,
    )
    return _verbose_logger


def get_current_verbose_logger() -> VerboseLogger:
    """获取当前全局VerboseLogger实例"""
    return _verbose_logger


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

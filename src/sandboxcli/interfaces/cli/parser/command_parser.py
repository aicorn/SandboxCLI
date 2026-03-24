"""命令解析器"""
import shlex
from typing import List, Optional


class CommandParser:
    """命令解析器"""

    @staticmethod
    def parse_command_line(command_line: str) -> tuple[str, List[str]]:
        """解析命令行"""
        try:
            parts = shlex.split(command_line)
            if not parts:
                return "", []
            
            command = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            return command, args
        except ValueError:
            return "", []

    @staticmethod
    def parse_env_vars(env_str: str) -> dict:
        """解析环境变量字符串"""
        env = {}
        if not env_str:
            return env
        
        for part in env_str.split(","):
            if "=" in part:
                key, value = part.split("=", 1)
                env[key.strip()] = value.strip()
        return env

    @staticmethod
    def parse_key_value(kv_str: str) -> Optional[tuple[str, str]]:
        """解析键值对"""
        if "=" in kv_str:
            key, value = kv_str.split("=", 1)
            return key.strip(), value.strip()
        return None


__all__ = ["CommandParser"]

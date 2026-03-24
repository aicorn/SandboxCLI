"""命令输入值对象"""
from typing import List, Optional

from pydantic import BaseModel, field_validator


class CommandInput(BaseModel):
    """命令输入值对象"""
    command: str
    args: List[str] = []
    working_directory: Optional[str] = None
    env: Optional[dict] = None

    model_config = {"frozen": True}

    @field_validator("command")
    @classmethod
    def _validate_command(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Command cannot be empty")
        return v.strip()

    def __str__(self) -> str:
        if self.args:
            return f"{self.command} {' '.join(self.args)}"
        return self.command

    def __repr__(self) -> str:
        return f"CommandInput(command='{self.command}', args={self.args})"

    def to_shell_string(self) -> str:
        """转换为shell命令字符串"""
        parts = [self.command]
        parts.extend(self.args)
        return " ".join(parts)

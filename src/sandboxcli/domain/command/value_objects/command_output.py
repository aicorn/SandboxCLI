"""命令输出值对象"""
from typing import Optional

from pydantic import BaseModel, field_validator


class CommandOutput(BaseModel):
    """命令输出值对象"""
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0

    model_config = {"frozen": True}

    @field_validator("exit_code")
    @classmethod
    def _validate_exit_code(cls, v: int) -> int:
        if v < 0 or v > 255:
            raise ValueError("Exit code must be between 0 and 255")
        return v

    def __str__(self) -> str:
        if self.stderr:
            return f"[stderr] {self.stderr}\n[stdout] {self.stdout}"
        return self.stdout

    def __repr__(self) -> str:
        return f"CommandOutput(stdout='{self.stdout[:50]}...', stderr='{self.stderr[:50]}...', exit_code={self.exit_code})"

    def has_error(self) -> bool:
        """判断是否有错误"""
        return bool(self.stderr) or self.exit_code != 0

    def has_output(self) -> bool:
        """判断是否有输出内容（标准输出或标准错误）"""
        return bool(self.stdout) or bool(self.stderr)

    def is_success(self) -> bool:
        """判断是否成功"""
        return not self.has_error()

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "exit_code": self.exit_code,
        }

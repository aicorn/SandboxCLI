"""执行记录实体"""
import uuid
from typing import Optional

from pydantic import BaseModel, Field

from ...shared import Timestamp
from ..value_objects import CommandInput, CommandOutput, ExecutionStatus


class Execution(BaseModel):
    """执行记录实体 - 命令执行记录"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    command_input: CommandInput
    command_output: Optional[CommandOutput] = None
    status: ExecutionStatus = Field(default_factory=ExecutionStatus)
    started_at: Optional[Timestamp] = None
    ended_at: Optional[Timestamp] = None

    model_config = {"frozen": False}

    @classmethod
    def create(cls, command_input: CommandInput) -> "Execution":
        """创建执行记录"""
        return cls(command_input=command_input)

    @property
    def execution_id(self) -> str:
        """获取执行记录ID"""
        return self.id

    def start(self) -> None:
        """开始执行"""
        self.status = self.status.mark_running()
        self.started_at = Timestamp.now()

    def complete(self, output: CommandOutput) -> None:
        """完成执行"""
        self.command_output = output
        if output.is_success():
            self.status = self.status.mark_success()
        else:
            self.status = self.status.mark_failed()
        self.ended_at = Timestamp.now()

    def fail(self, error: str) -> None:
        """执行失败"""
        self.command_output = CommandOutput(stderr=error, exit_code=1)
        self.status = self.status.mark_failed()
        self.ended_at = Timestamp.now()

    def timeout(self) -> None:
        """执行超时"""
        self.command_output = CommandOutput(stderr="Command execution timed out", exit_code=124)
        self.status = self.status.mark_timeout()
        self.ended_at = Timestamp.now()

    def mark_timeout_with_connection_fail(self) -> None:
        """执行超时且连接检测失败"""
        self.command_output = CommandOutput(
            stderr="Command execution timed out. Connection to sandbox service is unreachable.",
            exit_code=124
        )
        self.status = self.status.mark_timeout_with_connection_fail()
        self.ended_at = Timestamp.now()

    def mark_timeout_with_connection_ok(self) -> None:
        """执行超时但连接正常（可能是命令执行慢）"""
        self.command_output = CommandOutput(
            stderr="Command execution timed out, but sandbox service is reachable.",
            exit_code=124
        )
        self.status = self.status.mark_timeout_with_connection_ok()
        self.ended_at = Timestamp.now()

    def get_duration(self) -> Optional[float]:
        """获取执行时长（秒）"""
        if self.started_at and self.ended_at:
            return (self.ended_at.value - self.started_at.value).total_seconds()
        return None

    def __str__(self) -> str:
        return f"Execution(id='{self.id}', status='{self.status}')"

    def __repr__(self) -> str:
        return f"Execution(id='{self.id}', input={self.command_input}, status={self.status})"

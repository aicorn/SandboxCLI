"""指令上下文领域事件"""
from typing import Optional

from ...shared import DomainEvent, Timestamp
from ..value_objects import CommandInput, CommandOutput, ExecutionStatus


class CommandExecutedEvent(DomainEvent):
    """命令执行事件"""

    command_id: str
    execution_id: str
    input: CommandInput
    output: CommandOutput
    status: ExecutionStatus
    duration: Optional[float] = None

    def get_event_type(self) -> str:
        return "CommandExecutedEvent"

    def get_aggregate_id(self) -> str:
        return self.execution_id


class CommandFailedEvent(DomainEvent):
    """命令执行失败事件"""

    command_id: str
    execution_id: str
    input: CommandInput
    error: str
    status: ExecutionStatus

    def get_event_type(self) -> str:
        return "CommandFailedEvent"

    def get_aggregate_id(self) -> str:
        return self.execution_id


class CommandTimeoutEvent(DomainEvent):
    """命令执行超时事件
    
    当指令执行超时时触发此事件，可用于触发连接健康检查。
    """

    command_id: str
    execution_id: str
    input: CommandInput
    timeout_duration: int  # 超时时长（秒）
    connection_check_required: bool = True  # 是否需要检查连接

    def get_event_type(self) -> str:
        return "CommandTimeoutEvent"

    def get_aggregate_id(self) -> str:
        return self.execution_id


__all__ = ["CommandExecutedEvent", "CommandFailedEvent", "CommandTimeoutEvent"]

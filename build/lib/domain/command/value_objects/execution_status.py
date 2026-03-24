"""执行状态值对象"""
from enum import Enum

from pydantic import BaseModel


class ExecutionStatusEnum(str, Enum):
    """执行状态枚举"""
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    RUNNING = "RUNNING"
    PENDING = "PENDING"


class ExecutionStatus(BaseModel):
    """执行状态值对象"""
    status: ExecutionStatusEnum = ExecutionStatusEnum.PENDING

    model_config = {"frozen": True}

    def is_success(self) -> bool:
        """判断是否成功"""
        return self.status == ExecutionStatusEnum.SUCCESS

    def is_failed(self) -> bool:
        """判断是否失败"""
        return self.status == ExecutionStatusEnum.FAILED

    def is_timeout(self) -> bool:
        """判断是否超时"""
        return self.status == ExecutionStatusEnum.TIMEOUT

    def is_running(self) -> bool:
        """判断是否正在运行"""
        return self.status == ExecutionStatusEnum.RUNNING

    def is_pending(self) -> bool:
        """判断是否待处理"""
        return self.status == ExecutionStatusEnum.PENDING

    def mark_success(self) -> "ExecutionStatus":
        """标记为成功"""
        return ExecutionStatus(status=ExecutionStatusEnum.SUCCESS)

    def mark_failed(self) -> "ExecutionStatus":
        """标记为失败"""
        return ExecutionStatus(status=ExecutionStatusEnum.FAILED)

    def mark_timeout(self) -> "ExecutionStatus":
        """标记为超时"""
        return ExecutionStatus(status=ExecutionStatusEnum.TIMEOUT)

    def mark_running(self) -> "ExecutionStatus":
        """标记为运行中"""
        return ExecutionStatus(status=ExecutionStatusEnum.RUNNING)

    def __str__(self) -> str:
        return self.status.value

    def __repr__(self) -> str:
        return f"ExecutionStatus(status={self.status.value})"

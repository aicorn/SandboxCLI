"""执行聚合"""
from typing import Optional

from ..entities.execution import Execution
from ..value_objects import CommandOutput


class ExecutionAggregate:
    """执行聚合根"""

    def __init__(self, execution: Execution):
        self._execution = execution

    @property
    def execution(self) -> Execution:
        """获取执行记录实体"""
        return self._execution

    @property
    def execution_id(self) -> str:
        """获取执行记录ID"""
        return self._execution.id

    def is_completed(self) -> bool:
        """判断是否完成"""
        return not self._execution.status.is_running() and not self._execution.status.is_pending()

    def is_success(self) -> bool:
        """判断是否成功"""
        return self._execution.status.is_success()

    def is_failed(self) -> bool:
        """判断是否失败"""
        return self._execution.status.is_failed()

    def is_timeout(self) -> bool:
        """判断是否超时"""
        return self._execution.status.is_timeout()

    def get_output(self) -> Optional[CommandOutput]:
        """获取输出"""
        return self._execution.command_output

    def get_duration(self) -> Optional[float]:
        """获取执行时长"""
        return self._execution.get_duration()

    def to_dict(self) -> dict:
        """转换为字典"""
        result = {
            "id": self._execution.id,
            "command": str(self._execution.command_input),
            "status": str(self._execution.status),
            "started_at": str(self._execution.started_at) if self._execution.started_at else None,
            "ended_at": str(self._execution.ended_at) if self._execution.ended_at else None,
            "duration": self.get_duration(),
        }
        if self._execution.command_output:
            result["output"] = self._execution.command_output.to_dict()
        return result

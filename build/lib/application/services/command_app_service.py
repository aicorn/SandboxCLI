"""命令应用服务"""
from typing import Dict, Optional

from ...domain.command import CommandInput, CommandService, ExecutionAggregate
from ...domain.shared import Result
from ..commands.command import ExecuteCommandCommand


class CommandAppService:
    """命令应用服务"""

    def __init__(self):
        self._current_execution: Optional[ExecutionAggregate] = None

    def create_execution(self, command: ExecuteCommandCommand) -> Result[ExecutionAggregate]:
        """创建命令执行"""
        input_result = CommandService.create_command_input(
            command=command.command,
            args=command.args,
            working_directory=command.working_directory,
        )
        
        if input_result.is_failure():
            return Result.fail(input_result.error)
        
        execution = CommandService.create_execution(input_result.value)
        self._current_execution = execution
        return Result.ok(execution)

    def get_current_execution(self) -> Optional[ExecutionAggregate]:
        """获取当前执行"""
        return self._current_execution

    def execute_command(self, command: ExecuteCommandCommand) -> Result[Dict]:
        """执行命令（实际执行需要通过适配器调用远程服务）"""
        exec_result = self.create_execution(command)
        if exec_result.is_failure():
            return Result.fail(exec_result.error)
        
        execution = exec_result.value
        execution.execution.start()
        
        # 这里应该调用远程执行服务
        # 由基础设施层实现
        
        return Result.ok(execution.to_dict())

    def get_execution_result(self, execution_id: str) -> Result[Dict]:
        """获取执行结果"""
        if self._current_execution and self._current_execution.execution_id == execution_id:
            return Result.ok(self._current_execution.to_dict())
        return Result.fail("Execution not found")

"""指令领域服务"""
from typing import List

from ...shared import Result
from ..aggregates import CommandAggregate, ExecutionAggregate
from ..entities import Command, Execution
from ..value_objects import CommandInput, ExecutionStatus


class CommandService:
    """指令管理服务"""

    @staticmethod
    def create_command(command: str, args: List[str] = None, working_directory: str = None) -> CommandAggregate:
        """创建命令"""
        command_entity = Command.create(
            command=command,
            args=args,
            working_directory=working_directory,
        )
        return CommandAggregate(command_entity)

    @staticmethod
    def create_execution(command_input: CommandInput) -> ExecutionAggregate:
        """创建执行记录"""
        execution = Execution.create(command_input=command_input)
        return ExecutionAggregate(execution)

    @staticmethod
    def validate_command(command: str) -> Result[str]:
        """验证命令"""
        if not command or not command.strip():
            return Result.fail("Command cannot be empty")
        return Result.ok(command.strip())

    @staticmethod
    def create_command_input(command: str, args: List[str] = None, working_directory: str = None) -> Result[CommandInput]:
        """创建命令输入"""
        validation = CommandService.validate_command(command)
        if validation.is_failure():
            return Result.fail(validation.error)
        
        try:
            input_obj = CommandInput(
                command=command,
                args=args or [],
                working_directory=working_directory,
            )
            return Result.ok(input_obj)
        except Exception as e:
            return Result.fail(f"Invalid command input: {str(e)}")

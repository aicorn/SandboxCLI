"""命令聚合"""
from ..entities.command import Command


class CommandAggregate:
    """命令聚合根"""

    def __init__(self, command: Command):
        self._command = command

    @property
    def command(self) -> Command:
        """获取命令实体"""
        return self._command

    @property
    def command_id(self) -> str:
        """获取命令ID"""
        return self._command.id

    def get_input_string(self) -> str:
        """获取命令输入字符串"""
        return str(self._command.input)

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self._command.id,
            "input": str(self._command.input),
            "description": self._command.description,
        }

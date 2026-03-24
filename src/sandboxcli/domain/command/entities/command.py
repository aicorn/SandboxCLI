"""命令实体"""
import uuid
from typing import List, Optional

from pydantic import BaseModel, Field

from ..value_objects import CommandInput


class Command(BaseModel):
    """命令实体 - 要执行的命令"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    input: CommandInput
    description: Optional[str] = None
    created_at: Optional[str] = None

    model_config = {"frozen": True}

    @classmethod
    def create(cls, command: str, args: List[str] = None, working_directory: str = None) -> "Command":
        """创建命令"""
        input_obj = CommandInput(
            command=command,
            args=args or [],
            working_directory=working_directory,
        )
        return cls(input=input_obj)

    @property
    def command_id(self) -> str:
        """获取命令ID"""
        return self.id

    def __str__(self) -> str:
        return f"Command(id='{self.id}', command='{self.input.command}')"

    def __repr__(self) -> str:
        return f"Command(id='{self.id}', input={self.input})"

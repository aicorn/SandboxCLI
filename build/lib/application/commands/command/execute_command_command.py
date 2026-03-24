"""执行命令命令"""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ExecuteCommandCommand(BaseModel):
    """执行远程命令命令"""
    command: str = Field(..., description="要执行的命令")
    args: List[str] = Field(default_factory=list, description="命令参数")
    working_directory: Optional[str] = Field(None, description="工作目录")
    timeout: Optional[int] = Field(None, description="超时时间（秒）")
    env: Optional[Dict] = Field(None, description="环境变量")

    model_config = {"frozen": True}

    def get_full_command(self) -> str:
        """获取完整命令字符串"""
        if self.args:
            return f"{self.command} {' '.join(self.args)}"
        return self.command

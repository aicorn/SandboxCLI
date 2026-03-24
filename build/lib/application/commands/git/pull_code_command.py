"""拉取代码命令"""
from pydantic import BaseModel, Field


class PullCodeCommand(BaseModel):
    """拉取代码命令"""
    repo_path: str = Field(".", description="仓库路径")
    branch: str = Field("HEAD", description="分支名称")
    rebase: bool = Field(False, description="是否使用rebase")

    model_config = {"frozen": True}

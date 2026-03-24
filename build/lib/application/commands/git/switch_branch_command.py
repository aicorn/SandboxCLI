"""切换分支命令"""
from pydantic import BaseModel, Field


class SwitchBranchCommand(BaseModel):
    """切换Git分支命令"""
    branch_name: str = Field(..., description="分支名称")
    repo_path: str = Field(".", description="仓库路径")
    create_new: bool = Field(False, description="是否创建新分支")

    model_config = {"frozen": True}

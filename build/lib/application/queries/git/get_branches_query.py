"""获取分支列表查询"""
from pydantic import BaseModel, Field


class GetBranchesQuery(BaseModel):
    """获取分支列表查询"""
    repo_path: str = Field(".", description="仓库路径")
    include_remote: bool = Field(True, description="是否包含远程分支")
    include_current_only: bool = Field(False, description="是否只包含当前分支信息")

    model_config = {"frozen": True}

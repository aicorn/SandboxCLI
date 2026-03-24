"""获取Git日志查询"""
from pydantic import BaseModel, Field


class GetGitLogQuery(BaseModel):
    """获取Git日志查询"""
    repo_path: str = Field(".", description="仓库路径")
    max_count: int = Field(10, description="最大日志数量")
    branch: str = Field(None, description="分支名称")

    model_config = {"frozen": True}

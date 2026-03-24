"""获取Git状态查询"""
from pydantic import BaseModel, Field


class GetGitStatusQuery(BaseModel):
    """获取Git状态查询"""
    repo_path: str = Field(".", description="仓库路径")

    model_config = {"frozen": True}

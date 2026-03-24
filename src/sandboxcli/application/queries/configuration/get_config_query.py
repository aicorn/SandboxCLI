"""获取配置查询"""
from pydantic import BaseModel, Field


class GetConfigQuery(BaseModel):
    """获取配置查询"""
    config_id: str = Field("default", description="配置ID")
    include_sensitive: bool = Field(False, description="是否包含敏感信息")

    model_config = {"frozen": True}

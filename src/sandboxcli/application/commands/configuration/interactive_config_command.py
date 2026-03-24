"""交互式配置命令"""
from pydantic import BaseModel


class InteractiveConfigCommand(BaseModel):
    """交互式配置命令"""
    config_id: str = "default"

    model_config = {"frozen": True}

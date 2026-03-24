"""配置项值对象"""
from typing import Any, Optional

from pydantic import BaseModel, field_validator


class ConfigItem(BaseModel):
    """单个配置项值对象"""
    key: str
    value: Any
    description: Optional[str] = None
    default_value: Optional[Any] = None

    model_config = {"frozen": True}

    @field_validator("key")
    @classmethod
    def _validate_key(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Config key cannot be empty")
        return v.strip()

    def __str__(self) -> str:
        return f"{self.key}={self.value}"

    def __repr__(self) -> str:
        return f"ConfigItem(key='{self.key}', value={self.value!r})"

    def is_default(self) -> bool:
        """判断是否使用默认值"""
        return self.value == self.default_value

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "key": self.key,
            "value": self.value,
            "description": self.description,
            "default_value": self.default_value,
        }

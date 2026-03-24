"""结果值对象"""
from typing import Generic, TypeVar, Optional, Any

from pydantic import BaseModel, Field, field_validator

T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    """结果值对象，表示操作的成功或失败"""
    is_success: bool
    value: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None

    model_config = {"frozen": True, "arbitrary_types_allowed": True}

    @field_validator("value", mode="before")
    @classmethod
    def validate_value(cls, v):
        """允许任何类型的值"""
        return v

    @classmethod
    def ok(cls, value: T, message: Optional[str] = None) -> "Result[T]":
        """创建成功结果"""
        return cls(is_success=True, value=value, message=message)

    @classmethod
    def fail(cls, error: str, message: Optional[str] = None) -> "Result[T]":
        """创建失败结果"""
        return cls(is_success=False, error=error, message=message)

    def is_failure(self) -> bool:
        """判断是否失败"""
        return not self.is_success

    def unwrap(self) -> T:
        """获取值，如果失败则抛出异常"""
        if self.is_failure():
            raise ValueError(self.error or "Operation failed")
        return self.value  # type: ignore

    def unwrap_or(self, default: T) -> T:
        """获取值或默认值"""
        return self.value if self.is_success else default

    def __str__(self) -> str:
        if self.is_success:
            return f"Result.ok({self.value})"
        return f"Result.fail({self.error})"

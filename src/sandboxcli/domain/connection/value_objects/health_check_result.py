"""健康检查结果值对象"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class HealthCheckResult(BaseModel):
    """连接健康检查结果值对象"""

    is_reachable: bool = Field(default=False, description="是否可到达")
    latency: Optional[int] = Field(default=None, description="延迟（毫秒）")
    error_message: Optional[str] = Field(default=None, description="错误信息（如果不可达）")
    checked_at: datetime = Field(default_factory=datetime.now, description="检测时间")

    model_config = {"frozen": True}

    @classmethod
    def success(cls, latency: int) -> "HealthCheckResult":
        """创建成功结果"""
        return cls(
            is_reachable=True,
            latency=latency,
            error_message=None,
            checked_at=datetime.now()
        )

    @classmethod
    def failure(cls, error_message: str) -> "HealthCheckResult":
        """创建失败结果"""
        return cls(
            is_reachable=False,
            latency=None,
            error_message=error_message,
            checked_at=datetime.now()
        )

    def __str__(self) -> str:
        if self.is_reachable:
            return f"HealthCheckResult(OK, latency={self.latency}ms)"
        return f"HealthCheckResult(FAIL, error={self.error_message})"

    def __repr__(self) -> str:
        return self.__str__()
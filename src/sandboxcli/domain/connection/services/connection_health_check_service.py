"""连接健康检查领域服务"""
from ...shared import Result
from ..value_objects import ConnectionConfig, HealthCheckResult


class ConnectionHealthCheckService:
    """连接健康检查服务
    
    负责检测与远程沙盒服务的连接健康状态。
    该服务是领域服务，具体的健康检查实现由基础设施层提供。
    """

    @staticmethod
    def create_health_check_result(
        is_reachable: bool,
        latency: int = None,
        error_message: str = None,
    ) -> HealthCheckResult:
        """创建健康检查结果"""
        if is_reachable:
            return HealthCheckResult.success(latency)
        return HealthCheckResult.failure(error_message or "Connection unreachable")

    @staticmethod
    def validate_config_for_health_check(
        config: ConnectionConfig,
    ) -> Result[ConnectionConfig]:
        """验证配置是否可用于健康检查"""
        if not config.host:
            return Result.fail("Host is required for health check")
        if config.port <= 0 or config.port > 65535:
            return Result.fail(f"Invalid port: {config.port}")
        return Result.ok(config)

    @staticmethod
    def is_timeout_likely_due_to_connection(
        health_check_result: HealthCheckResult,
        timeout_threshold_ms: int = 5000,
    ) -> bool:
        """判断超是否可能是由于连接问题导致
        
        Args:
            health_check_result: 健康检查结果
            timeout_threshold_ms: 超时阈值（毫秒），默认5秒
            
        Returns:
            True 表示可能是连接问题导致的超时
        """
        if not health_check_result.is_reachable:
            return True
        
        # 如果延迟超过阈值，也认为是连接问题
        if health_check_result.latency is not None:
            return health_check_result.latency > timeout_threshold_ms
        
        return False

    @staticmethod
    def get_timeout_status(
        health_check_result: HealthCheckResult,
    ) -> str:
        """获取超时状态描述
        
        Args:
            health_check_result: 健康检查结果
            
        Returns:
            超时状态描述字符串
        """
        if not health_check_result.is_reachable:
            return "TIMEOUT_WITH_CONNECTION_FAIL"
        
        if health_check_result.latency is not None and health_check_result.latency > 5000:
            return "TIMEOUT_WITH_HIGH_LATENCY"
        
        return "TIMEOUT_WITH_CONNECTION_OK"
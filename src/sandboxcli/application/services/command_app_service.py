"""命令应用服务"""
import time
from typing import Dict, Optional, TYPE_CHECKING

from ...domain.command import CommandInput, CommandService, ExecutionAggregate
from ...domain.command.value_objects import CommandOutput
from ...domain.connection.value_objects import HealthCheckResult
from ...domain.connection.services import ConnectionHealthCheckService
from ...domain.shared import Result
from ...infrastructure.persistence.config.config_repository import ConfigRepository
from ...infrastructure.remote.adapter.factory import RemoteAdapterFactory
from ..commands.command import ExecuteCommandCommand

if TYPE_CHECKING:
    from ...infrastructure.remote.adapter.remote_adapter import RemoteAdapter


class CommandAppService:
    """命令应用服务"""

    def __init__(self):
        self._current_execution: Optional[ExecutionAggregate] = None
        self._config_repository = ConfigRepository()
        self._config = self._config_repository.load()
        self._remote_client: Optional["RemoteAdapter"] = None  # 缓存远程客户端

    def _get_base_url(self) -> Optional[str]:
        """从配置中获取base_url"""
        if self._config.server_address and self._config.server_address.base_url:
            return self._config.server_address.base_url
        return None

    def _get_timeout(self) -> int:
        """从配置中获取超时时间"""
        if self._config.timeout:
            return self._config.timeout.seconds
        return 30

    def _get_remote_client(self) -> Optional["RemoteAdapter"]:
        """获取或创建远程客户端"""
        if self._remote_client is None:
            base_url = self._get_base_url()
            if base_url:
                self._remote_client = RemoteAdapterFactory.create_sandbox_client(
                    base_url=base_url,
                    timeout=self._get_timeout(),
                )
        return self._remote_client

    def create_execution(self, command: ExecuteCommandCommand) -> Result[ExecutionAggregate]:
        """创建命令执行"""
        input_result = CommandService.create_command_input(
            command=command.command,
            args=command.args,
            working_directory=command.working_directory,
        )
        
        if input_result.is_failure():
            return Result.fail(input_result.error)
        
        execution = CommandService.create_execution(input_result.value)
        self._current_execution = execution
        return Result.ok(execution)

    def get_current_execution(self) -> Optional[ExecutionAggregate]:
        """获取当前执行"""
        return self._current_execution

    def execute_command(self, command: ExecuteCommandCommand) -> Result[Dict]:
        """执行命令（实际执行需要通过适配器调用远程服务）"""
        exec_result = self.create_execution(command)
        if exec_result.is_failure():
            return Result.fail(exec_result.error)
        
        execution = exec_result.value
        execution.execution.start()
        
        # 调用远程沙盒服务执行命令
        base_url = self._get_base_url()
        timeout = self._get_timeout()
        
        if base_url:
            # 使用 HTTP API 模式 (AIO Sandbox)
            client = self._get_remote_client()
            
            # 创建 CommandInput
            command_input = CommandInput(
                command=command.command,
                args=command.args,
                working_directory=command.working_directory,
            )
            
            # 执行远程命令（带超时处理）
            command_output = self._execute_with_timeout(client, command_input, timeout)
            
            # 检查是否超时
            if command_output is None:
                # 命令执行超时，进行连接健康检查
                health_check_result = self._perform_health_check()
                
                if health_check_result and not health_check_result.is_reachable:
                    # 连接不可达，标记为连接失败的超时
                    execution.execution.mark_timeout_with_connection_fail()
                else:
                    # 连接正常或无法确定，标记为普通超时
                    execution.execution.mark_timeout()
            else:
                # 命令执行成功
                execution.execution.complete(command_output)
        else:
            # 没有配置 base_url，无法执行远程命令
            execution.execution.fail("No server address configured. Please configure sandbox server first.")
        
        return Result.ok(execution.to_dict())

    def _execute_with_timeout(self, client, command_input: CommandInput, timeout: int) -> Optional[CommandOutput]:
        """带超时执行命令
        
        Args:
            client: 远程客户端
            command_input: 命令输入
            timeout: 超时时间（秒）
            
        Returns:
            命令输出，如果超时返回None
        """
        import threading
        result = []
        exception = [None]
        
        def execute_in_thread():
            try:
                result.append(client.execute_command(command_input))
            except Exception as e:
                exception[0] = e
        
        thread = threading.Thread(target=execute_in_thread)
        thread.daemon = True
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            # 超时
            return None
        
        if exception[0]:
            raise exception[0]
        
        return result[0] if result else None

    def _perform_health_check(self) -> Optional[HealthCheckResult]:
        """执行连接健康检查
        
        Returns:
            健康检查结果，如果检查失败返回None
        """
        client = self._get_remote_client()
        if not client:
            return None
        
        try:
            start_time = time.time()
            is_healthy = client.health_check()
            latency_ms = int((time.time() - start_time) * 1000)
            
            if is_healthy:
                return HealthCheckResult.success(latency_ms)
            return HealthCheckResult.failure("Health check failed")
        except Exception as e:
            return HealthCheckResult.failure(str(e))

    def get_execution_result(self, execution_id: str) -> Result[Dict]:
        """获取执行结果"""
        if self._current_execution and self._current_execution.execution_id == execution_id:
            return Result.ok(self._current_execution.to_dict())
        return Result.fail("Execution not found")

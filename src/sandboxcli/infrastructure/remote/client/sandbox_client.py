"""AIO Sandbox HTTP 客户端

实现与 AIO Sandbox HTTP API 的通信。
"""
from typing import Any, Dict, Optional

import httpx

from ....domain.command.value_objects import CommandInput, CommandOutput
from ....domain.connection.value_objects import ConnectionConfig

from ..adapter.remote_adapter import RemoteAdapter
from ..protocol.sandbox_protocol import SandboxProtocol


class SandboxClient(RemoteAdapter):
    """AIO Sandbox HTTP 客户端

    通过 HTTP API 与 AIO Sandbox 通信
    """

    def __init__(
        self,
        config: ConnectionConfig,
        timeout: int = 30,
        verify_ssl: bool = True,
    ):
        """初始化 AIO Sandbox 客户端

        Args:
            config: 连接配置
            timeout: 请求超时时间（秒）
            verify_ssl: 是否验证 SSL 证书
        """
        super().__init__(config)
        self._timeout = timeout
        self._verify_ssl = verify_ssl
        self._client: Optional[httpx.Client] = None
        self._base_url = config.base_url or f"http://{config.host}:{config.port}"

    def _get_client(self) -> httpx.Client:
        """获取 HTTP 客户端"""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                timeout=self._timeout,
                verify=self._verify_ssl,
            )
        return self._client

    def connect(self) -> bool:
        """建立连接"""
        try:
            client = self._get_client()
            response = client.get(SandboxProtocol.ENDPOINT_SANDBOX)
            response.raise_for_status()
            self._connected = True
            return True
        except httpx.HTTPError:
            self._connected = False
            return False

    def disconnect(self) -> None:
        """断开连接"""
        if self._client:
            self._client.close()
            self._client = None
        self._connected = False

    def execute_command(self, command_input: CommandInput) -> CommandOutput:
        """执行命令

        Args:
            command_input: 命令输入

        Returns:
            命令输出
        """
        client = self._get_client()

        request = SandboxProtocol.build_shell_exec_request(
            command=command_input.command,
            timeout=self._timeout,
        )

        try:
            response = client.post(
                SandboxProtocol.ENDPOINT_SHELL_EXEC,
                json=request.to_dict(),
            )
            response.raise_for_status()

            result = SandboxProtocol.parse_shell_response(response.json())

            return CommandOutput(
                stdout=result.output,
                stderr=result.stderr,
                exit_code=result.exit_code,
            )
        except httpx.HTTPError as e:
            return CommandOutput(
                stdout="",
                stderr=str(e),
                exit_code=1,
            )

    def get_sandbox_info(self) -> Dict[str, Any]:
        """获取沙盒信息"""
        client = self._get_client()

        try:
            response = client.get(SandboxProtocol.ENDPOINT_SANDBOX)
            response.raise_for_status()
            return response.json().get("data", {})
        except httpx.HTTPError as e:
            return {"error": str(e)}

    def health_check(self) -> bool:
        """健康检查"""
        try:
            client = self._get_client()
            response = client.get(SandboxProtocol.ENDPOINT_SANDBOX)
            return response.status_code == 200
        except httpx.HTTPError:
            return False

    def read_file(self, file_path: str) -> str:
        """读取文件

        Args:
            file_path: 文件路径

        Returns:
            文件内容
        """
        client = self._get_client()

        request = SandboxProtocol.build_file_read_request(file_path)

        try:
            response = client.post(
                SandboxProtocol.ENDPOINT_FILE_READ,
                json=request.to_dict(),
            )
            response.raise_for_status()

            result = SandboxProtocol.parse_file_read_response(response.json())
            return result.content
        except httpx.HTTPError as e:
            raise IOError(f"Failed to read file: {e}")

    def write_file(self, file_path: str, content: str) -> bool:
        """写入文件

        Args:
            file_path: 文件路径
            content: 文件内容

        Returns:
            是否成功
        """
        client = self._get_client()

        request = SandboxProtocol.build_file_write_request(file_path, content)

        try:
            response = client.post(
                SandboxProtocol.ENDPOINT_FILE_WRITE,
                json=request.to_dict(),
            )
            response.raise_for_status()
            return True
        except httpx.HTTPError as e:
            raise IOError(f"Failed to write file: {e}")

    def take_screenshot(self) -> str:
        """获取浏览器截图

        Returns:
            Base64 编码的截图数据
        """
        client = self._get_client()

        try:
            response = client.post(SandboxProtocol.ENDPOINT_BROWSER_SCREENSHOT)
            response.raise_for_status()

            data = response.json()
            return data.get("data", {}).get("screenshot", "")
        except httpx.HTTPError as e:
            raise IOError(f"Failed to take screenshot: {e}")

    def execute_jupyter_code(self, code: str) -> list:
        """执行 Jupyter 代码

        Args:
            code: Python 代码

        Returns:
            执行结果列表
        """
        client = self._get_client()

        request = SandboxProtocol.build_jupyter_execute_request(code)

        try:
            response = client.post(
                SandboxProtocol.ENDPOINT_JUPYTER_EXECUTE,
                json=request.to_dict(),
            )
            response.raise_for_status()

            result = SandboxProtocol.parse_jupyter_response(response.json())
            return result.outputs
        except httpx.HTTPError as e:
            raise IOError(f"Failed to execute Jupyter code: {e}")


class SandboxAsyncClient(SandboxClient):
    """AIO Sandbox 异步客户端"""

    async def connect(self) -> bool:
        """建立连接"""
        try:
            async with httpx.AsyncClient(
                base_url=self._base_url,
                timeout=self._timeout,
                verify=self._verify_ssl,
            ) as client:
                response = await client.get(SandboxProtocol.ENDPOINT_SANDBOX)
                response.raise_for_status()
                self._connected = True
                return True
        except httpx.HTTPError:
            self._connected = False
            return False

    async def execute_command(self, command_input: CommandInput) -> CommandOutput:
        """异步执行命令"""
        async with httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
            verify=self._verify_ssl,
        ) as client:
            request = SandboxProtocol.build_shell_exec_request(
                command=command_input.command,
                timeout=self._timeout,
            )

            try:
                response = await client.post(
                    SandboxProtocol.ENDPOINT_SHELL_EXEC,
                    json=request.to_dict(),
                )
                response.raise_for_status()

                result = SandboxProtocol.parse_shell_response(response.json())

                return CommandOutput(
                    stdout=result.output,
                    stderr=result.stderr,
                    exit_code=result.exit_code,
                )
            except httpx.HTTPError as e:
                return CommandOutput(
                    stdout="",
                    stderr=str(e),
                    exit_code=1,
                )

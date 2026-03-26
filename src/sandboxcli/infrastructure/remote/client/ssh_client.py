"""SSH 客户端

实现通过 SSH 与远程沙盒系统的通信。
"""
from typing import Any, Dict, Optional

import paramiko

from ....domain.command.value_objects import CommandInput, CommandOutput
from ....domain.connection.value_objects import ConnectionConfig, AuthCredential

from ..adapter.remote_adapter import RemoteAdapter


class SSHClient(RemoteAdapter):
    """SSH 客户端

    通过 SSH 协议与远程沙盒通信
    """

    def __init__(
        self,
        config: ConnectionConfig,
        credential: Optional[AuthCredential] = None,
        timeout: int = 30,
    ):
        """初始化 SSH 客户端

        Args:
            config: 连接配置
            credential: 认证凭据
            timeout: 连接超时时间（秒）
        """
        super().__init__(config)
        self._credential = credential
        self._timeout = timeout
        self._client: Optional[paramiko.SSHClient] = None

    def _get_client(self) -> paramiko.SSHClient:
        """获取 SSH 客户端"""
        if self._client is None:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client = client
        return self._client

    def connect(self) -> bool:
        """建立 SSH 连接"""
        try:
            client = self._get_client()

            # 构建连接参数
            connect_kwargs = {
                "hostname": self._config.host,
                "port": self._config.port,
                "username": self._config.username,
                "timeout": self._timeout,
            }

            # 添加认证信息
            if self._credential:
                if self._credential.password:
                    connect_kwargs["password"] = self._credential.password
                elif self._credential.private_key:
                    connect_kwargs["pkey"] = self._credential.private_key

            client.connect(**connect_kwargs)
            self._connected = True
            return True
        except paramiko.SSHException:
            self._connected = False
            return False

    def disconnect(self) -> None:
        """断开 SSH 连接"""
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

        try:
            stdin, stdout, stderr = client.exec_command(
                command_input.command,
                timeout=command_input.timeout,
            )

            stdout_data = stdout.read().decode("utf-8")
            stderr_data = stderr.read().decode("utf-8")
            exit_code = stdout.channel.recv_exit_status()

            return CommandOutput(
                stdout=stdout_data,
                stderr=stderr_data,
                exit_code=exit_code,
            )
        except Exception as e:
            return CommandOutput(
                stdout="",
                stderr=str(e),
                exit_code=1,
            )

    def get_sandbox_info(self) -> Dict[str, Any]:
        """获取远程沙盒信息"""
        # 执行系统信息命令
        output = self.execute_command(CommandInput(command="uname -a"))
        return {
            "system_info": output.stdout,
            "connected_host": self._config.host,
            "connected_port": self._config.port,
            "username": self._config.username,
        }

    def health_check(self) -> bool:
        """健康检查"""
        try:
            client = self._get_client()
            # 执行简单的命令来检查连接
            stdin, stdout, stderr = client.exec_command("echo 'health_check'")
            result = stdout.read().decode("utf-8").strip()
            return result == "health_check"
        except paramiko.SSHException:
            return False

    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """上传文件

        Args:
            local_path: 本地文件路径
            remote_path: 远程文件路径

        Returns:
            是否成功
        """
        try:
            sftp = self._client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            return True
        except IOError:
            return False

    def download_file(self, remote_path: str, local_path: str) -> bool:
        """下载文件

        Args:
            remote_path: 远程文件路径
            local_path: 本地文件路径

        Returns:
            是否成功
        """
        try:
            sftp = self._client.open_sftp()
            sftp.get(remote_path, local_path)
            sftp.close()
            return True
        except IOError:
            return False


class SSHSession:
    """SSH 会话管理器"""

    def __init__(self, client: SSHClient):
        """初始化 SSH 会话

        Args:
            client: SSH 客户端
        """
        self._client = client
        self._connected = False

    def __enter__(self) -> SSHClient:
        """上下文管理器入口"""
        if self._client.connect():
            self._connected = True
            return self._client
        raise ConnectionError("Failed to establish SSH connection")

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """上下文管理器出口"""
        if self._connected:
            self._client.disconnect()
            self._connected = False

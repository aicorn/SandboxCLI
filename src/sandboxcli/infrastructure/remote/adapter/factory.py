"""远程适配器工厂

根据连接配置创建适当的远程适配器实例。
"""
from typing import Optional

from ....domain.connection.value_objects import ConnectionConfig, AuthCredential

from ..adapter.remote_adapter import RemoteAdapter
from ..client.sandbox_client import SandboxClient
from ..client.ssh_client import SSHClient


class RemoteAdapterFactory:
    """远程适配器工厂

    根据配置类型自动选择合适的适配器
    """

    @staticmethod
    def create(
        config: ConnectionConfig,
        credential: Optional[AuthCredential] = None,
        timeout: int = 30,
    ) -> RemoteAdapter:
        """创建远程适配器

        Args:
            config: 连接配置
            credential: 认证凭据
            timeout: 超时时间

        Returns:
            远程适配器实例

        Raises:
            ValueError: 配置无效
        """
        # 判断连接类型
        if config.base_url:
            # HTTP API 模式 (AIO Sandbox)
            return SandboxClient(
                config=config,
                timeout=timeout,
                verify_ssl=config.verify_ssl,
            )
        elif config.host:
            # SSH 模式
            return SSHClient(
                config=config,
                credential=credential,
                timeout=timeout,
            )
        else:
            raise ValueError("Invalid connection config: must specify either host or base_url")

    @staticmethod
    def create_sandbox_client(
        base_url: str,
        timeout: int = 30,
        verify_ssl: bool = True,
    ) -> SandboxClient:
        """创建 AIO Sandbox 客户端

        Args:
            base_url: AIO Sandbox 基础 URL
            timeout: 超时时间
            verify_ssl: 是否验证 SSL

        Returns:
            AIO Sandbox 客户端
        """
        config = ConnectionConfig(
            host=None,  # 不使用 SSH
            port=8080,
            username=None,
            use_ssl=False,
            verify_ssl=verify_ssl,
            base_url=base_url,
        )
        return SandboxClient(config=config, timeout=timeout, verify_ssl=verify_ssl)

    @staticmethod
    def create_ssh_client(
        host: str,
        port: int = 22,
        username: str = None,
        credential: Optional[AuthCredential] = None,
        timeout: int = 30,
        use_ssl: bool = False,
        verify_ssl: bool = True,
    ) -> SSHClient:
        """创建 SSH 客户端

        Args:
            host: 服务器地址
            port: 端口
            username: 用户名
            credential: 认证凭据
            timeout: 超时时间
            use_ssl: 是否使用 SSL
            verify_ssl: 是否验证 SSL

        Returns:
            SSH 客户端
        """
        config = ConnectionConfig(
            host=host,
            port=port,
            username=username or "",
            use_ssl=use_ssl,
            verify_ssl=verify_ssl,
        )
        return SSHClient(config=config, credential=credential, timeout=timeout)

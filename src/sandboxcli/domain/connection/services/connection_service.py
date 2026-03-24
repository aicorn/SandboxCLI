"""连接领域服务"""
from ...shared import Result
from ..aggregates import ConnectionAggregate
from ..entities import Connection
from ..value_objects import AuthCredential, ConnectionConfig


class ConnectionService:
    """连接管理服务"""

    @staticmethod
    def create_connection(
        host: str,
        port: int,
        username: str,
        password: str = None,
        private_key: str = None,
        token: str = None,
        use_ssl: bool = True,
    ) -> Result[ConnectionAggregate]:
        """创建连接"""
        try:
            config = ConnectionConfig(
                host=host,
                port=port,
                username=username,
                use_ssl=use_ssl,
            )

            if password:
                credential = AuthCredential(
                    auth_type="password",
                    username=username,
                    password=password,
                )
            elif private_key:
                credential = AuthCredential(
                    auth_type="key",
                    username=username,
                    private_key=private_key,
                )
            elif token:
                credential = AuthCredential(
                    auth_type="token",
                    username=username,
                    token=token,
                )
            else:
                credential = None

            connection = Connection.create(config=config, credential=credential)
            return Result.ok(ConnectionAggregate(connection))

        except Exception as e:
            return Result.fail(f"Failed to create connection: {str(e)}")

    @staticmethod
    def validate_connection_config(
        host: str,
        port: int,
        username: str,
    ) -> Result[ConnectionConfig]:
        """验证连接配置"""
        try:
            config = ConnectionConfig(host=host, port=port, username=username)
            return Result.ok(config)
        except Exception as e:
            return Result.fail(f"Invalid connection config: {str(e)}")

    @staticmethod
    def validate_credential(
        auth_type: str,
        username: str = None,
        password: str = None,
        private_key: str = None,
        token: str = None,
    ) -> Result[AuthCredential]:
        """验证认证凭据"""
        try:
            credential = AuthCredential(
                auth_type=auth_type,
                username=username,
                password=password,
                private_key=private_key,
                token=token,
            )
            
            if not credential.has_credential():
                return Result.fail("No credential provided")
            
            return Result.ok(credential)
        except Exception as e:
            return Result.fail(f"Invalid credential: {str(e)}")

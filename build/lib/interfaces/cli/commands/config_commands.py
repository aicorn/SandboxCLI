"""配置CLI命令"""
import click

from ....application.commands.configuration import (
    InteractiveConfigCommand,
    UpdateConfigCommand,
)
from ....application.queries.configuration import GetConfigQuery


@click.group(name="config")
def config_group():
    """配置管理命令组"""
    pass


@config_group.command(name="get")
@click.option("--config-id", default="default", help="配置ID")
@click.option("--include-sensitive", is_flag=True, help="包含敏感信息")
def get_config(config_id: str, include_sensitive: bool):
    """获取配置"""
    query = GetConfigQuery(
        config_id=config_id,
        include_sensitive=include_sensitive,
    )
    click.echo(f"Getting config: {config_id}")
    # TODO: 调用应用服务


@config_group.command(name="set")
@click.option("--host", help="服务器地址")
@click.option("--port", type=int, help="服务器端口")
@click.option("--username", help="用户名")
@click.option("--timeout", type=int, help="超时时间(秒)")
@click.option("--key", help="自定义配置键")
@click.option("--value", help="自定义配置值")
def update_config(host, port, username, timeout, key, value):
    """更新配置"""
    command = UpdateConfigCommand(
        server_host=host,
        server_port=port,
        username=username,
        timeout=timeout,
        config_key=key,
        config_value=value,
    )
    click.echo("Updating config...")
    # TODO: 调用应用服务


@config_group.command(name="interactive")
@click.option("--config-id", default="default", help="配置ID")
def interactive_config(config_id: str):
    """交互式配置"""
    command = InteractiveConfigCommand(config_id=config_id)
    click.echo("Starting interactive config mode...")
    # TODO: 调用应用服务


__all__ = ["config_group"]

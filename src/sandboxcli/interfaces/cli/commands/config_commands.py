"""配置CLI命令"""
import click

from sandboxcli.application.commands.configuration import (
    InteractiveConfigCommand,
    UpdateConfigCommand,
)
from sandboxcli.application.queries.configuration import GetConfigQuery
from sandboxcli.infrastructure.persistence.config.config_repository import ConfigRepository
from sandboxcli.domain.configuration.aggregates.config_aggregate import ConfigAggregate
from sandboxcli.domain.configuration.services.config_service import ConfigService
from sandboxcli.application.services.configuration_app_service import ConfigurationAppService


def _get_config_service():
    """获取配置应用服务"""
    repository = ConfigRepository()
    config = repository.load()
    config_aggregate = ConfigAggregate(config)
    return ConfigurationAppService(config_aggregate), repository


def _save_config_service(config_aggregate, repository):
    """保存配置"""
    repository.save(config_aggregate.config)


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
    service, _ = _get_config_service()
    result = service.get_config(query)
    if result.is_success:
        import json
        click.echo(json.dumps(result.value, indent=2, ensure_ascii=False))
    else:
        click.echo(f"Error: {result.error}", err=True)


@config_group.command(name="set")
@click.option("--host", help="服务器地址 (SSH模式)")
@click.option("--port", type=int, help="服务器端口")
@click.option("--username", help="用户名")
@click.option("--timeout", type=int, help="超时时间(秒)")
@click.option("--key", help="自定义配置键")
@click.option("--value", help="自定义配置值")
@click.option("--base-url", help="AIO Sandbox HTTP API 地址 (如 http://your-aio-server:8080)")
def update_config(host, port, username, timeout, key, value, base_url):
    """更新配置"""
    command = UpdateConfigCommand(
        server_host=host,
        server_port=port,
        username=username,
        timeout=timeout,
        config_key=key,
        config_value=value,
        base_url=base_url,
    )
    
    service, repository = _get_config_service()
    result = service.update_config(command)
    
    if result.is_success:
        _save_config_service(service._config, repository)
        click.echo("Config updated successfully!")
        if base_url:
            click.echo(f"  Base URL: {base_url}")
        if host:
            click.echo(f"  Host: {host}")
        if port:
            click.echo(f"  Port: {port}")
        if username:
            click.echo(f"  Username: {username}")
    else:
        click.echo(f"Error: {result.error}", err=True)


@config_group.command(name="interactive")
@click.option("--config-id", default="default", help="配置ID")
def interactive_config(config_id: str):
    """交互式配置"""
    service, repository = _get_config_service()
    
    click.echo("=== SandboxCLI 交互式配置 ===")
    click.echo("")
    
    # 配置 AIO Sandbox HTTP API 地址
    base_url = click.prompt(
        "AIO Sandbox HTTP API 地址 (如 http://your-aio-server:8080)",
        default="",
        show_default=False,
    )
    
    # 配置用户名
    username = click.prompt(
        "用户名",
        default="",
        show_default=False,
    )
    
    # 配置超时时间
    timeout = click.prompt(
        "超时时间(秒)",
        default=30,
        type=int,
    )
    
    # 构建更新命令
    command = UpdateConfigCommand(
        config_id=config_id,
        base_url=base_url if base_url else None,
        username=username if username else None,
        timeout=timeout,
    )
    
    # 更新配置
    result = service.update_config(command)
    
    if result.is_success:
        _save_config_service(service._config, repository)
        click.echo("")
        click.echo("配置已保存!")
    else:
        click.echo(f"Error: {result.error}", err=True)


@config_group.command(name="set-git")
@click.option("--url", help="Git仓库URL")
@click.option("--auth-type", type=click.Choice(["none", "https", "ssh"]), help="认证方式")
@click.option("--ssh-key-path", help="SSH密钥文件路径")
@click.option("--username", help="Git用户名")
@click.option("--email", help="Git邮箱")
@click.option("--password", help="Git密码(HTTPS认证时使用)")
@click.option("--default-branch", default="main", help="默认分支名")
def set_git_config(url, auth_type, ssh_key_path, username, email, password, default_branch):
    """Git配置管理
    
    设置Git仓库信息。
    
    示例:
        sandboxcli config set-git --url https://github.com/user/repo.git --auth-type https --username youruser
    """
    from sandboxcli.domain.configuration.value_objects import (
        GitConfig, GitRepoUrl, GitAuthType, SSHKey, GitCredential
    )
    
    service, repository = _get_config_service()
    
    # 设置Git配置
    # 获取现有Git配置或创建新的
    current_git_config = service.get_git_config() or GitConfig.empty()
    
    # 更新配置
    if url:
        new_url = GitRepoUrl(url=url)
    else:
        new_url = current_git_config.repo_url
    
    if auth_type:
        new_auth_type = GitAuthType(auth_type=auth_type)
    else:
        new_auth_type = current_git_config.auth_type
    
    if ssh_key_path:
        new_ssh_key = SSHKey.from_path(ssh_key_path)
    else:
        new_ssh_key = current_git_config.ssh_key
    
    if username or email or password:
        new_credential = GitCredential.create(
            username=username or current_git_config.credential.username or "",
            email=email or current_git_config.credential.email or "",
            password=password,
        )
    else:
        new_credential = current_git_config.credential
    
    # 创建新的GitConfig
    new_git_config = GitConfig(
        repo_url=new_url,
        auth_type=new_auth_type,
        ssh_key=new_ssh_key,
        credential=new_credential,
        default_branch=default_branch or current_git_config.default_branch,
        description="Git配置",
    )
    
    # 更新配置
    service.set_git_config(new_git_config)
    
    # 保存配置
    _save_config_service(service._config, repository)
    
    click.echo("Git配置已保存!")
    click.echo(f"  仓库URL: {new_git_config.repo_url.url}")
    click.echo(f"  认证方式: {new_git_config.auth_type.auth_type.value}")
    if new_git_config.ssh_key.key_path:
        click.echo(f"  SSH密钥: {new_git_config.ssh_key.key_path}")
    if new_git_config.credential.username:
        click.echo(f"  用户名: {new_git_config.credential.username}")
    if new_git_config.credential.email:
        click.echo(f"  邮箱: {new_git_config.credential.email}")


__all__ = ["config_group"]

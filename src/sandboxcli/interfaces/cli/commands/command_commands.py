"""命令CLI命令"""
import click

from sandboxcli.application.commands.command import ExecuteCommandCommand
from sandboxcli.application.services.command_app_service import CommandAppService
from sandboxcli.interfaces.cli.presenter.output_formatter import OutputFormatter


# 创建应用服务实例
_command_service = CommandAppService()


@click.group(name="command")
def command_group():
    """命令执行命令组"""
    pass


@command_group.command(name="exec")
@click.argument("command")
@click.option("--args", multiple=True, help="命令参数")
@click.option("--cwd", "--working-directory", help="工作目录")
@click.option("--timeout", type=int, help="超时时间(秒)")
@click.option("--env", multiple=True, help="环境变量 (KEY=VALUE格式)")
@click.option("-v", "--verbose", is_flag=True, help="显示详细信息")
def execute_command(command: str, args: tuple, cwd: str, timeout: int, env: tuple, verbose: bool):
    """执行远程命令"""
    env_dict = {}
    for e in env:
        if "=" in e:
            key, value = e.split("=", 1)
            env_dict[key] = value

    cmd = ExecuteCommandCommand(
        command=command,
        args=list(args),
        working_directory=cwd,
        timeout=timeout,
        env=env_dict if env_dict else None,
    )

    result = _command_service.execute_command(cmd)

    if result.is_failure():
        click.echo(f"Error: {result.error}", err=True)
        raise click.Abort()

    output = result.value
    click.echo(OutputFormatter.format_command_output(output, verbose=verbose))


@command_group.command(name="run")
@click.argument("cmd")
@click.option("-v", "--verbose", is_flag=True, help="显示详细信息")
def run_command(cmd: str, verbose: bool):
    """快速执行命令"""
    # 将命令字符串解析为命令和参数
    parts = cmd.strip().split()
    command = parts[0] if parts else ""
    args = parts[1:] if len(parts) > 1 else []

    execute_cmd = ExecuteCommandCommand(
        command=command,
        args=args,
    )

    result = _command_service.execute_command(execute_cmd)

    if result.is_failure():
        click.echo(f"Error: {result.error}", err=True)
        raise click.Abort()

    output = result.value
    click.echo(OutputFormatter.format_command_output(output, verbose=verbose))


__all__ = ["command_group"]

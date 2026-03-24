"""命令CLI命令"""
import click

from ....application.commands.command import ExecuteCommandCommand


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
def execute_command(command: str, args: tuple, cwd: str, timeout: int, env: tuple):
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
    click.echo(f"Executing: {cmd.get_full_command()}")
    # TODO: 调用应用服务


@command_group.command(name="run")
@click.argument("cmd")
def run_command(cmd: str):
    """快速执行命令"""
    click.echo(f"Running: {cmd}")
    # TODO: 调用应用服务


__all__ = ["command_group"]

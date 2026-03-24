"""CLI主入口"""
import click

from ..interfaces.cli.commands import command_group, config_group, git_group


@click.group()
@click.version_option(version="0.0.1")
def cli():
    """SandboxCLI - 远程沙盒系统控制工具"""
    pass


# 注册子命令组
cli.add_command(config_group)
cli.add_command(command_group)
cli.add_command(git_group)


if __name__ == "__main__":
    cli()

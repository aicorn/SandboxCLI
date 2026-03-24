"""Git CLI命令"""
import click

from ....application.commands.git import PullCodeCommand, SwitchBranchCommand
from ....application.queries.git import GetBranchesQuery, GetGitLogQuery, GetGitStatusQuery


@click.group(name="git")
def git_group():
    """Git管理命令组"""
    pass


@git_group.command(name="status")
@click.option("--repo-path", default=".", help="仓库路径")
def get_git_status(repo_path: str):
    """获取Git状态"""
    query = GetGitStatusQuery(repo_path=repo_path)
    click.echo(f"Getting git status for: {repo_path}")
    # TODO: 调用应用服务


@git_group.command(name="log")
@click.option("--repo-path", default=".", help="仓库路径")
@click.option("--max-count", default=10, help="最大日志数量")
@click.option("--branch", help="分支名称")
def get_git_log(repo_path: str, max_count: int, branch: str):
    """获取Git日志"""
    query = GetGitLogQuery(
        repo_path=repo_path,
        max_count=max_count,
        branch=branch,
    )
    click.echo(f"Getting git log for: {repo_path}")
    # TODO: 调用应用服务


@git_group.command(name="branch")
@click.option("--repo-path", default=".", help="仓库路径")
@click.option("--include-remote/--no-remote", default=True, help="包含远程分支")
def get_branches(repo_path: str, include_remote: bool):
    """获取分支列表"""
    query = GetBranchesQuery(
        repo_path=repo_path,
        include_remote=include_remote,
    )
    click.echo(f"Getting branches for: {repo_path}")
    # TODO: 调用应用服务


@git_group.command(name="switch")
@click.argument("branch_name")
@click.option("--repo-path", default=".", help="仓库路径")
@click.option("--create/--no-create", default=False, help="创建新分支")
def switch_branch(branch_name: str, repo_path: str, create: bool):
    """切换分支"""
    command = SwitchBranchCommand(
        branch_name=branch_name,
        repo_path=repo_path,
        create_new=create,
    )
    click.echo(f"Switching to branch: {branch_name}")
    # TODO: 调用应用服务


@git_group.command(name="pull")
@click.option("--repo-path", default=".", help="仓库路径")
@click.option("--branch", default="HEAD", help="分支名称")
@click.option("--rebase/--no-rebase", default=False, help="使用rebase")
def pull_code(repo_path: str, branch: str, rebase: bool):
    """拉取代码"""
    command = PullCodeCommand(
        repo_path=repo_path,
        branch=branch,
        rebase=rebase,
    )
    click.echo(f"Pulling code for: {repo_path}")
    # TODO: 调用应用服务


__all__ = ["git_group"]

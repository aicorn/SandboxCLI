"""Git CLI命令"""
import click

from sandboxcli.application.commands.git import CloneRepositoryCommand, PullCodeCommand, SwitchBranchCommand
from sandboxcli.application.queries.git import GetBranchesQuery, GetGitLogQuery, GetGitStatusQuery
from sandboxcli.application.services.git_app_service import GitAppService
from sandboxcli.interfaces.cli.presenter.output_formatter import OutputFormatter

# 创建应用服务实例
_git_service = GitAppService()


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


@git_group.command(name="clone")
@click.argument("url")
@click.option("--target-dir", "-d", help="目标目录")
@click.option("--branch", "-b", help="指定分支")
@click.option("--depth", type=int, help="浅克隆深度")
@click.option("--recursive/--no-recursive", default=False, help="递归克隆子模块")
@click.option("--use-config-git/--no-use-config-git", default=True, help="使用配置中的Git凭据")
def clone_repository(url: str, target_dir: str, branch: str, depth: int, recursive: bool, use_config_git: bool):
    """克隆Git仓库
    
    克隆远程Git仓库到本地。
    
    示例:
        sandboxcli git clone https://github.com/user/repo.git
        sandboxcli git clone https://github.com/user/repo.git -d /path/to/dir
        sandboxcli git clone https://github.com/user/repo.git -b develop --depth 1
    """
    command = CloneRepositoryCommand(
        url=url,
        target_dir=target_dir,
        branch=branch,
        depth=depth,
        recursive=recursive,
        use_config_git=use_config_git,
    )
    
    # 调用应用服务执行克隆
    result = _git_service.execute_clone(command)
    
    if result.is_failure():
        click.echo(f"Error: {result.error}", err=True)
        raise click.ClickException(result.error)
    
    clone_result = result.value
    click.echo(f"Successfully cloned to: {clone_result.cloned_path}")


__all__ = ["git_group"]

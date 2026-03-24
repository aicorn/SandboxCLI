"""Git CLI命令"""
import click

from sandboxcli.application.commands.git import CloneRepositoryCommand, PullCodeCommand, SwitchBranchCommand
from sandboxcli.application.queries.git import GetBranchesQuery, GetGitLogQuery, GetGitStatusQuery


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


@git_group.command(name="config")
def get_git_config():
    """获取Git配置
    
    获取当前配置的Git仓库信息。
    
    示例:
        sandboxcli git config
    """
    from sandboxcli.infrastructure.persistence.config.config_repository import ConfigRepository
    from sandboxcli.domain.configuration.aggregates.config_aggregate import ConfigAggregate
    from sandboxcli.application.services.configuration_app_service import ConfigurationAppService
    
    repository = ConfigRepository()
    config = repository.load()
    config_aggregate = ConfigAggregate(config)
    service = ConfigurationAppService(config_aggregate)
    
    git_config = service.get_git_config()
    if git_config:
        import json
        click.echo(json.dumps(git_config.to_dict(), indent=2, ensure_ascii=False))
    else:
        click.echo("Git配置未设置")


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
    
    click.echo(f"Cloning repository: {url}")
    if target_dir:
        click.echo(f"Target directory: {target_dir}")
    if branch:
        click.echo(f"Branch: {branch}")
    if depth:
        click.echo(f"Depth: {depth}")
    if recursive:
        click.echo("Recursive: Yes")
    
    # TODO: 调用应用服务执行克隆
    # git_app_service = GitAppService()
    # result = git_app_service.execute_clone(command)
    # if result.is_success():
    #     click.echo(f"Successfully cloned to: {result.value.cloned_path}")
    # else:
    #     click.echo(f"Error: {result.error}", err=True)


__all__ = ["git_group"]

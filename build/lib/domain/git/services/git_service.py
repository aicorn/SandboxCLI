"""Git领域服务"""
from ...shared import Result
from ..aggregates import RepositoryAggregate
from ..entities import Repository
from ..value_objects import BranchInfo, GitLogEntry, GitStatus


class GitService:
    """Git管理服务"""

    @staticmethod
    def create_repository(path: str) -> RepositoryAggregate:
        """创建Git仓库"""
        repository = Repository(path=path)
        return RepositoryAggregate(repository)

    @staticmethod
    def validate_branch_name(branch_name: str) -> Result[str]:
        """验证分支名称"""
        if not branch_name or not branch_name.strip():
            return Result.fail("Branch name cannot be empty")
        
        invalid_chars = ["~", "^", ":", "\\", " ", "#", "["]
        for char in invalid_chars:
            if char in branch_name:
                return Result.fail(f"Branch name contains invalid character: {char}")
        
        if branch_name.startswith("/") or branch_name.endswith("/"):
            return Result.fail("Branch name cannot start or end with /")
        
        if branch_name == "HEAD":
            return Result.fail("Branch name cannot be HEAD")
        
        return Result.ok(branch_name.strip())

    @staticmethod
    def validate_repo_path(path: str) -> Result[str]:
        """验证仓库路径"""
        if not path or not path.strip():
            return Result.fail("Repository path cannot be empty")
        return Result.ok(path.strip())

    @staticmethod
    def parse_branch_name(branch_ref: str) -> str:
        """解析分支引用为分支名"""
        prefixes = ["refs/heads/", "origin/", "refs/remotes/"]
        for prefix in prefixes:
            if branch_ref.startswith(prefix):
                return branch_ref[len(prefix):]
        return branch_ref

    @staticmethod
    def is_local_branch(branch_name: str) -> bool:
        """判断是否为本地分支"""
        return not branch_name.startswith("origin/") and "/" not in branch_name

    @staticmethod
    def is_remote_branch(branch_name: str) -> bool:
        """判断是否为远程分支"""
        return branch_name.startswith("origin/") or "/" in branch_name

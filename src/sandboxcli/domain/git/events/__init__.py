"""Git上下文领域事件"""
from ...shared import DomainEvent


class BranchSwitchedEvent(DomainEvent):
    """分支切换事件"""

    repo_path: str
    from_branch: str
    to_branch: str

    def get_event_type(self) -> str:
        return "BranchSwitchedEvent"

    def get_aggregate_id(self) -> str:
        return self.repo_path


class CodePulledEvent(DomainEvent):
    """代码拉取事件"""

    repo_path: str
    branch: str
    new_commits: int = 0
    new_files: int = 0

    def get_event_type(self) -> str:
        return "CodePulledEvent"

    def get_aggregate_id(self) -> str:
        return self.repo_path


class RepositoryClonedEvent(DomainEvent):
    """仓库克隆成功事件"""

    operation_id: str
    repo_url: str
    cloned_path: str
    branch: str
    commit_hash: str

    def get_event_type(self) -> str:
        return "RepositoryClonedEvent"

    def get_aggregate_id(self) -> str:
        return self.operation_id


class CloneFailedEvent(DomainEvent):
    """仓库克隆失败事件"""

    operation_id: str
    repo_url: str
    error: str

    def get_event_type(self) -> str:
        return "CloneFailedEvent"

    def get_aggregate_id(self) -> str:
        return self.operation_id


class RepositoryCleanedEvent(DomainEvent):
    """仓库清理成功事件"""

    operation_id: str
    repo_path: str
    cleanup_type: str
    cleaned_files: list
    deleted_branches: list
    deleted_tags: list

    def get_event_type(self) -> str:
        return "RepositoryCleanedEvent"

    def get_aggregate_id(self) -> str:
        return self.operation_id


class CleanupFailedEvent(DomainEvent):
    """仓库清理失败事件"""

    operation_id: str
    repo_path: str
    cleanup_type: str
    error: str

    def get_event_type(self) -> str:
        return "CleanupFailedEvent"

    def get_aggregate_id(self) -> str:
        return self.operation_id


__all__ = [
    "BranchSwitchedEvent", 
    "CodePulledEvent", 
    "RepositoryClonedEvent", 
    "CloneFailedEvent",
    "RepositoryCleanedEvent",
    "CleanupFailedEvent",
]

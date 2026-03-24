"""Git配置值对象"""
from typing import Optional, Tuple

from pydantic import BaseModel

from .git_auth_type import GitAuthType, GitAuthTypeEnum
from .git_credential import GitCredential
from .git_repo_url import GitRepoUrl
from .ssh_key import SSHKey


class GitConfig(BaseModel):
    """Git配置值对象
    
    聚合所有Git相关配置的value object。
    用于在配置上下文中存储Git操作所需的配置信息。
    """
    repo_url: GitRepoUrl = GitRepoUrl.empty()
    auth_type: GitAuthType = GitAuthType.none()
    ssh_key: SSHKey = SSHKey.empty()
    credential: GitCredential = GitCredential.empty()
    default_branch: Optional[str] = "main"
    description: Optional[str] = "Git配置"
    
    model_config = {"frozen": True}
    
    def is_configured(self) -> bool:
        """是否已配置有效的仓库URL"""
        return not self.repo_url.is_empty()
    
    def needs_ssh_key(self) -> bool:
        """是否需要SSH密钥"""
        return self.auth_type.is_ssh() and self.ssh_key.is_empty()
    
    def needs_credential(self) -> bool:
        """是否需要凭据"""
        return self.auth_type.is_https() and self.credential.is_empty()
    
    def validate_for_clone(self) -> Tuple[bool, Optional[str]]:
        """验证配置是否可用于克隆操作
        
        Returns:
            tuple: (是否有效, 错误信息)
        """
        if self.repo_url.is_empty():
            return False, "仓库URL未设置"
        
        if self.auth_type.is_ssh() and self.ssh_key.is_empty():
            return False, "SSH认证方式需要配置SSH密钥"
        
        if self.auth_type.is_https() and self.credential.is_empty():
            return False, "HTTPS认证方式需要配置用户名和密码"
        
        return True, None
    
    def __str__(self) -> str:
        return f"GitConfig(url={self.repo_url.url}, auth={self.auth_type.auth_type.value})"
    
    def __repr__(self) -> str:
        return f"GitConfig(repo_url={self.repo_url.url}, auth_type={self.auth_type.auth_type.value}, default_branch={self.default_branch})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "repo_url": self.repo_url.to_dict(),
            "auth_type": self.auth_type.to_dict(),
            "ssh_key": self.ssh_key.to_dict(),
            "credential": self.credential.to_dict(),
            "default_branch": self.default_branch,
            "description": self.description,
        }
    
    @staticmethod
    def empty() -> "GitConfig":
        """创建空Git配置"""
        return GitConfig(
            repo_url=GitRepoUrl.empty(),
            auth_type=GitAuthType.none(),
            ssh_key=SSHKey.empty(),
            credential=GitCredential.empty(),
            default_branch="main",
            description="未配置的Git"
        )
    
    @staticmethod
    def from_url(url: str, auth_type: GitAuthTypeEnum = GitAuthTypeEnum.NONE) -> "GitConfig":
        """从URL创建Git配置"""
        return GitConfig(
            repo_url=GitRepoUrl(url=url),
            auth_type=GitAuthType(auth_type=auth_type),
            default_branch="main",
            description=f"Git配置: {url}"
        )

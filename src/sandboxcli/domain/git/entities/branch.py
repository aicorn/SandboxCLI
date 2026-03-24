"""Git分支实体"""
from pydantic import BaseModel, Field

from ..value_objects import BranchInfo


class Branch(BaseModel):
    """Git分支实体"""
    name: str
    info: BranchInfo = Field(default_factory=BranchInfo)

    model_config = {"frozen": True}

    @property
    def branch_name(self) -> str:
        """获取分支名称"""
        return self.name

    @classmethod
    def create(cls, name: str, is_current: bool = False) -> "Branch":
        """创建分支"""
        info = BranchInfo(name=name, is_current=is_current)
        return cls(name=name, info=info)

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "name": self.name,
            "info": self.info.to_dict(),
        }

    def __str__(self) -> str:
        return self.name

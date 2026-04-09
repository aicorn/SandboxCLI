"""配置实体"""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, PrivateAttr

from ..value_objects import ConfigItem, ServerAddress, Timeout, SandboxType, VerboseConfig, WorkingDirectory


class Config(BaseModel):
    """配置实体 - 管理CLI配置"""
    id: str = Field(default="default")
    server_address: Optional[ServerAddress] = None
    timeout: Timeout = Field(default_factory=Timeout.default)
    username: Optional[str] = None
    sandbox_type: SandboxType = Field(default_factory=SandboxType.default_aio)  # 沙盒类型
    working_directory: WorkingDirectory = Field(default_factory=WorkingDirectory.default)  # 工作目录
    verbose_config: VerboseConfig = Field(default_factory=VerboseConfig.default)  # Verbose调试配置
    items: Dict[str, ConfigItem] = Field(default_factory=dict, exclude=True)

    model_config = {"frozen": False}

    def get_item(self, key: str) -> Optional[ConfigItem]:
        """获取配置项"""
        return self.items.get(key)

    def get_all_items(self) -> List[ConfigItem]:
        """获取所有配置项"""
        return list(self.items.values())

    def set_item(self, key: str, value: any, description: Optional[str] = None) -> None:
        """设置配置项"""
        item = ConfigItem(
            key=key,
            value=value,
            description=description,
        )
        self.items[key] = item

    def remove_item(self, key: str) -> bool:
        """移除配置项"""
        if key in self.items:
            del self.items[key]
            return True
        return False

    def has_item(self, key: str) -> bool:
        """检查配置项是否存在"""
        return key in self.items

    def update_server_address(
        self,
        host: str = None,
        port: int = 22,
        base_url: str = None,
    ) -> None:
        """更新服务器地址

        Args:
            host: 服务器主机名 (SSH 模式)
            port: 服务器端口 (SSH 模式，默认 22)
            base_url: AIO Sandbox HTTP API 地址 (HTTP 模式)
        """
        self.server_address = ServerAddress(host=host, port=port, base_url=base_url)

    def update_timeout(self, seconds: int) -> None:
        """更新超时配置"""
        self.timeout = Timeout.from_seconds(seconds)

    def update_username(self, username: str) -> None:
        """更新用户名"""
        self.username = username

    def update_sandbox_type(self, sandbox_type: str, description: Optional[str] = None) -> None:
        """更新沙盒类型

        Args:
            sandbox_type: 沙盒类型 ("aio", "ssh", "custom")
            description: 沙盒类型描述
        """
        from ..value_objects.sandbox_type import SandboxTypeEnum
        self.sandbox_type = SandboxType(
            type=SandboxTypeEnum(sandbox_type),
            description=description,
        )

    def update_working_directory(self, path: str) -> None:
        """更新工作目录

        Args:
            path: 工作目录路径
        """
        self.working_directory = WorkingDirectory.from_path(path)

    def update_verbose_config(
        self,
        level: str = None,
        enable_timestamp: bool = None,
        enable_color: bool = None,
    ) -> None:
        """更新Verbose调试配置

        Args:
            level: 调试级别 (off/error/info/debug)
            enable_timestamp: 是否显示时间戳
            enable_color: 是否使用彩色输出
        """
        if level is not None:
            self.verbose_config = VerboseConfig.from_level(level)
        elif enable_timestamp is not None or enable_color is not None:
            # 部分更新
            new_config = self.verbose_config.to_dict()
            if enable_timestamp is not None:
                new_config["enable_timestamp"] = enable_timestamp
            if enable_color is not None:
                new_config["enable_color"] = enable_color
            self.verbose_config = VerboseConfig.from_dict(new_config)

    def get_verbose_config(self) -> VerboseConfig:
        """获取Verbose配置

        Returns:
            VerboseConfig 对象
        """
        return self.verbose_config

    def get_working_directory_path(self) -> str:
        """获取工作目录路径

        Returns:
            工作目录路径字符串
        """
        return self.working_directory.path

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "server_address": str(self.server_address) if self.server_address else None,
            "timeout": str(self.timeout),
            "username": self.username,
            "sandbox_type": str(self.sandbox_type),
            "working_directory": str(self.working_directory),
            "verbose_config": self.verbose_config.to_dict(),
            "items": [item.to_dict() for item in self.items.values()],
        }

    def __str__(self) -> str:
        return f"Config(id='{self.id}')"

    def __repr__(self) -> str:
        return f"Config(id='{self.id}', server_address={self.server_address}, timeout={self.timeout}, sandbox_type={self.sandbox_type})"

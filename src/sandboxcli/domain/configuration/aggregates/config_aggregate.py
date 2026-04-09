"""配置聚合"""
from typing import Any, Dict, List, Optional

from ..entities.config import Config
from ..value_objects import ConfigItem
from ..events.working_directory_changed_event import WorkingDirectoryChangedEvent


class ConfigAggregate:
    """配置聚合根"""

    def __init__(self, config: Config):
        self._config = config
        self._pending_events: List[WorkingDirectoryChangedEvent] = []

    @property
    def config(self) -> Config:
        """获取配置实体"""
        return self._config

    @property
    def config_id(self) -> str:
        """获取配置ID"""
        return self._config.id

    @property
    def pending_events(self) -> List[WorkingDirectoryChangedEvent]:
        """获取待处理的事件"""
        return self._pending_events

    def get_all_items(self) -> List[ConfigItem]:
        """获取所有配置项"""
        return self._config.get_all_items()

    def get_item(self, key: str) -> Optional[ConfigItem]:
        """获取指定配置项"""
        return self._config.get_item(key)

    def update_item(self, key: str, value: Any, description: Optional[str] = None) -> None:
        """更新配置项"""
        self._config.set_item(key, value, description)

    def remove_item(self, key: str) -> bool:
        """移除配置项"""
        return self._config.remove_item(key)

    def update_working_directory(self, path: str) -> WorkingDirectoryChangedEvent:
        """更新工作目录

        Args:
            path: 新的工作目录路径

        Returns:
            WorkingDirectoryChangedEvent 事件
        """
        old_path = self._config.get_working_directory_path()
        self._config.update_working_directory(path)
        new_path = self._config.get_working_directory_path()

        # 创建并存储事件
        event = WorkingDirectoryChangedEvent.create(
            old_path=old_path,
            new_path=new_path,
            changed_by="user"
        )
        self._pending_events.append(event)
        return event

    def get_working_directory(self) -> str:
        """获取当前工作目录

        Returns:
            工作目录路径
        """
        return self._config.get_working_directory_path()

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
        self._config.update_verbose_config(
            level=level,
            enable_timestamp=enable_timestamp,
            enable_color=enable_color,
        )

    def get_verbose_config(self):
        """获取Verbose配置

        Returns:
            VerboseConfig 对象
        """
        return self._config.get_verbose_config()

    def create_snapshot(self) -> Dict:
        """创建配置快照"""
        return self._config.to_dict()

    def restore_from_snapshot(self, snapshot: Dict) -> None:
        """从快照恢复配置"""
        if "server_address" in snapshot and snapshot["server_address"]:
            host, port = snapshot["server_address"].rsplit(":", 1)
            self._config.update_server_address(host, int(port))
        if "timeout" in snapshot:
            self._config.update_timeout(int(snapshot["timeout"].rstrip("s")))
        if "username" in snapshot and snapshot["username"]:
            self._config.update_username(snapshot["username"])
        if "working_directory" in snapshot and snapshot["working_directory"]:
            self._config.update_working_directory(snapshot["working_directory"])
        if "verbose_config" in snapshot and snapshot["verbose_config"]:
            self._config.update_verbose_config(
                level=snapshot["verbose_config"].get("level"),
                enable_timestamp=snapshot["verbose_config"].get("enable_timestamp"),
                enable_color=snapshot["verbose_config"].get("enable_color"),
            )
        if "items" in snapshot:
            for item in snapshot["items"]:
                self._config.set_item(item["key"], item["value"], item.get("description"))

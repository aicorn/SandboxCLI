"""配置聚合"""
from typing import Any, Dict, List, Optional

from ..entities.config import Config
from ..value_objects import ConfigItem


class ConfigAggregate:
    """配置聚合根"""

    def __init__(self, config: Config):
        self._config = config

    @property
    def config(self) -> Config:
        """获取配置实体"""
        return self._config

    @property
    def config_id(self) -> str:
        """获取配置ID"""
        return self._config.id

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
        if "items" in snapshot:
            for item in snapshot["items"]:
                self._config.set_item(item["key"], item["value"], item.get("description"))

"""配置仓储实现"""
import json
import os
from pathlib import Path
from typing import Optional

from domain.configuration.entities import Config
from domain.configuration.value_objects import ServerAddress, Timeout


class ConfigRepository:
    """配置仓储 - 负责配置的持久化"""

    DEFAULT_CONFIG_PATH = "~/.sandboxcli/config.json"

    def __init__(self, config_path: Optional[str] = None):
        """初始化配置仓储

        Args:
            config_path: 配置文件路径，默认 ~/.sandboxcli/config.json
        """
        self._config_path = config_path or self.DEFAULT_CONFIG_PATH

    def _get_config_file_path(self) -> Path:
        """获取配置文件路径"""
        return Path(os.path.expanduser(self._config_path))

    def load(self) -> Config:
        """加载配置"""
        config_file = self._get_config_file_path()

        if not config_file.exists():
            return Config()

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return self._deserialize(data)
        except (json.JSONDecodeError, IOError):
            return Config()

    def save(self, config: Config) -> None:
        """保存配置"""
        config_file = self._get_config_file_path()
        config_file.parent.mkdir(parents=True, exist_ok=True)

        data = self._serialize(config)

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _serialize(self, config: Config) -> dict:
        """序列化配置"""
        data = {
            "id": config.id,
        }

        if config.server_address:
            data["server_address"] = {
                "host": config.server_address.host,
                "port": config.server_address.port,
                "base_url": config.server_address.base_url,
            }

        if config.timeout:
            data["timeout"] = {
                "seconds": config.timeout.seconds,
            }

        if config.username:
            data["username"] = config.username

        if config._items:
            data["items"] = {
                key: item.to_dict()
                for key, item in config._items.items()
            }

        return data

    def _deserialize(self, data: dict) -> Config:
        """反序列化配置"""
        config = Config(id=data.get("id", "default"))

        if "server_address" in data:
            server_data = data["server_address"]
            config.server_address = ServerAddress(
                host=server_data.get("host", ""),
                port=server_data.get("port", 22),
                base_url=server_data.get("base_url"),
            )

        if "timeout" in data:
            timeout_data = data["timeout"]
            config.timeout = Timeout(seconds=timeout_data.get("seconds", 30))

        if "username" in data:
            config.username = data["username"]

        if "items" in data:
            for key, item_data in data["items"].items():
                config.set_item(
                    key=key,
                    value=item_data.get("value"),
                    description=item_data.get("description"),
                )

        return config

    def delete(self) -> bool:
        """删除配置"""
        config_file = self._get_config_file_path()

        if config_file.exists():
            config_file.unlink()
            return True

        return False

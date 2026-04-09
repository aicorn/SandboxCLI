"""配置仓储实现"""
import json
import os
from pathlib import Path
from typing import Optional

from sandboxcli.domain.configuration.entities import Config
from sandboxcli.domain.configuration.value_objects import ServerAddress, Timeout, VerboseConfig, WorkingDirectory


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

        # 序列化 working_directory
        if config.working_directory:
            data["working_directory"] = {
                "path": config.working_directory.path,
                "isDefault": config.working_directory.isDefault,
            }

        # 序列化 verbose_config
        if config.verbose_config:
            data["verbose_config"] = {
                "level": config.verbose_config.level.value,
                "enable_timestamp": config.verbose_config.enable_timestamp,
                "enable_color": config.verbose_config.enable_color,
            }

        # 序列化items（包括git_config等自定义配置项）
        # 使用get_all_items()因为items字段有exclude=True
        all_items = config.get_all_items()
        if all_items:
            data["items"] = {}
            for item in all_items:
                data["items"][item.key] = item.to_dict()

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

        # 反序列化 working_directory
        if "working_directory" in data:
            wd_data = data["working_directory"]
            config.working_directory = WorkingDirectory(
                path=wd_data.get("path", "."),
                isDefault=wd_data.get("isDefault", True),
            )

        # 反序列化 verbose_config
        if "verbose_config" in data:
            vc_data = data["verbose_config"]
            config.verbose_config = VerboseConfig(
                level=vc_data.get("level", "off"),
                enable_timestamp=vc_data.get("enable_timestamp", True),
                enable_color=vc_data.get("enable_color", True),
            )

        if "items" in data and data["items"]:
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

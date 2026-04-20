"""Tests for ConfigItem value object"""
import pytest

from sandboxcli.domain.configuration.value_objects.config_item import ConfigItem


def test_config_item_creation():
    item = ConfigItem(key="host", value="localhost")
    assert item.key == "host"
    assert item.value == "localhost"


def test_config_item_key_stripped():
    item = ConfigItem(key="  host  ", value="localhost")
    assert item.key == "host"


def test_config_item_empty_key_raises():
    with pytest.raises(ValueError):
        ConfigItem(key="", value="localhost")


def test_config_item_blank_key_raises():
    with pytest.raises(ValueError):
        ConfigItem(key="   ", value="localhost")


def test_config_item_is_default_true():
    item = ConfigItem(key="timeout", value=30, default_value=30)
    assert item.is_default() is True


def test_config_item_is_default_false():
    item = ConfigItem(key="timeout", value=60, default_value=30)
    assert item.is_default() is False


def test_config_item_to_dict():
    item = ConfigItem(key="host", value="localhost", description="Server host", default_value="127.0.0.1")
    d = item.to_dict()
    assert d["key"] == "host"
    assert d["value"] == "localhost"
    assert d["description"] == "Server host"
    assert d["default_value"] == "127.0.0.1"


def test_config_item_str():
    item = ConfigItem(key="host", value="localhost")
    assert str(item) == "host=localhost"


def test_config_item_repr():
    item = ConfigItem(key="host", value="localhost")
    assert "host" in repr(item)
    assert "localhost" in repr(item)

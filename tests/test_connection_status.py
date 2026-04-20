"""Tests for ConnectionStatus value object"""
from sandboxcli.domain.connection.value_objects.connection_status import (
    ConnectionStatus,
    ConnectionStatusEnum,
)


def test_default_status_is_disconnected():
    status = ConnectionStatus()
    assert status.is_disconnected() is True
    assert status.is_connected() is False
    assert status.is_connecting() is False
    assert status.is_error() is False


def test_mark_connected():
    status = ConnectionStatus()
    connected = status.mark_connected("ok")
    assert connected.is_connected() is True
    assert connected.message == "ok"


def test_mark_disconnected():
    status = ConnectionStatus(status=ConnectionStatusEnum.CONNECTED)
    disconnected = status.mark_disconnected("bye")
    assert disconnected.is_disconnected() is True
    assert disconnected.message == "bye"


def test_mark_connecting():
    status = ConnectionStatus()
    connecting = status.mark_connecting("in progress")
    assert connecting.is_connecting() is True


def test_mark_error():
    status = ConnectionStatus()
    error = status.mark_error("connection refused")
    assert error.is_error() is True
    assert error.message == "connection refused"


def test_str_representation():
    status = ConnectionStatus(status=ConnectionStatusEnum.CONNECTED)
    assert str(status) == "CONNECTED"


def test_repr_representation():
    status = ConnectionStatus(status=ConnectionStatusEnum.CONNECTED, message="hello")
    r = repr(status)
    assert "CONNECTED" in r
    assert "hello" in r

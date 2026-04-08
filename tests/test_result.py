"""Tests for Result value object"""
import pytest

from sandboxcli.domain.shared.value_objects.result import Result


def test_result_ok_is_success():
    result = Result.ok(42)
    assert result.is_success is True
    assert result.value == 42
    assert result.error is None


def test_result_ok_with_message():
    result = Result.ok("data", message="done")
    assert result.is_success is True
    assert result.message == "done"


def test_result_fail_is_failure():
    result = Result.fail("something went wrong")
    assert result.is_success is False
    assert result.is_failure() is True
    assert result.error == "something went wrong"


def test_result_fail_with_message():
    result = Result.fail("err", message="context")
    assert result.message == "context"


def test_result_unwrap_success():
    result = Result.ok(99)
    assert result.unwrap() == 99


def test_result_unwrap_failure_raises():
    result = Result.fail("oops")
    with pytest.raises(ValueError, match="oops"):
        result.unwrap()


def test_result_unwrap_or_success():
    result = Result.ok(1)
    assert result.unwrap_or(0) == 1


def test_result_unwrap_or_failure():
    result = Result.fail("err")
    assert result.unwrap_or("default") == "default"


def test_result_str_ok():
    result = Result.ok(5)
    assert "Result.ok" in str(result)


def test_result_str_fail():
    result = Result.fail("bad")
    assert "Result.fail" in str(result)

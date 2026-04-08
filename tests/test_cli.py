"""Tests for CLI entry point"""
from click.testing import CliRunner

from sandboxcli.main.__main__ import cli


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "SandboxCLI" in result.output


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.0.1" in result.output


def test_config_group_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["config", "--help"])
    assert result.exit_code == 0


def test_command_group_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["command", "--help"])
    assert result.exit_code == 0


def test_git_group_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["git", "--help"])
    assert result.exit_code == 0

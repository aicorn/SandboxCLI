# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Support for working directory configuration (`--working-directory` option in `config set`)
- Added `WorkingDirectory` value object with default value "."
- Added `WorkingDirectoryChangedEvent` domain event for tracking directory changes
- Added `working_directory` field to configuration persistence
- Git clone command now executes in the configured working directory
- CLI displays working directory change message when directory is updated
- Support for connection health check on command timeout
- Added `HealthCheckResult` value object for connection health check results
- Added `ConnectionHealthCheckService` domain service for connection health detection
- Added `CommandTimeoutEvent` domain event for timeout handling
- Added `TIMEOUT_WITH_CONNECTION_FAIL` and `TIMEOUT_WITH_CONNECTION_OK` execution status
- Command execution now automatically checks connection health when timeout occurs
- Distinguish between network issues and slow command execution on timeout
- Support for configuring sandbox type (`sandbox_type` field in configuration)
- Added `SandboxType` value object with AIO, SSH, and Custom types
- Added `Config.update_sandbox_type()` method for runtime configuration updates
- Sandbox type controls which infrastructure adapter is used for command execution
- `config get` command now displays Git configuration information directly
- Added git_config field to config get output (extracted from items)
- Optimized config output format by removing description fields and simplifying single-key values
- Added sensitive information hiding (password and key_content are masked by default)
- Fixed config_repository serialization to properly save items configuration
- Removed sensitive URL exposure in CLI help text and documentation
- Added `--verbose` / `-v` option to `command exec` and `command run` commands for detailed output
- Added `has_output()` method to `CommandOutput` value object
- DDD design document now includes command error display design with ExecutionStatus states
- Added `stderr` field to `ShellExecResponse` in protocol layer
- Command error display now shows error message in concise mode (like local command execution)
- **SSH key support for Git operations - SSH keys are now automatically copied to remote sandbox**

### Fixed
- Fixed command execution output not displaying results (API response format parsing issue)
- Fixed `parse_shell_response()` to correctly extract output from `data` field
- Fixed `ShellExecResponse.from_dict()` to handle None values
- Fixed `OutputFormatter` to always display output content (even when empty)
- Fixed CLI output display issue when stdout is empty
- Fixed `Execution` entity missing `mark_timeout()` method
- Fixed `CommandAppService` not correctly handling command execution errors (exit_code != 0)
- Fixed command run with incorrect commands not showing error messages
- Fixed concise mode not showing error message when stderr is empty but stdout contains error info

## [0.0.2] - 2026-03-25

### Added
- Support for configuring AIO Sandbox HTTP API endpoint (`--base-url` parameter)
- Implemented `config set` command to set configuration
- Implemented `config get` command to view current configuration
- Implemented `config interactive` command for interactive configuration mode
- Added `ConfigService.update_base_url()` method in domain layer

### Fixed
- Fixed `Result.is_success()` method call issue (changed to property access)
- Fixed configuration serialization issue using `config.model_dump()`
- Fixed import path issues in infrastructure layer

### Changed
- Updated configuration persistence to save to `~/.sandboxcli/config.json`

## [0.0.1] - 2026-03-25

### Fixed
- Multiple Python 3.8 compatibility issues
- Fixed ModuleNotFoundError for sandboxcli.interfaces.application
- Fixed TypeError for list[str] and dict[str] type annotations
- Fixed TypeError for | union type syntax
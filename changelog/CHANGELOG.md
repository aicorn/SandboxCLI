# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
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
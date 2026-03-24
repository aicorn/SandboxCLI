# SandboxCLI DDD 设计文档

> **版本更新说明**：根据最新需求文档，增加了Git克隆仓库功能，并在配置系统中增加相应字段。

## 1. 战略设计

### 1.1 业务领域概述

SandboxCLI 是一个远程沙盒系统控制工具，用户通过 CLI 客户端连接到远程沙盒服务器进行操作。根据功能划分，系统包含以下主要业务领域：

- **配置管理**：CLI 工具的配置查看与修改，包括Git相关配置
- **指令系统**：远程命令执行（在沙盒系统内执行指令）
- **Git 管理**：Git 版本控制操作（在沙盒系统内执行 git 指令，包括克隆）
- **连接管理**：与远程沙盒的连接维护

### 1.2 Bounded Contexts 划分

系统划分为 **4 个 Bounded Contexts**：

| 上下文 | 英文名 | 职责 | 核心域 |
|--------|--------|------|--------|
| 配置上下文 | Configuration Context | CLI 配置的查看、修改、交互式修改，包括Git配置 | 支撑域 |
| 指令上下文 | Command Context | 远程指令执行 | 核心域 |
| Git 上下文 | Git Context | Git 状态、日志、分支、代码拉取、仓库克隆 | 核心域 |
| 连接上下文 | Connection Context | 与远程沙盒的连接建立、维护、通信 | 支撑域 |

### 1.3 Context Map

```
┌─────────────────────────────────────────────────────────────────┐
│                        SandboxCLI                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│   │ Configuration│     │   Command    │     │     Git      │   │
│   │   Context    │     │   Context    │     │   Context    │   │
│   └──────┬───────┘     └──────┬───────┘     └──────┬───────┘   │
│          │                    │                    │            │
│          └────────────────────┼────────────────────┘            │
│                               │                                 │
│                       ┌───────▼───────┐                         │
│                       │  Connection   │                         │
│                       │   Context     │                         │
│                       └───────────────┘                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**上下文关系说明**：

| 上下文关系 | 类型 | 说明 |
|------------|------|------|
| Configuration → Connection | Customer-Supplier | 配置上下文需要连接上下文来测试配置的有效性 |
| Command → Connection | Customer-Supplier | 指令执行依赖连接进行远程通信 |
| Git → Connection | Customer-Supplier | Git 操作依赖连接进行远程通信 |
| Configuration → Git | Customer-Supplier | Git上下文需要配置上下文提供Git操作所需的认证信息 |
| Configuration, Command, Git | Separate Ways | 三个上下文之间相互独立，无直接依赖 |

### 1.4 Ubiquitous Language 词汇表

#### 配置上下文 (Configuration Context)

| 术语 | 英文 | 定义 |
|------|------|------|
| 配置项 | ConfigItem | CLI 的单个配置项，如服务器地址、端口、超时设置等 |
| 配置值 | ConfigValue | 配置项的具体值 |
| 配置快照 | ConfigSnapshot | 某一时刻的完整配置状态 |
| 沙盒类型 | SandboxType | 使用的沙盒类型（AIO、SSH等），决定指令调用的基础设施层代码 |
| Git仓库URL | GitRepoUrl | 远程Git仓库的URL地址 |
| Git认证方式 | GitAuthType | Git认证方式（SSH、HTTPS、None） |
| SSH密钥 | SSHKey | SSH认证所需的私钥内容或路径 |
| Git用户名 | GitUsername | Git操作时的用户名 |
| Git邮箱 | GitEmail | Git操作时的邮箱 |

#### 指令上下文 (Command Context)

| 术语 | 英文 | 定义 |
|------|------|------|
| 指令 | Command | 用户输入的要执行的命令 |
| 执行结果 | ExecutionResult | 指令执行后的输出结果 |
| 执行状态 | ExecutionStatus | SUCCESS, FAILED, TIMEOUT |

#### Git 上下文 (Git Context)

| 术语 | 英文 | 定义 |
|------|------|------|
| Git 状态 | GitStatus | 工作区、暂存区、提交状态 |
| Git 日志 | GitLog | 提交历史记录 |
| 分支 | Branch | Git 分支信息 |
| 提交 | Commit | Git 提交记录 |
| 仓库 | Repository | Git 仓库 |
| 克隆操作 | CloneOperation | 克隆远程仓库到本地 |
| 克隆结果 | CloneResult | 克隆操作的结果 |

#### 连接上下文 (Connection Context)

| 术语 | 英文 | 定义 |
|------|------|------|
| 连接配置 | ConnectionConfig | 服务器地址、端口、认证信息 |
| 连接会话 | ConnectionSession | 与远程服务器的会话连接 |
| 连接状态 | ConnectionStatus | CONNECTED, DISCONNECTED, CONNECTING |

---

## 2. 战术设计

### 2.1 配置上下文 (Configuration Context)

#### Entities

| Entity | 标识 | 职责 |
|--------|------|------|
| Config | ConfigId | 管理系统配置 |

#### Value Objects

| Value Object | 职责 |
|--------------|------|
| ConfigItem | 单个配置项（键值对） |
| ServerAddress | 服务器地址（主机名/IP + 端口） |
| Timeout | 超时配置 |
| SandboxType | 沙盒类型（AIO、其他沙盒等） |
| **GitConfig** | **Git相关配置集合** |
| **GitRepoUrl** | **远程Git仓库URL** |
| **GitAuthType** | **Git认证方式（SSH/HTTPS/None）** |
| **SSHKey** | **SSH私钥** |
| **GitCredential** | **Git认证凭据（用户名+邮箱）** |

#### Aggregate

```
Config Aggregate (Aggregate Root)
├── Config (Entity, Root)
└── configItems: ConfigItem[] (Value Objects 集合)
    ├── ServerAddress
    ├── Timeout
    ├── SandboxType
    └── GitConfig (Value Object)
        ├── gitRepoUrl: GitRepoUrl
        ├── gitAuthType: GitAuthType
        ├── sshKey: SSHKey
        └── gitCredential: GitCredential
```

#### Domain Services

| Service | 职责 |
|---------|------|
| ConfigService | 配置的管理和验证 |
| GitConfigValidator | Git配置的验证 |

### 2.2 指令上下文 (Command Context)

#### Entities

| Entity | 标识 | 职责 |
|--------|------|------|
| Command | CommandId | 要执行的命令 |
| Execution | ExecutionId | 命令执行记录 |

#### Value Objects

| Value Object | 职责 |
|--------------|------|
| CommandInput | 命令输入（命令字符串、参数） |
| CommandOutput | 命令输出（标准输出、错误输出） |
| ExecutionStatus | 执行状态（成功/失败/超时） |
| Timestamp | 时间戳 |

#### Aggregates

```
Command Aggregate (Aggregate Root)
├── Command (Entity, Root)
└── input: CommandInput (Value Object)

Execution Aggregate (Aggregate Root)
├── Execution (Entity, Root)
├── input: CommandInput (Value Object)
├── output: CommandOutput (Value Object)
└── status: ExecutionStatus (Value Object)
```

#### Domain Events

| Event | 说明 |
|-------|------|
| CommandExecutedEvent | 命令执行事件 |
| CommandFailedEvent | 命令执行失败事件 |

### 2.3 Git 上下文 (Git Context)

#### Entities

| Entity | 标识 | 职责 |
|--------|------|------|
| Repository | RepoPath | Git 仓库 |
| Branch | BranchName | Git 分支 |
| Commit | CommitHash | Git 提交 |
| **CloneOperation** | **OperationId** | **Git仓库克隆操作** |

#### Value Objects

| Value Object | 职责 |
|--------------|------|
| GitStatus | Git 状态（工作区、暂存区状态） |
| GitLogEntry | 单条 Git 日志 |
| BranchInfo | 分支信息 |
| **CloneResult** | **克隆操作结果** |
| **CloneOptions** | **克隆选项（URL、目录、深度等）** |

#### Aggregates

```
Repository Aggregate (Aggregate Root)
├── Repository (Entity, Root)
└── branches: Branch[] (Entity 集合)

Branch Aggregate
├── Branch (Entity, Root)
└── info: BranchInfo (Value Object)

Commit Aggregate
├── Commit (Entity, Root)
└── log: GitLogEntry (Value Object)

CloneOperation Aggregate (Aggregate Root)
├── CloneOperation (Entity, Root)
├── options: CloneOptions (Value Object)
└── result: CloneResult (Value Object)
```

#### Domain Events

| Event | 说明 |
|-------|------|
| BranchSwitchedEvent | 分支切换事件 |
| CodePulledEvent | 代码拉取事件 |
| **RepositoryClonedEvent** | **仓库克隆成功事件** |
| **CloneFailedEvent** | **仓库克隆失败事件** |

#### Git克隆功能设计

**CloneOptions (Value Object)**:

| 字段 | 类型 | 说明 |
|------|------|------|
| url | GitRepoUrl | 远程仓库URL |
| targetDir | str | 目标目录（可选） |
| branch | str | 指定分支（可选） |
| depth | int | 浅克隆深度（可选） |
| recursive | bool | 是否递归克隆子模块 |

**CloneResult (Value Object)**:

| 字段 | 类型 | 说明 |
|------|------|------|
| success | bool | 是否成功 |
| message | str | 结果消息 |
| clonedPath | str | 克隆到的本地路径 |
| commitHash | str | 最新提交哈希（成功时） |

### 2.4 连接上下文 (Connection Context)

#### Entities

| Entity | 标识 | 职责 |
|--------|------|------|
| Connection | SessionId | 连接会话 |

#### Value Objects

| Value Object | 职责 |
|--------------|------|
| ConnectionConfig | 连接配置 |
| ConnectionStatus | 连接状态 |
| AuthCredential | 认证凭据 |

#### Aggregate

```
Connection Aggregate (Aggregate Root)
├── Connection (Entity, Root)
├── config: ConnectionConfig (Value Object)
└── credential: AuthCredential (Value Object)
```

---

## 3. 架构设计

### 3.1 架构模式选择

推荐使用 **Hexagonal Architecture（ hexagonal 架构/端口与适配器）**，原因如下：

1. **解耦性高**：核心领域逻辑与外部依赖完全隔离
2. **CLI 工具特性**：CLI 是典型的输入/输出驱动应用，hexagonal 架构适合处理多种 IO 方式
3. **可测试性**：领域逻辑可以完全脱离基础设施进行单元测试
4. **远程通信**：需要与远程沙盒系统通信，适配器模式便于替换通信方式
5. **Python 实现**：推荐使用 Click 或 Typer 框架构建 CLI，结合 Hexagonal Architecture 实现清晰的分层
6. **多沙盒支持**：不同沙盒类型需要不同的客户端实现，适配器模式便于扩展

> **技术栈**：Python 3.10+ | Click/Typer | asyncio | pydantic

### 3.2 分层结构

```
src/
├── domain/                          # 领域层（核心业务逻辑）
│   ├── configuration/               # 配置上下文
│   │   ├── entities/
│   │   │   └── config.py
│   │   ├── value_objects/
│   │   │   ├── config_item.py
│   │   │   ├── server_address.py
│   │   │   ├── timeout.py
│   │   │   ├── sandbox_type.py
│   │   │   ├── git_config.py       # 新增：Git配置
│   │   │   ├── git_repo_url.py     # 新增：Git仓库URL
│   │   │   ├── git_auth_type.py    # 新增：Git认证方式
│   │   │   ├── ssh_key.py          # 新增：SSH密钥
│   │   │   └── git_credential.py   # 新增：Git凭据
│   │   ├── aggregates/
│   │   │   └── config_aggregate.py
│   │   ├── events/
│   │   │   └── __init__.py
│   │   └── services/
│   │       ├── config_service.py
│   │       └── git_config_validator.py
│   │
│   ├── command/                     # 指令上下文
│   │   ├── entities/
│   │   │   ├── command.py
│   │   │   └── execution.py
│   │   ├── value_objects/
│   │   │   ├── command_input.py
│   │   │   ├── command_output.py
│   │   │   └── execution_status.py
│   │   ├── aggregates/
│   │   │   ├── command_aggregate.py
│   │   │   └── execution_aggregate.py
│   │   ├── events/
│   │   │   └── __init__.py
│   │   └── services/
│   │       └── command_service.py
│   │
│   ├── git/                         # Git 上下文
│   │   ├── entities/
│   │   │   ├── repository.py
│   │   │   ├── branch.py
│   │   │   ├── commit.py
│   │   │   └── clone_operation.py  # 新增：克隆操作
│   │   ├── value_objects/
│   │   │   ├── git_status.py
│   │   │   ├── git_log_entry.py
│   │   │   ├── branch_info.py
│   │   │   ├── clone_options.py    # 新增：克隆选项
│   │   │   └── clone_result.py     # 新增：克隆结果
│   │   ├── aggregates/
│   │   │   ├── repository_aggregate.py
│   │   │   └── clone_operation_aggregate.py  # 新增
│   │   ├── events/
│   │   │   ├── __init__.py
│   │   │   ├── repository_cloned_event.py    # 新增
│   │   │   └── clone_failed_event.py         # 新增
│   │   └── services/
│   │       ├── git_service.py
│   │       └── clone_service.py             # 新增：克隆服务
│   │
│   ├── connection/                  # 连接上下文
│   │   ├── entities/
│   │   │   └── connection.py
│   │   ├── value_objects/
│   │   │   ├── connection_config.py
│   │   │   ├── connection_status.py
│   │   │   └── auth_credential.py
│   │   ├── aggregates/
│   │   │   └── connection_aggregate.py
│   │   └── services/
│   │       └── connection_service.py
│   │
│   └── shared/                      # 共享内核
│       ├── value_objects/
│       │   ├── timestamp.py
│       │   └── result.py
│       └── events/
│           └── domain_event.py
│
├── application/                     # 应用层（用例）
│   ├── commands/                    # 命令（写操作）
│   │   ├── configuration/
│   │   │   ├── update_config_command.py
│   │   │   └── interactive_config_command.py
│   │   ├── command/
│   │   │   └── execute_command_command.py
│   │   └── git/
│   │       ├── switch_branch_command.py
│   │       ├── pull_code_command.py
│   │       └── clone_repository_command.py   # 新增：克隆仓库命令
│   │
│   ├── queries/                     # 查询（读操作）
│   │   ├── configuration/
│   │   │   └── get_config_query.py
│   │   └── git/
│   │       ├── get_git_status_query.py
│   │       ├── get_git_log_query.py
│   │       └── get_branches_query.py
│   │
│   └── services/                    # 应用服务
│       ├── configuration_app_service.py
│       ├── command_app_service.py
│       └── git_app_service.py
│
├── infrastructure/                  # 基础设施层
│   ├── persistence/                 # 持久化
│   │   └── config/
│   │       └── config_repository.py
│   │
│   ├── remote/                      # 远程通信
│   │   ├── adapter/
│   │   │   ├── factory.py           # 适配器工厂（根据沙盒类型选择）
│   │   │   ├── remote_adapter.py   # 抽象适配器接口
│   │   │   ├── aio_adapter.py      # AIO沙盒适配器
│   │   │   └── ssh_adapter.py      # SSH沙盒适配器（可选）
│   │   ├── protocol/
│   │   │   └── sandbox_protocol.py # 抽象协议接口
│   │   └── client/
│   │       ├── sandbox_client.py   # 抽象客户端接口
│   │       ├── aio_client.py       # AIO沙盒客户端
│   │       └── ssh_client.py       # SSH客户端
│   │
│   └── logging/                     # 日志
│       └── logger.py
│
├── interfaces/                      # 接口层
│   ├── cli/                         # CLI 接口
│   │   ├── commands/
│   │   │   ├── config_commands.py
│   │   │   ├── command_commands.py
│   │   │   └── git_commands.py     # 包含clone命令
│   │   ├── parser/
│   │   │   └── command_parser.py
│   │   └── presenter/
│   │       └── output_formatter.py
│   │
│   └── http/                        # HTTP 接口（可选）
│       └── rest/
│           └── rest_api.py
│
└── main/                            # 入口
    └── __main__.py
```

### 3.3 包结构说明

| 层级 | 职责 | 依赖 |
|------|------|------|
| domain | 纯业务逻辑，无外部依赖 | 无 |
| application | 用例编排，协调领域对象 | domain |
| infrastructure | 外部依赖实现（远程通信、持久化） | domain, application |
| interfaces | 用户交互接口 | application |

### 3.4 沙盒类型适配器设计

为了支持多种沙盒类型（如AIO沙盒、SSH沙盒等），基础设施层采用适配器模式：

```
┌─────────────────────────────────────────────────────────────┐
│                    Adapter Factory                          │
│              根据配置中的 sandbox_type 选择                  │
│                    对应的适配器                             │
└─────────────────────────────────────────────────────────────┘
                                │
            ┌───────────────────┼───────────────────┐
            ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   AIO Adapter   │ │   SSH Adapter   │ │  Other Adapter  │
│   (aio_client)  │ │  (ssh_client)   │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

**沙盒类型配置**：

| 沙盒类型 | 标识 | 说明 |
|----------|------|------|
| AIO | `aio` | AIO Sandbox，使用HTTP API通信 |
| SSH | `ssh` | 传统SSH连接方式 |
| Custom | `custom` | 自定义沙盒 |

**工作流程**：
1. 用户配置 `sandbox_type` 为 `aio`
2. 应用层根据配置调用适配器工厂
3. 工厂创建对应的 `AioAdapter` 实例
4. 指令执行时通过适配器与AIO沙盒通信

### 3.5 Git配置与克隆流程

**Git配置数据流**：

```
┌─────────────────────────────────────────────────────────────────┐
│                     Git配置流程                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  用户配置 ──▶ Config Context ──▶ GitConfig (Value Object)       │
│       │                                                         │
│       ├── git_repo_url: GitRepoUrl                              │
│       ├── git_auth_type: GitAuthType (SSH/HTTPS/None)           │
│       ├── ssh_key: SSHKey (可选)                                │
│       └── git_credential: GitCredential (可选)                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Git克隆流程**：

```
┌─────────────────────────────────────────────────────────────────┐
│                     Git克隆流程                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. 用户调用 git clone 命令                                      │
│     │                                                           │
│     ▼                                                            │
│  2. GitAppService 获取 GitConfig (从 Configuration Context)    │
│     │                                                           │
│     ▼                                                            │
│  3. CloneService 创建 CloneOptions                              │
│     │                                                           │
│     ▼                                                            │
│  4. 通过 Remote Adapter 执行 git clone 指令                     │
│     │                                                           │
│     ▼                                                            │
│  5. 返回 CloneResult                                            │
│     │                                                           │
│     ▼                                                            │
│  6. 触发 RepositoryClonedEvent 或 CloneFailedEvent             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. 领域模型总览

### 4.1 Entity-Value Object 分布

```
┌─────────────────────────────────────────────────────────────────┐
│                      Configuration Context                      │
├─────────────────────────────────────────────────────────────────┤
│  Entities: Config                                              │
│  Value Objects: ConfigItem, ServerAddress, Timeout,            │
│                SandboxType, GitConfig, GitRepoUrl,             │
│                GitAuthType, SSHKey, GitCredential              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        Command Context                          │
├─────────────────────────────────────────────────────────────────┤
│  Entities: Command, Execution                                   │
│  Value Objects: CommandInput, CommandOutput, ExecutionStatus  │
│  Domain Events: CommandExecuted, CommandFailed                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                          Git Context                             │
├─────────────────────────────────────────────────────────────────┤
│  Entities: Repository, Branch, Commit, CloneOperation           │
│  Value Objects: GitStatus, GitLogEntry, BranchInfo,            │
│                CloneOptions, CloneResult                       │
│  Domain Events: BranchSwitched, CodePulled,                   │
│                 RepositoryCloned, CloneFailed                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       Connection Context                        │
├─────────────────────────────────────────────────────────────────┤
│  Entities: Connection                                          │
│  Value Objects: ConnectionConfig, ConnectionStatus,           │
│                AuthCredential                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. 设计决策说明

### 5.1 Bounded Context 划分理由

- **分离核心域与支撑域**：指令系统、Git 系统是用户的核心操作，属于核心域；配置和连接是支撑功能
- **独立演化**：每个上下文可以独立开发和测试，减少耦合
- **远程通信集中**：连接上下文作为基础设施，被其他所有上下文依赖
- **功能扩展**：增加Git克隆功能，需要在Git上下文和配置上下文中同时扩展

### 5.2 Git配置设计原则

- **配置与操作分离**：Git配置作为独立的Value Objects，与Git操作业务逻辑分离
- **认证方式灵活**：支持SSH、HTTPS等多种认证方式，通过GitAuthType区分
- **可选配置**：SSH密钥和Git凭据为可选配置，根据认证方式决定是否需要
- **安全存储**：敏感信息（SSH密钥）需要安全存储，建议加密或引用文件路径

### 5.3 CloneOperation Aggregate设计

- **独立Aggregate**：克隆操作作为独立的Aggregate，便于跟踪操作状态
- **幂等性设计**：克隆结果包含成功/失败状态，支持重试
- **事件驱动**：通过Domain Event通知克隆结果，便于日志记录和后续处理

### 5.4 Aggregate 边界

- **最小化 Aggregate 原则**：每个 Aggregate 只包含保证一致性所必需的对象
- **Execution Aggregate**：每次执行是独立的事件

### 5.5 Value Object 使用

- **优先使用 Value Objects**：如 `CommandInput`、`CommandOutput`、`GitStatus` 等没有身份标识的概念都设计为 Value Objects
- **不可变性**：所有 Value Objects 设计为不可变，确保线程安全和简化并发处理

---

## 6. 现有 CLI 指令说明

### 6.1 配置相关指令

| 指令 | 命令 | 说明 |
|------|------|------|
| 获取配置 | `sandboxcli config get` | 获取当前配置信息，可选参数 `--include-sensitive` 包含敏感信息 |
| 更新配置 | `sandboxcli config set` | 更新服务器地址、端口、用户名、超时时间、AIO Sandbox HTTP API 地址等 |
| 交互式配置 | `sandboxcli config interactive` | 通过交互式界面配置 AIO Sandbox HTTP API 地址、用户名、超时时间 |
| 设置Git配置 | `sandboxcli config set-git` | 设置Git仓库URL、认证方式（none/https/ssh）、SSH密钥路径、用户名、邮箱等 |

**`config get` 命令输出说明：**

`config get` 命令返回的配置字段：

| 字段 | 类型 | 说明 | 备注 |
|------|------|------|------|
| id | string | 配置ID | 默认值 "default" |
| server_address | string | 服务器地址 | AIO模式为HTTP API地址，SSH模式为host:port |
| timeout | string | 超时时间 | 格式如 "30s" |
| username | string | 用户名 | 可为null |
| sandbox_type | string | 沙盒类型 | 默认 "aio" |
| git_config | object | Git配置 | 包含仓库URL、认证方式等 |
| items | array | 自定义配置项 | 用户通过 --key/--value 添加的额外配置 |

**git_config 字段详情：**

| 子字段 | 类型 | 说明 |
|--------|------|------|
| repo_url | string | Git仓库URL |
| auth_type | string | 认证方式 (none/https/ssh) |
| ssh_key | object | SSH密钥信息 |
| credential | object | Git凭据 (username、email) |
| default_branch | string | 默认分支名 |

**配置命令选项详情：**

`config get` 命令选项：
- `--config-id`: 配置ID（可选，指定获取特定配置项）
- `--include-sensitive`: 包含敏感信息（可选，默认false）

`config set` 命令选项：
- `--host`: 服务器地址 (SSH模式)
- `--port`: 服务器端口
- `--username`: 用户名
- `--timeout`: 超时时间(秒)
- `--key`: 自定义配置键
- `--value`: 自定义配置值
- `--base-url`: AIO Sandbox HTTP API 地址 (如 http://your-aio-server:8080)

`config set-git` 命令选项：
- `--url`: Git仓库URL
- `--auth-type`: 认证方式 (none/https/ssh)
- `--ssh-key-path`: SSH密钥文件路径
- `--username`: Git用户名
- `--email`: Git邮箱
- `--password`: Git密码(HTTPS认证时使用)
- `--default-branch`: 默认分支名

### 6.2 命令执行指令

| 指令 | 命令 | 说明 |
|------|------|------|
| 执行远程命令 | `sandboxcli command exec <command>` | 在远程沙盒中执行命令 |
| 快速执行命令 | `sandboxcli command run <cmd>` | 快速执行命令（简化版） |

**命令执行选项：**

`command exec` 命令选项：
- `command`: 要执行的命令（位置参数）
- `--args`: 命令参数（多个）
- `--cwd/--working-directory`: 工作目录
- `--timeout`: 超时时间(秒)
- `--env`: 环境变量 (KEY=VALUE格式)

### 6.3 Git 操作指令

| 指令 | 命令 | 说明 |
|------|------|------|
| 获取Git状态 | `sandboxcli git status` | 获取工作区、暂存区的Git状态 |
| 获取Git日志 | `sandboxcli git log` | 获取提交历史记录 |
| 获取分支列表 | `sandboxcli git branch` | 获取本地和远程分支列表 |
| 切换分支 | `sandboxcli git switch <branch_name>` | 切换到指定分支 |
| 拉取代码 | `sandboxcli git pull` | 从远程仓库拉取最新代码 |
| 克隆仓库 | `sandboxcli git clone <url>` | 克隆远程Git仓库到本地 |

**Git 操作选项：**

`git status` 选项：
- `--repo-path`: 仓库路径（默认 "."）

`git log` 选项：
- `--repo-path`: 仓库路径（默认 "."）
- `--max-count`: 最大日志数量（默认 10）
- `--branch`: 分支名称

`git branch` 选项：
- `--repo-path`: 仓库路径（默认 "."）
- `--include-remote/--no-remote`: 是否包含远程分支（默认 True）

`git switch` 选项：
- `branch_name`: 分支名称（位置参数）
- `--repo-path`: 仓库路径（默认 "."）
- `--create/--no-create`: 是否创建新分支（默认 False）

`git pull` 选项：
- `--repo-path`: 仓库路径（默认 "."）
- `--branch`: 分支名称（默认 "HEAD"）
- `--rebase/--no-rebase`: 是否使用rebase（默认 False）

`git clone` 选项：
- `url`: 远程仓库URL（位置参数）
- `-d/--target-dir`: 目标目录
- `-b/--branch`: 指定分支
- `--depth`: 浅克隆深度
- `--recursive/--no-recursive`: 是否递归克隆子模块（默认 False）
- `--use-config-git/--no-use-config-git`: 是否使用配置中的Git凭据（默认 True）

### 6.4 指令使用示例

```bash
# 配置管理示例
sandboxcli config get
sandboxcli config set --base-url http://your-aio-server:8080 --username admin --timeout 60
sandboxcli config interactive

# Git配置示例
sandboxcli config set-git --url https://github.com/user/repo.git --auth-type https --username youruser
sandboxcli config set-git --url git@github.com:user/repo.git --auth-type ssh --ssh-key-path ~/.ssh/id_rsa

# 命令执行示例
sandboxcli command exec "ls -la" --cwd /home/user
sandboxcli command exec "python script.py" --args arg1 arg2 --timeout 120

# Git操作示例
sandboxcli git status --repo-path /path/to/repo
sandboxcli git log --max-count 20 --branch main
sandboxcli git branch --no-remote
sandboxcli git switch develop --create
sandboxcli git pull --rebase
sandboxcli git clone https://github.com/user/repo.git -d /tmp/repo -b main --depth 1
```

---

## 7. 后续步骤

1. **实现代码**：切换到 Code 模式开始实现
2. **定义远程协议**：根据沙盒系统的接口定义通信协议适配器
3. **实现 CLI 命令**：在 interfaces 层实现具体的 CLI 命令，包含 git clone 命令
4. **添加单元测试**：为 domain 层的领域逻辑添加单元测试
5. **配置存储**：实现Git配置的持久化存储

---

## 7. 附录：Git配置字段参考

### 7.1 配置字段列表

| 配置项 | 类型 | 必填 | 说明 | 默认值 |
|--------|------|------|------|--------|
| sandbox_type | str | 是 | 沙盒类型 | "aio" |
| server_address | str | 是 | 服务器地址 | "" |
| server_port | int | 是 | 服务器端口 | 8080 |
| timeout | int | 否 | 超时时间（秒） | 30 |
| git_repo_url | str | 否 | 默认Git仓库URL | "" |
| git_auth_type | str | 否 | Git认证方式 | "none" |
| git_ssh_key_path | str | 否 | SSH密钥文件路径 | "" |
| git_username | str | 否 | Git用户名 | "" |
| git_email | str | 否 | Git邮箱 | "" |

### 7.2 认证方式说明

| 认证方式 | git_auth_type 值 | 需要的配置项 |
|----------|------------------|--------------|
| 无认证 | "none" | 无 |
| HTTPS用户名密码 | "https" | git_username, git_password |
| SSH密钥 | "ssh" | git_ssh_key_path |

# SandboxCLI DDD 设计文档

> **版本更新说明**：根据最新需求文档，移除了文件系统功能。

## 1. 战略设计

### 1.1 业务领域概述

SandboxCLI 是一个远程沙盒系统控制工具，用户通过 CLI 客户端连接到远程沙盒服务器进行操作。根据功能划分，系统包含以下主要业务领域：

- **配置管理**：CLI 工具的配置查看与修改
- **指令系统**：远程命令执行（在沙盒系统内执行指令）
- **Git 管理**：Git 版本控制操作（在沙盒系统内执行 git 指令）
- **连接管理**：与远程沙盒的连接维护

### 1.2 Bounded Contexts 划分

系统划分为 **4 个 Bounded Contexts**：

| 上下文 | 英文名 | 职责 | 核心域 |
|--------|--------|------|--------|
| 配置上下文 | Configuration Context | CLI 配置的查看、修改、交互式修改 | 支撑域 |
| 指令上下文 | Command Context | 远程指令执行 | 核心域 |
| Git 上下文 | Git Context | Git 状态、日志、分支、代码拉取 | 核心域 |
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
| Configuration, Command, Git | Separate Ways | 三个上下文之间相互独立，无直接依赖 |

### 1.4 Ubiquitous Language 词汇表

#### 配置上下文 (Configuration Context)

| 术语 | 英文 | 定义 |
|------|------|------|
| 配置项 | ConfigItem | CLI 的单个配置项，如服务器地址、端口、超时设置等 |
| 配置值 | ConfigValue | 配置项的具体值 |
| 配置快照 | ConfigSnapshot | 某一时刻的完整配置状态 |

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

#### Aggregate

```
Config Aggregate (Aggregate Root)
├── Config (Entity, Root)
└── configItems: ConfigItem[] (Value Objects 集合)
```

#### Domain Services

| Service | 职责 |
|---------|------|
| ConfigService | 配置的管理和验证 |

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

#### Value Objects

| Value Object | 职责 |
|--------------|------|
| GitStatus | Git 状态（工作区、暂存区状态） |
| GitLogEntry | 单条 Git 日志 |
| BranchInfo | 分支信息 |

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
```

#### Domain Events

| Event | 说明 |
|-------|------|
| BranchSwitchedEvent | 分支切换事件 |
| CodePulledEvent | 代码拉取事件 |

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
│   │   │   └── timeout.py
│   │   ├── aggregates/
│   │   │   └── config_aggregate.py
│   │   ├── events/
│   │   │   └── __init__.py
│   │   └── services/
│   │       └── config_service.py
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
│   │   │   └── commit.py
│   │   ├── value_objects/
│   │   │   ├── git_status.py
│   │   │   ├── git_log_entry.py
│   │   │   └── branch_info.py
│   │   ├── aggregates/
│   │   │   └── repository_aggregate.py
│   │   ├── events/
│   │   │   └── __init__.py
│   │   └── services/
│   │       └── git_service.py
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
│   │       └── pull_code_command.py
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
│   │   │   └── remote_adapter.py
│   │   ├── protocol/
│   │   │   └── sandbox_protocol.py
│   │   └── client/
│   │       └── sandbox_client.py
│   │
│   └── logging/                     # 日志
│       └── logger.py
│
├── interfaces/                      # 接口层
│   ├── cli/                         # CLI 接口
│   │   ├── commands/
│   │   │   ├── config_commands.py
│   │   │   ├── command_commands.py
│   │   │   └── git_commands.py
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

---

## 4. 领域模型总览

### 4.1 Entity-Value Object 分布

```
┌─────────────────────────────────────────────────────────────────┐
│                      Configuration Context                      │
├─────────────────────────────────────────────────────────────────┤
│  Entities: Config                                              │
│  Value Objects: ConfigItem, ServerAddress, Timeout            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        Command Context                          │
├─────────────────────────────────────────────────────────────────┤
│  Entities: Command, Execution                                   │
│  Value Objects: CommandInput, CommandOutput, ExecutionStatus   │
│  Domain Events: CommandExecuted, CommandFailed                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                          Git Context                             │
├─────────────────────────────────────────────────────────────────┤
│  Entities: Repository, Branch, Commit                          │
│  Value Objects: GitStatus, GitLogEntry, BranchInfo             │
│  Domain Events: BranchSwitched, CodePulled                     │
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
- **功能简化**：根据最新需求，移除了文件系统功能，简化了系统边界

### 5.2 Aggregate 边界

- **最小化 Aggregate 原则**：每个 Aggregate 只包含保证一致性所必需的对象
- **Execution Aggregate**：每次执行是独立的事件

### 5.3 Value Object 使用

- **优先使用 Value Objects**：如 `CommandInput`、`CommandOutput`、`GitStatus` 等没有身份标识的概念都设计为 Value Objects
- **不可变性**：所有 Value Objects 设计为不可变，确保线程安全和简化并发处理

---

## 6. 后续步骤

1. **实现代码**：切换到 Code 模式开始实现
2. **定义远程协议**：根据沙盒系统的接口定义通信协议适配器
3. **实现 CLI 命令**：在 interfaces 层实现具体的 CLI 命令
4. **添加单元测试**：为 domain 层的领域逻辑添加单元测试

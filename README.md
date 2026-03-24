# SandboxCLI

SandboxCLI - 远程沙盒系统控制工具

## 安装

### 从源码安装

```bash
# 克隆仓库
git clone <repository-url>
cd SandboxCLI

# 安装（可编辑模式）
pip install -e .

# 或安装为发布版本
pip install .
```

### 验证安装

```bash
sandboxcli --version
```

## 使用

### 查看帮助

```bash
sandboxcli --help
```

### 配置命令

```bash
# 查看当前配置
sandboxcli config get

# 交互式配置
sandboxcli config interactive

# 更新配置项
sandboxcli config update <key> <value>
```

### 命令执行

```bash
# 执行命令
sandboxcli command execute <command>
```

### Git 命令

```bash
# 拉取代码
sandboxcli git pull

# 切换分支
sandboxcli git switch <branch-name>

# 查看分支
sandboxcli git branches

# 查看 Git 状态
sandboxcli git status

# 查看 Git 日志
sandboxcli git log
```

## 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

## 许可证

MIT License

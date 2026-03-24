"""Git克隆服务"""
from typing import List, Tuple

from ...shared import Result
from ...configuration.value_objects import GitConfig
from ..entities import CloneOperation
from ..value_objects import CloneOptions, CloneResult


class CloneService:
    """Git克隆服务
    
    负责处理Git仓库克隆操作的核心领域逻辑。
    注意：实际的远程执行由应用层和基础设施层完成。
    """
    
    @staticmethod
    def create_clone_operation(
        url: str,
        target_dir: str = None,
        branch: str = None,
        depth: int = None,
        recursive: bool = False,
    ) -> CloneOperation:
        """创建克隆操作
        
        Args:
            url: 远程仓库URL
            target_dir: 目标目录
            branch: 指定分支
            depth: 浅克隆深度
            recursive: 是否递归克隆子模块
            
        Returns:
            CloneOperation: 克隆操作实体
        """
        options = CloneOptions(
            url=url,
            target_dir=target_dir,
            branch=branch,
            depth=depth,
            recursive=recursive,
        )
        return CloneOperation.create(options)
    
    @staticmethod
    def validate_clone_options(options: CloneOptions) -> Result[CloneOptions]:
        """验证克隆选项
        
        Args:
            options: 克隆选项
            
        Returns:
            Result: 验证结果
        """
        if not options.url or not options.url.strip():
            return Result.fail("仓库URL不能为空")
        
        # 验证URL格式
        url = options.url.strip()
        valid_prefixes = ["https://", "http://", "git@", "ssh://"]
        if not any(url.startswith(prefix) for prefix in valid_prefixes):
            return Result.fail(f"无效的仓库URL格式: {url}")
        
        # 验证深度
        if options.depth is not None and options.depth <= 0:
            return Result.fail("浅克隆深度必须大于0")
        
        return Result.ok(options)
    
    @staticmethod
    def validate_git_config(config: GitConfig) -> Result[GitConfig]:
        """验证Git配置
        
        Args:
            config: Git配置
            
        Returns:
            Result: 验证结果
        """
        # 检查仓库URL
        if config.repo_url.is_empty():
            return Result.fail("Git仓库URL未设置")
        
        # 检查认证配置
        if config.auth_type.is_ssh() and config.ssh_key.is_empty():
            return Result.fail("SSH认证方式需要配置SSH密钥")
        
        if config.auth_type.is_https() and config.credential.is_empty():
            return Result.fail("HTTPS认证方式需要配置用户名和密码")
        
        return Result.ok(config)
    
    @staticmethod
    def create_clone_options_from_config(
        config: GitConfig,
        override_url: str = None,
        target_dir: str = None,
        branch: str = None,
        depth: int = None,
    ) -> Result[CloneOptions]:
        """从Git配置创建克隆选项
        
        Args:
            config: Git配置
            override_url: 覆盖默认URL
            target_dir: 目标目录
            branch: 分支
            depth: 浅克隆深度
            
        Returns:
            Result: 克隆选项
        """
        # 验证配置
        validate_result = CloneService.validate_git_config(config)
        if not validate_result.is_success():
            return Result.fail(validate_result.error)
        
        # 确定URL
        url = override_url or config.repo_url.url
        if not url:
            return Result.fail("仓库URL不能为空")
        
        # 使用默认分支（如果未指定）
        if not branch:
            branch = config.default_branch
        
        options = CloneOptions(
            url=url,
            target_dir=target_dir,
            branch=branch,
            depth=depth,
            recursive=False,
        )
        
        return CloneService.validate_clone_options(options)
    
    @staticmethod
    def build_clone_command(
        options: CloneOptions,
        git_config: GitConfig,
    ) -> List[str]:
        """构建克隆命令
        
        Args:
            options: 克隆选项
            git_config: Git配置
            
        Returns:
            list[str]: git clone命令参数列表
        """
        cmd = ["git", "clone"]
        
        # 添加选项
        if options.depth:
            cmd.extend(["--depth", str(options.depth)])
        
        if options.branch:
            cmd.extend(["--branch", options.branch])
        
        if options.recursive:
            cmd.append("--recursive")
        
        # 添加URL
        cmd.append(options.url)
        
        # 添加目标目录
        if options.target_dir:
            cmd.append(options.target_dir)
        
        return cmd
    
    @staticmethod
    def parse_clone_result(
        output: str,
        error_output: str,
        exit_code: int,
        options: CloneOptions,
    ) -> CloneResult:
        """解析克隆结果
        
        Args:
            output: 标准输出
            error_output: 错误输出
            exit_code: 退出码
            options: 使用的克隆选项
            
        Returns:
            CloneResult: 克隆结果
        """
        if exit_code == 0:
            # 提取克隆路径
            cloned_path = options.target_dir or options.url.split("/")[-1].replace(".git", "")
            
            return CloneResult.success(
                message=f"成功克隆仓库: {options.url}",
                cloned_path=cloned_path,
                remote_url=options.url,
                branch=options.branch or "main",
            )
        else:
            return CloneResult.failed(
                message=f"克隆失败: {error_output or output}",
                error=error_output or output,
            )

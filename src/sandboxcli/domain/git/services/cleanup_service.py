"""Git清理服务"""
from typing import List, Tuple, Optional

from ...shared import Result
from ..entities import CleanupOperation
from ..value_objects import CleanupOptions, CleanupResult, CleanupType


class CleanupService:
    """Git清理服务
    
    负责处理Git仓库清理操作的核心领域逻辑。
    注意：实际的远程执行由应用层和基础设施层完成。
    """
    
    @staticmethod
    def create_cleanup_operation(
        cleanup_type: CleanupType = CleanupType.CLEAN_WORKSPACE,
        force: bool = False,
        repo_path: str = ".",
    ) -> CleanupOperation:
        """创建清理操作
        
        Args:
            cleanup_type: 清理类型
            force: 是否强制执行
            repo_path: 仓库路径
            
        Returns:
            CleanupOperation: 清理操作实体
        """
        options = CleanupOptions(
            cleanup_type=cleanup_type,
            force=force,
            repo_path=repo_path,
        )
        return CleanupOperation.create(options)
    
    @staticmethod
    def validate_cleanup_options(options: CleanupOptions) -> Result[CleanupOptions]:
        """验证清理选项
        
        Args:
            options: 清理选项
            
        Returns:
            Result: 验证结果
        """
        if not options.repo_path or not options.repo_path.strip():
            return Result.fail("仓库路径不能为空")
        
        # 验证清理类型
        try:
            CleanupType(options.cleanup_type)
        except ValueError:
            return Result.fail(f"无效的清理类型: {options.cleanup_type}")
        
        return Result.ok(options)
    
    @staticmethod
    def build_workspace_clean_command(
        options: CleanupOptions,
    ) -> List[str]:
        """构建工作区清理命令
        
        Args:
            options: 清理选项
            
        Returns:
            list[str]: git clean命令参数列表
        """
        cmd = ["git", "-C", options.repo_path, "clean"]
        
        # -f: 强制删除文件
        # -d: 同时删除未跟踪的目录
        # -x: 删除被忽略的文件（可选）
        # -X: 只删除被忽略的文件（可选）
        
        if options.force:
            cmd.append("-f")
        
        cmd.append("-d")
        
        return cmd
    
    @staticmethod
    def build_branch_list_command(
        options: CleanupOptions,
    ) -> List[str]:
        """构建获取已合并分支列表命令
        
        Args:
            options: 清理选项
            
        Returns:
            list[str]: git branch命令参数列表
        """
        # 获取已合并到当前分支的本地分支
        return ["git", "-C", options.repo_path, "branch", "--merged"]
    
    @staticmethod
    def build_branch_delete_commands(
        options: CleanupOptions,
        branches: List[str],
    ) -> List[List[str]]:
        """构建删除分支命令列表
        
        Args:
            options: 清理选项
            branches: 要删除的分支列表
            
        Returns:
            list[list[str]]: git branch -d命令列表
        """
        # 保护分支列表
        protected_branches = ["main", "master", "develop", "develop", "main", "HEAD"]
        current_branch = None  # 需要通过 git branch 获取
        
        commands = []
        for branch in branches:
            branch = branch.strip()
            if not branch:
                continue
            # 跳过保护分支
            if branch.lower() in [b.lower() for b in protected_branches]:
                continue
            # 跳过当前分支标记
            if branch.startswith("*"):
                branch = branch[1:].strip()
                current_branch = branch
                continue
            
            # 构建删除命令
            commands.append(["git", "-C", options.repo_path, "branch", "-d", branch])
        
        return commands
    
    @staticmethod
    def build_tag_list_command(
        options: CleanupOptions,
    ) -> List[str]:
        """构建获取标签列表命令
        
        Args:
            options: 清理选项
            
        Returns:
            list[str]: git tag命令参数列表
        """
        return ["git", "-C", options.repo_path, "tag", "-l"]
    
    @staticmethod
    def build_tag_delete_commands(
        options: CleanupOptions,
        tags: List[str],
    ) -> List[List[str]]:
        """构建删除标签命令列表
        
        Args:
            options: 清理选项
            tags: 要删除的标签列表
            
        Returns:
            list[list[str]]: git tag -d命令列表
        """
        commands = []
        for tag in tags:
            tag = tag.strip()
            if not tag:
                continue
            commands.append(["git", "-C", options.repo_path, "tag", "-d", tag])
        
        return commands
    
    @staticmethod
    def parse_clean_result(
        output: str,
        error_output: str,
        exit_code: int,
    ) -> Tuple[bool, List[str]]:
        """解析清理输出
        
        Args:
            output: 标准输出
            error_output: 错误输出
            exit_code: 退出码
            
        Returns:
            Tuple[bool, List[str]]: (是否成功, 已删除的文件/目录列表)
        """
        if exit_code == 0:
            # 解析输出，提取已删除的文件
            files = []
            for line in output.split("\n"):
                line = line.strip()
                if line:
                    files.append(line)
            return True, files
        else:
            return False, []
    
    @staticmethod
    def create_success_result(
        cleaned_files: List[str] = None,
        deleted_branches: List[str] = None,
        deleted_tags: List[str] = None,
    ) -> CleanupResult:
        """创建成功结果
        
        Args:
            cleaned_files: 已清理的文件列表
            deleted_branches: 已删除的分支列表
            deleted_tags: 已删除的标签列表
            
        Returns:
            CleanupResult: 清理结果
        """
        cleaned = cleaned_files or []
        branches = deleted_branches or []
        tags = deleted_tags or []
        
        total = len(cleaned) + len(branches) + len(tags)
        
        message = f"清理完成，共删除 {total} 个项目"
        if cleaned:
            message += f"（{len(cleaned)} 个文件/目录）"
        if branches:
            message += f"，{len(branches)} 个分支"
        if tags:
            message += f"，{len(tags)} 个标签"
        
        return CleanupResult.success(
            message=message,
            cleaned_files=cleaned,
            deleted_branches=branches,
            deleted_tags=tags,
        )
    
    @staticmethod
    def create_failed_result(error: str) -> CleanupResult:
        """创建失败结果
        
        Args:
            error: 错误信息
            
        Returns:
            CleanupResult: 清理结果
        """
        return CleanupResult.failed(
            message=f"清理失败: {error}",
            error=error,
        )
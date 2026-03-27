"""输出格式化器"""
import json
from typing import Any, Dict, List


class OutputFormatter:
    """输出格式化器"""

    @staticmethod
    def format_json(data: Any, indent: int = 2) -> str:
        """格式化为JSON"""
        return json.dumps(data, indent=indent, ensure_ascii=False)

    @staticmethod
    def format_table(headers: List[str], rows: List[List[str]]) -> str:
        """格式化为表格"""
        if not rows:
            return ""
        
        # 计算每列的最大宽度
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # 构建表格
        lines = []
        
        # 表头
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        lines.append(header_line)
        lines.append("-" * len(header_line))
        
        # 数据行
        for row in rows:
            row_line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
            lines.append(row_line)
        
        return "\n".join(lines)

    @staticmethod
    def format_key_value(data: Dict, indent: int = 0) -> str:
        """格式化为键值对"""
        lines = []
        prefix = " " * indent
        
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(OutputFormatter.format_key_value(value, indent + 2))
            elif isinstance(value, list):
                lines.append(f"{prefix}{key}:")
                for item in value:
                    lines.append(f"{prefix}  - {item}")
            else:
                lines.append(f"{prefix}{key}: {value}")
        
        return "\n".join(lines)

    @staticmethod
    def format_error(error: str) -> str:
        """格式化错误信息"""
        return f"\033[91mError: {error}\033[0m"

    @staticmethod
    def format_success(message: str) -> str:
        """格式化成功信息"""
        return f"\033[92m{message}\033[0m"

    @staticmethod
    def format_warning(message: str) -> str:
        """格式化警告信息"""
        return f"\033[93mWarning: {message}\033[0m"

    @staticmethod
    def format_command_output(output: Dict, verbose: bool = False) -> str:
        """格式化命令执行输出

        Args:
            output: 输出字典
            verbose: 是否显示详细信息（默认 False，只显示输出内容）
        """
        if not output:
            return "No output"

        # 简洁模式：只显示输出内容
        if not verbose:
            output_data = output.get("output")
            if isinstance(output_data, dict):
                stdout = output_data.get("stdout", "")
                stderr = output_data.get("stderr", "")
                exit_code = output_data.get("exit_code", 0)

                # 根据设计文档：错误输出优先显示
                if stderr:
                    # 有 stderr 则显示 stderr
                    return stderr
                elif exit_code != 0:
                    # 执行失败但没有 stderr 时，显示默认错误消息
                    return f"Command failed with exit code: {exit_code}"
                else:
                    # 执行成功，显示 stdout（可能为空）
                    return stdout
            elif output_data:
                return str(output_data)
            return ""

        # 详细模式：显示完整信息
        lines = []
        lines.append("=" * 40)
        lines.append("Command Execution Result")
        lines.append("=" * 40)

        # 基本信息
        if "execution_id" in output:
            lines.append(f"Execution ID: {output['execution_id']}")

        if "command" in output:
            lines.append(f"Command: {output['command']}")

        # 执行状态
        if "status" in output:
            status = output["status"]
            lines.append(f"Status: {status}")

            # 如果是失败状态，添加颜色标记
            if status in ("FAILED", "TIMEOUT", "TIMEOUT_WITH_CONNECTION_FAIL", "TIMEOUT_WITH_CONNECTION_OK"):
                lines.append("")

        # 输出内容 - 支持字典和字符串两种格式
        if "output" in output:
            output_data = output["output"]
            if isinstance(output_data, dict):
                # 字典格式 (从 CommandOutput.to_dict() 来的)
                stdout = output_data.get("stdout", "")
                stderr = output_data.get("stderr", "")
                exit_code = output_data.get("exit_code", 0)

                # 始终显示输出内容，即使是空字符串也要显示
                # 只有当 stdout 和 stderr 都为空时才显示 "No output"
                if stdout or stderr:
                    if stdout:
                        lines.append(f"\nOutput:\n{stdout}")
                    if stderr:
                        lines.append(f"\nError:\n{stderr}")
                else:
                    lines.append("\nOutput: (empty)")

                lines.append(f"Exit Code: {exit_code}")

                # 如果执行失败但没有错误输出，显示默认消息
                if exit_code != 0 and not stderr:
                    lines.append(f"\nNote: Command exited with code {exit_code}")
            elif output_data:
                # 字符串格式
                lines.append(f"\nOutput:\n{output_data}")
            else:
                # output 存在但是空（如空字典或 None）
                lines.append("\nOutput: (empty)")
                # 获取 exit_code（如果存在）
                if isinstance(output.get("output"), dict):
                    exit_code = output.get("output").get("exit_code", 0)
                    if exit_code != 0:
                        lines.append(f"Exit Code: {exit_code}")

        # 兼容旧格式
        if "error" in output and output["error"]:
            lines.append(f"\nError: {output['error']}")

        return "\n".join(lines)


__all__ = ["OutputFormatter"]

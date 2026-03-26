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
    def format_command_output(output: Dict) -> str:
        """格式化命令执行输出"""
        if not output:
            return "No output"

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
            lines.append(f"Status: {output['status']}")

        # 输出内容 - 支持字典和字符串两种格式
        if "output" in output:
            output_data = output["output"]
            if isinstance(output_data, dict):
                # 字典格式 (从 CommandOutput.to_dict() 来的)
                if output_data.get("stdout"):
                    lines.append(f"\nOutput:\n{output_data['stdout']}")
                if output_data.get("stderr"):
                    lines.append(f"\nError:\n{output_data['stderr']}")
                if "exit_code" in output_data:
                    lines.append(f"Exit Code: {output_data['exit_code']}")
            else:
                # 字符串格式
                lines.append(f"\nOutput:\n{output_data}")

        # 兼容旧格式
        if "error" in output and output["error"]:
            lines.append(f"\nError: {output['error']}")

        return "\n".join(lines)


__all__ = ["OutputFormatter"]

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


__all__ = ["OutputFormatter"]

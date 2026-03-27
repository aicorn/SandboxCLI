"""AIO Sandbox 协议实现

定义与 AIO Sandbox HTTP API 通信的协议。
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SandboxResponse:
    """沙盒响应"""
    success: bool
    data: Any
    error: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "SandboxResponse":
        """从字典创建响应对象"""
        return cls(
            success=data.get("success", True),
            data=data.get("data"),
            error=data.get("error"),
        )


@dataclass
class ShellExecRequest:
    """Shell 执行请求"""
    command: str
    timeout: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {"command": self.command}
        if self.timeout:
            result["timeout"] = self.timeout
        return result


@dataclass
class ShellExecResponse:
    """Shell 执行响应"""
    output: str = ""
    stderr: str = ""
    exit_code: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> "ShellExecResponse":
        """从字典创建响应对象"""
        # 确保 output 不为 None，返回空字符串
        output = data.get("output")
        if output is None:
            output = ""
        # 确保 stderr 不为 None，返回空字符串
        stderr = data.get("stderr")
        if stderr is None:
            stderr = ""
        return cls(
            output=output,
            stderr=stderr,
            exit_code=data.get("exit_code", 0),
        )


@dataclass
class FileReadRequest:
    """文件读取请求"""
    file: str

    def to_dict(self) -> Dict[str, Any]:
        return {"file": self.file}


@dataclass
class FileReadResponse:
    """文件读取响应"""
    content: str

    @classmethod
    def from_dict(cls, data: dict) -> "FileReadResponse":
        return cls(
            content=data.get("content", ""),
        )


@dataclass
class FileWriteRequest:
    """文件写入请求"""
    file: str
    content: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": self.file,
            "content": self.content,
        }


@dataclass
class BrowserScreenshotResponse:
    """浏览器截图响应"""
    screenshot: str  # base64 encoded

    @classmethod
    def from_dict(cls, data: dict) -> "BrowserScreenshotResponse":
        return cls(
            screenshot=data.get("screenshot", ""),
        )


@dataclass
class JupyterExecuteRequest:
    """Jupyter 执行请求"""
    code: str

    def to_dict(self) -> Dict[str, Any]:
        return {"code": self.code}


@dataclass
class JupyterExecuteResponse:
    """Jupyter 执行响应"""
    outputs: list

    @classmethod
    def from_dict(cls, data: dict) -> "JupyterExecuteResponse":
        return cls(
            outputs=data.get("outputs", []),
        )


class SandboxProtocol:
    """AIO Sandbox 协议"""

    # API 端点
    ENDPOINT_SANDBOX = "/v1/sandbox"
    ENDPOINT_SHELL_EXEC = "/v1/shell/exec"
    ENDPOINT_FILE_READ = "/v1/file/read"
    ENDPOINT_FILE_WRITE = "/v1/file/write"
    ENDPOINT_BROWSER_SCREENSHOT = "/v1/browser/screenshot"
    ENDPOINT_JUPYTER_EXECUTE = "/v1/jupyter/execute"

    @staticmethod
    def build_shell_exec_request(command: str, timeout: int = None) -> ShellExecRequest:
        """构建 Shell 执行请求"""
        return ShellExecRequest(command=command, timeout=timeout)

    @staticmethod
    def build_file_read_request(file_path: str) -> FileReadRequest:
        """构建文件读取请求"""
        return FileReadRequest(file=file_path)

    @staticmethod
    def build_file_write_request(file_path: str, content: str) -> FileWriteRequest:
        """构建文件写入请求"""
        return FileWriteRequest(file=file_path, content=content)

    @staticmethod
    def build_jupyter_execute_request(code: str) -> JupyterExecuteRequest:
        """构建 Jupyter 执行请求"""
        return JupyterExecuteRequest(code=code)

    @staticmethod
    def parse_shell_response(data: dict) -> ShellExecResponse:
        """解析 Shell 执行响应

        Args:
            data: API 响应数据

        Returns:
            ShellExecResponse 对象

        注意：响应格式为 {'success': True, 'data': {'output': ..., 'stderr': ..., 'exit_code': ...}}
        """
        # 获取 data 字段中的内容
        data_obj = data.get("data", data)  # 兼容两种格式：有 data 包装 或 直接是数据

        # 确保 output 不为 None，返回空字符串
        output = data_obj.get("output")
        if output is None:
            output = ""

        # 确保 stderr 不为 None，返回空字符串
        stderr = data_obj.get("stderr")
        if stderr is None:
            stderr = ""

        return ShellExecResponse(
            output=output,
            stderr=stderr,
            exit_code=data_obj.get("exit_code", 0),
        )

    @staticmethod
    def parse_file_read_response(data: dict) -> FileReadResponse:
        """解析文件读取响应"""
        return FileReadResponse.from_dict(data)

    @staticmethod
    def parse_jupyter_response(data: dict) -> JupyterExecuteResponse:
        """解析 Jupyter 执行响应"""
        return JupyterExecuteResponse.from_dict(data)

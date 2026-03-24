"""Setup configuration for SandboxCLI"""
from setuptools import setup, find_packages

setup(
    name="sandboxcli",
    version="0.0.1",
    description="SandboxCLI - 远程沙盒系统控制工具",
    author="SandboxCLI Team",
    packages=find_packages("src", include=["sandboxcli", "sandboxcli.*"]),
    package_dir={
        "": "src",
    },
    install_requires=[
        "click>=8.0.0",
        "pydantic>=2.0.0",
        "paramiko>=3.0.0",
        "httpx>=0.24.0",
        "pyyaml>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "sandboxcli=sandboxcli.main.__main__:cli",
        ],
    },
    python_requires=">=3.8",
)

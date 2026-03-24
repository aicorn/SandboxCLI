"""认证凭据值对象"""
from typing import Optional

from pydantic import BaseModel, field_validator


class AuthCredential(BaseModel):
    """认证凭据值对象"""
    auth_type: str = "password"  # password, key, token
    username: Optional[str] = None
    password: Optional[str] = None
    private_key: Optional[str] = None
    token: Optional[str] = None

    model_config = {"frozen": True}

    @field_validator("auth_type")
    @classmethod
    def _validate_auth_type(cls, v: str) -> str:
        valid_types = ["password", "key", "token"]
        if v not in valid_types:
            raise ValueError(f"Auth type must be one of: {valid_types}")
        return v

    def is_password_auth(self) -> bool:
        """判断是否使用密码认证"""
        return self.auth_type == "password"

    def is_key_auth(self) -> bool:
        """判断是否使用密钥认证"""
        return self.auth_type == "key"

    def is_token_auth(self) -> bool:
        """判断是否使用令牌认证"""
        return self.auth_type == "token"

    def has_credential(self) -> bool:
        """判断是否有所需凭据"""
        if self.is_password_auth():
            return self.password is not None
        elif self.is_key_auth():
            return self.private_key is not None
        elif self.is_token_auth():
            return self.token is not None
        return False

    def to_dict(self) -> dict:
        """转换为字典（隐藏敏感信息）"""
        result = {"auth_type": self.auth_type, "username": self.username}
        if self.password:
            result["password"] = "***"
        if self.private_key:
            result["private_key"] = "***"
        if self.token:
            result["token"] = "***"
        return result

    def __repr__(self) -> str:
        return f"AuthCredential(auth_type='{self.auth_type}', username='{self.username}')"

# server/config.py  —— Pydantic v2 + pydantic-settings 写法
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    BASE_URL: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    )
    DASHSCOPE_API_KEY: Optional[str] = Field(default=None)  # 不要再硬编码密钥～
    AI_MODEL: str = "qwen-plus"
    AI_TEMPERATURE: float = 0.3  # 降低温度提高速度和稳定性
    AI_MAX_TOKENS: int = 500  # 减少token数量加快响应
    AI_TOP_P: float = 0.8  # 稍微降低多样性提高速度
    AI_TIMEOUT: float = 30.0

    # v2 的配置写法（替代 v1 的 class Config）
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

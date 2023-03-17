from typing import Optional

from pydantic import BaseSettings, HttpUrl, SecretStr, validator


class Settings(BaseSettings):
    token: SecretStr
    secret: SecretStr

    webhook_host: Optional[HttpUrl]
    webhook_prefix: Optional[str] = "/telegram-webhook"
    host: str = "127.0.0.1"
    port: int = 8000

    @validator("webhook_prefix")
    def validate_webhook_prefix(cls, value: str):
        if value and not value.startswith("/"):
            raise ValueError("path should be started with `/` or be empty")
        return value

    class Config:
        env_file = ".env"


settings = Settings()

from pydantic import BaseSettings


class Settings(BaseSettings):
    TOKEN: str

    class Config:
        env_file = ".env"


settings = Settings()

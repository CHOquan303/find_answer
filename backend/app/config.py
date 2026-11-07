"""应用配置。"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 19
    DATABASE_URL: str = "sqlite:///./findanswer.db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

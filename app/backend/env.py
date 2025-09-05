import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env" if os.path.exists(".env") else None,
        frozen=True,
        extra="ignore",
    )
    USER: str
    PASSWORD: SecretStr
    HOST: str
    PORT: int
    NAME: str
    # Connection pool settings
    POOL_MIN_CONNECTIONS: int = 1
    POOL_MAX_CONNECTIONS: int = 10
    POOL_TIMEOUT: int = 30  # seconds
    POOL_RECONNECT: bool = True  # Auto-reconnect on connection loss


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env" if os.path.exists(".env") else None,
        frozen=True,
        extra="ignore",
    )
    HOST: str = "http://localhost"
    PORT: int = 8000


DB_CONFIG = DatabaseConfig()
APP_CONFIG = AppConfig()

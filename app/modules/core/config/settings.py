from modules.core.config.env import (
    POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
)
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_STR: str = '/api'
    DB_URL: str = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    DB_URL_MIGRATION: str = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}'
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )

settings: Settings = Settings()

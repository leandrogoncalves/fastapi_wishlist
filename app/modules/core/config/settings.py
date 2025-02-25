from modules.core.config.env import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_STR: str = '/api'
    DB_URL: str = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

    class Config:
        case_sensitive = True

settings: Settings = Settings()
from sqlalchemy.ext.declarative import declarative_base
from modules.core.config.env import (
    POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
)
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_STR: str = '/api'
    DB_URL: str = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    # DBBaseModel = declarative_base()
    JWT_SECRET: str = 's_sLeGE4R6CKon-7T-QqPPeL64s1czS5DgDQUtdYPpc'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        case_sensitive=True
    )


settings: Settings = Settings()

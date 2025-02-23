import os
from dotenv import load_dotenv
from pythondi import Provider
from pythondi import configure

from pydantic_settings import BaseSettings

from modules.customer.domain.repository.database.customer_repository_abstract import CustomerRepositoryAbstract
from modules.customer.infrastructure.repository.database.customer_repository import CustomerRepository

load_dotenv()

APP_NAME = os.environ.get("APP_NAME", "FastApi_whishlist")
APP_TITLE = os.environ.get("APP_TITLE", "Whishlist API v1.0")
APP_DESCRIPTION = os.environ.get("APP_DESCRIPTION", "Projeto para teste de habilidades de programação")

APP_HOST = os.environ.get("APP_HOST", default="0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", default=8000))
APP_LOG_LEVEL = os.environ.get("APP_LOG_LEVEL", default="debug")
APP_RELOAD = os.environ.get("APP_RELOAD", default=True)

SWAGGER_URL = os.environ.get("SWAGGER_URL")

CORS_ALLOW_ORIGINS = os.environ.get("CORS_ALLOW_ORIGINS", default="*")
CORS_ALLOW_CREDENTIALS = os.environ.get("CORS_ALLOW_CREDENTIALS", default=True)
CORS_ALLOW_METHODS = os.environ.get("CORS_ALLOW_METHODS", default="*")
CORS_ALLOW_HEADERS = os.environ.get("CORS_ALLOW_HEADERS", default="*")

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", default=5432))

provider = Provider()
provider.bind(CustomerRepositoryAbstract, CustomerRepository)

configure(provider=provider)

class Settings(BaseSettings):
    API_STR: str = '/api'
    DB_URL: str = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

    class Config:
        case_sensitive = True

settings: Settings = Settings()

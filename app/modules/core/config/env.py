import os
from pathlib import Path
from dotenv import load_dotenv

#env_path = Path('../../../..') / '.env'
# load_dotenv(dotenv_path=env_path)
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "FastApi_whishlist")
APP_TITLE = os.getenv("APP_TITLE", "Whishlist API v1.0")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Projeto para teste de habilidades de programação")

APP_HOST = os.getenv("APP_HOST", default="0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", default=8000))
APP_LOG_LEVEL = os.getenv("APP_LOG_LEVEL", default="debug")
APP_RELOAD = os.getenv("APP_RELOAD", default=True)

SWAGGER_URL = os.getenv("SWAGGER_URL")

CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", default="*")
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", default=True)
CORS_ALLOW_METHODS = os.getenv("CORS_ALLOW_METHODS", default="*")
CORS_ALLOW_HEADERS = os.getenv("CORS_ALLOW_HEADERS", default="*")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", default=5432))

PAGE_SIZE = os.getenv("PAGE_SIZE", default=10)
DEFAULT_TINE_ZONE = os.getenv("DEFAULT_TINE_ZONE", default="America/Sao_Paulo")


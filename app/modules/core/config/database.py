from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from modules.core.config.settings import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL, echo=True, future=True)

session: AsyncSession = sessionmaker(
    autocommit = False,
    autoflush = False,
    expire_on_commit = False,
    class_ = AsyncSession,
    bind = engine
)

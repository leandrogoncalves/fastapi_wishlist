from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from modules.core.config.database import session


async def get_session() -> Generator:
    Session: AsyncSession = session()
    try:
        yield Session
    finally:
        await Session.close()
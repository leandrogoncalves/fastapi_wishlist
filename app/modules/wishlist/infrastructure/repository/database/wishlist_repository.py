import uuid
from http import HTTPStatus
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlmodel import select
from sqlalchemy import func
from fastapi import HTTPException
from modules.core.config.database import get_session
from modules.core.config.env import DEFAULT_TINE_ZONE
from modules.wishlist.domain.repository.database.wishlist_repository_abstract import WishlistRepositoryAbstract
from modules.wishlist.infrastructure.database.models.wishlist_model import WishlistModel



class WishlistRepository(WishlistRepositoryAbstract):

    async def create(self, wishlist_name: str) -> WishlistModel:
        new_wishlist = WishlistModel(
            id=str(uuid.uuid4()),
            name=wishlist_name,
            created_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE)),
            updated_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE))
        )
        async with get_session() as session:
            session.add(new_wishlist)
            await session.commit()
            return new_wishlist

    async def get_by_id(self, wishlist_id: str) -> WishlistModel:
        async with get_session() as session:
            query = select(WishlistModel).where(WishlistModel.id == wishlist_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

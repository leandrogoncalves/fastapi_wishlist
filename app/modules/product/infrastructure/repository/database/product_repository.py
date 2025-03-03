from typing import List
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlmodel import select
from sqlalchemy import func
from modules.core.config.env import DEFAULT_TINE_ZONE
from modules.shared.domain.repository.database.product_repository_abstract import ProductRepositoryAbstract
from modules.product.infrastructure.database.models.product_model import ProductModel
from modules.product.domain.entity.product import Product
from modules.core.config.database import get_session


class ProductRepository(ProductRepositoryAbstract):

    async def get_all_products(self, offset: int, limit: int) -> List[ProductModel]:
        async with get_session() as session:
            query = select(ProductModel).offset(offset).where(ProductModel.deleted_at.is_(None)).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()

    async def count(self) -> int:
        async with get_session() as session:
            query = select(func.count()).select_from(ProductModel).where(ProductModel.deleted_at.is_(None))
            result = await session.execute(query)
            return result.scalar_one()

    async def get_by_id(self, product_id: str) -> ProductModel:
        async with get_session() as session:
            query = select(ProductModel).where(
                ProductModel.id == product_id,
                ProductModel.deleted_at.is_(None)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> ProductModel:
        async with get_session() as session:
            query = select(ProductModel).where(
                ProductModel.email == email,
                ProductModel.deleted_at.is_(None)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def create(self, product: Product) -> ProductModel:
        async with get_session() as session:
            session.add(product)
            await session.commit()
            return product

    async def update(self, product: ProductModel) -> ProductModel:
        async with get_session() as session:
            product.updated_at = datetime.now(ZoneInfo(DEFAULT_TINE_ZONE))
            session.add(product)
            await session.commit()
            return product

    async def delete(self, product: ProductModel) -> None:
        async with get_session() as session:
            product.deleted_at = datetime.now(ZoneInfo(DEFAULT_TINE_ZONE))
            session.add(product)
            # await session.delete(product)
            await session.commit()

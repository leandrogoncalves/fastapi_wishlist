import uuid
from typing import List
from http import HTTPStatus
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlmodel import select
from sqlalchemy import func
from fastapi import HTTPException
from modules.core.config.env import DEFAULT_TINE_ZONE
from modules.product.domain.repository.database.product_repository_abstract import ProductRepositoryAbstract
from modules.product.infrastructure.database.models.product_model import ProductModel
from modules.product.domain.entity.product import Product
from modules.core.config.database import get_session


class ProductRepository(ProductRepositoryAbstract):

    async def get_all_products(self, offset: int, limit: int) -> List[ProductModel]:
        async with get_session() as session:
            query = select(ProductModel).offset(offset).limit(limit)
            result = await session.execute(query)
            products = result.scalars().all()
            return products

    async def count(self) -> int:
        async with get_session() as session:
            query = select(func.count()).select_from(ProductModel)
            result = await session.execute(query)
            total = result.scalar_one()
            return total

    async def get_by_id(self, product_id: str) -> ProductModel:
        async with get_session() as session:
            query = select(ProductModel).filter(ProductModel.id == product_id)
            result = await session.execute(query)
            product: ProductModel = result.scalar_one_or_none()
            return product

    async def get_by_email(self, email: str) -> ProductModel:
        async with get_session() as session:
            query = select(ProductModel).filter(ProductModel.email == email)
            result = await session.execute(query)
            product: ProductModel = result.scalar_one_or_none()
            return product

    async def create(self, product: Product) -> ProductModel:
        new_product = ProductModel(
            id=str(uuid.uuid4()),
            title=product.title,
            brand=product.brand,
            price=product.price,
            image=product.image,
            review_score=product.reviewScore,
            created_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE)),
            updated_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE))
        )
        async with get_session() as session:
            session.add(new_product)
            await session.commit()
            return new_product

    async def update(self, product_id: str, product: Product) -> ProductModel:
        print(product)
        product_founded = await self.get_by_id(product_id)
        if product_founded is None:
            raise HTTPException(
                detail="Product Not Found",
                status_code=HTTPStatus.NOT_FOUND,
            )
        async with get_session() as session:
            if product.title:
                product_founded.title = product.title
            if product.brand:
                product_founded.brand = product.brand
            if product.price:
                product_founded.price = product.price
            if product.image:
                product_founded.image = product.image
            if product.reviewScore:
                product_founded.review_score = product.reviewScore
            product_founded.updated_at = datetime.now(ZoneInfo(DEFAULT_TINE_ZONE))
            session.add(product_founded)
            await session.commit()
            return product_founded

    async def delete(self, product_id: str) -> None:
        product_founded = await self.get_by_id(product_id)
        if product_founded is None:
            raise HTTPException(
                detail="Product Not Found",
                status_code=HTTPStatus.NOT_FOUND,
            )
        async with get_session() as session:
            await session.delete(product_founded)
            await session.commit()

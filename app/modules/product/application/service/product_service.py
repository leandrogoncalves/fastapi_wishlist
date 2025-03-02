from http import HTTPStatus
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from pythondi import inject
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from modules.core.config.env import PAGE_SIZE
from modules.core.config.env import DEFAULT_TINE_ZONE
from modules.product.domain.repository.database.product_repository_abstract import ProductRepositoryAbstract
from modules.product.infrastructure.database.models.product_model import ProductModel
from modules.product.domain.entity.product import Product
from modules.product.domain.entity.product_paginated import ProductPaginated

class ProductService:

    def __init__(self):
        self.repository = self._get_product_repository()

    @inject()
    def _get_product_repository(self, repository: ProductRepositoryAbstract):
        return repository

    async def get_all_paginated(self, page: int) -> ProductPaginated:
        total = await self.count_all()
        total_pages = round(total / PAGE_SIZE)
        offset = (page - 1) * PAGE_SIZE
        data = await self.repository.get_all_products(offset, PAGE_SIZE)
        product_data = [self._get_product(product) for product in data]
        return ProductPaginated(
            page=page,
            total_pages=total_pages or 1,
            total_results=total,
            results_in_page=len(product_data),
            data=jsonable_encoder(product_data)
        )

    async def count_all(self) -> int:
        return await self.repository.count()

    async def get_by_id(self, product_id: str) -> Optional[Product]:
        product_model: ProductModel = await self.repository.get_by_id(product_id)
        if product_model is None:
            raise HTTPException(
                detail="Product Not Found",
                status_code=HTTPStatus.NOT_FOUND,
            )
        return self._get_product(product_model)

    async def store(self, product: Product) -> ProductModel:
        new_product = await self.repository.create(product)
        return self._get_product(new_product)

    async def update(self, product_id: str, product: Product) -> Product:
        product_updated = await self.repository.update(product_id, product)
        return self._get_product(product_updated)

    async def delete(self, product_id: int) -> None:
        await self.repository.delete(product_id)


    def _get_product(self, product_model: ProductModel) -> Product:
        return Product(
            id=product_model.id,
            title=product_model.title,
            brand=product_model.brand,
            price=product_model.price,
            image=product_model.image,
            reviewScore=product_model.review_score,
            created_at=product_model.created_at.astimezone(ZoneInfo(DEFAULT_TINE_ZONE)).strftime("%d/%m/%Y %H:%M:%S")
                if isinstance(product_model.created_at, datetime)
                else product_model.created_at,
            updated_at=product_model.updated_at.astimezone(ZoneInfo(DEFAULT_TINE_ZONE)).strftime("%d/%m/%Y %H:%M:%S")
                if isinstance(product_model.updated_at, datetime)
                else product_model.updated_at,
        )
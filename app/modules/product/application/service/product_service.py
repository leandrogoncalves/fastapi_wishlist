import uuid
from http import HTTPStatus
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from pythondi import inject
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from modules.core.config.env import PAGE_SIZE
from modules.core.config.env import DEFAULT_TINE_ZONE
from modules.shared.domain.repository.database.product_repository_abstract import ProductRepositoryAbstract
from modules.product.infrastructure.database.models.product_model import ProductModel
from modules.product.domain.entity.product import Product
from modules.product.domain.entity.product_paginated import ProductPaginated

class ProductService:

    def __init__(self):
        self.repository = self._get_product_repository()

    @inject()
    def _get_product_repository(self, repository: ProductRepositoryAbstract):
        return repository

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

    def _validate_product(self, product_model: ProductModel) -> None:
        if product_model is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Product not found")

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
        self._validate_product(product_model)
        return self._get_product(product_model)

    async def store(self, product: Product) -> ProductModel:
        new_product = ProductModel(
            id=str(uuid.uuid4()),
            title=product.title,
            brand=product.brand,
            price=product.price,
            image=str(product.image),
            review_score=product.reviewScore,
            created_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE)),
            updated_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE))
        )
        return self._get_product(await self.repository.create(new_product))

    async def update(self, product_id: str, product: Product) -> Product:
        product_founded: ProductModel = await self.repository.get_by_id(product_id)
        self._validate_product(product_founded)
        if product.title:
            product_founded.title = product.title
        if product.brand:
            product_founded.brand = product.brand
        if product.price:
            product_founded.price = product.price
        if product.image:
            product_founded.image = str(product.image)
        if product.reviewScore:
            product_founded.review_score = product.reviewScore
        return self._get_product(await self.repository.update(product_founded))

    async def delete(self, product_id: int) -> None:
        product_founded: ProductModel = await self.repository.get_by_id(product_id)
        self._validate_product(product_founded)
        await self.repository.delete(product_founded)

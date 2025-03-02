from abc import ABC, abstractmethod
from typing import List
from modules.product.infrastructure.database.models.product_model import ProductModel
from modules.product.domain.entity.product import Product


class ProductRepositoryAbstract(ABC):
    @abstractmethod
    def get_all_products(self, offset: int, limit: int) -> List[ProductModel]: raise NotImplementedError

    @abstractmethod
    async def count(self) -> int: raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, product_id: str) -> ProductModel: raise NotImplementedError

    @abstractmethod
    async def create(self, product: ProductModel) -> ProductModel: raise NotImplementedError

    @abstractmethod
    async def update(self, product_id: str, product: Product) -> ProductModel: raise NotImplementedError

    @abstractmethod
    async def delete(self, product_id: str) -> None: raise NotImplementedError
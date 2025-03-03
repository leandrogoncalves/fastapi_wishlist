from abc import ABC, abstractmethod
from typing import List
from modules.product.infrastructure.database.models.product_model import ProductModel
from modules.wishlist.domain.entity.wishlist_product_list import WishlistProductList


class WishlistProductRepositoryAbstract(ABC):

    @abstractmethod
    async def get_products_by_wishlist_id(
        self,
        wishlist_id: str
    ) -> List[ProductModel]: raise NotImplementedError

    @abstractmethod
    async def get_products_by_list(
            self,
            wishlist_id: str,
            products_list: WishlistProductList
    ) -> List[ProductModel]: raise NotImplementedError

    @abstractmethod
    async def add_product(self, wishlist_id: str, product_id: str) -> None: raise NotImplementedError

    @abstractmethod
    async def remove_products_by_wishlist_id(
            self,
            wishlist_id: str,
            products_list: WishlistProductList
    ) -> None: raise NotImplementedError

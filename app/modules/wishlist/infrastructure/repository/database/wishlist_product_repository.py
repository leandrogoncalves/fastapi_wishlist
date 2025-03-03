from typing import List
from sqlmodel import select, delete
from modules.core.config.database import get_session
from modules.product.infrastructure.database.models.product_model import ProductModel
from modules.wishlist.infrastructure.database.models.wishlist_product_model import WishlistProductModel
from modules.wishlist.domain.entity.wishlist_product_list import WishlistProductList

class WishlistProductRepository():

    async def get_products_by_wishlist_id(
        self,
        wishlist_id: str
    ) -> List[ProductModel]:
        async with get_session() as session:
            query = select(
                ProductModel
            ).select_from(
                WishlistProductModel
            ).join(
                ProductModel, ProductModel.id == WishlistProductModel.product_id
            ).where(
                WishlistProductModel.wishlist_id == wishlist_id,
            )
            result = await session.execute(query)
            return result.all()

    async def get_products_by_list(
        self,
        wishlist_id: str,
        products_list: WishlistProductList
    ) -> List[ProductModel]:
        async with get_session() as session:
            query = select(
                ProductModel
            ).select_from(
                WishlistProductModel
            ).join(
                ProductModel, ProductModel.id == WishlistProductModel.product_id
            ).where(
                WishlistProductModel.wishlist_id == wishlist_id,
                WishlistProductModel.product_id.in_(products_list.products)
            )
            result = await session.execute(query)
            return result.all()

    async def add_product(self, wishlist_id: str, product_id: str) -> None:
        async with get_session() as session:
            session.add(
                WishlistProductModel(
                    wishlist_id=wishlist_id,
                    product_id=product_id
                )
            )
            await session.commit()

    async def remove_products_by_wishlist_id(
        self,
        wishlist_id: str,
        products_list: WishlistProductList
    ) -> None:
        async with get_session() as session:
            query = (delete(WishlistProductModel)
            .where(
                WishlistProductModel.wishlist_id == wishlist_id,
                WishlistProductModel.product_id.in_(products_list.products)
            ))
            await session.execute(query)
            await session.commit()



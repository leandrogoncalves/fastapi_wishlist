from http import HTTPStatus
from datetime import datetime
from zoneinfo import ZoneInfo
from pythondi import inject
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from modules.core.config.env import DEFAULT_TINE_ZONE
from modules.wishlist.domain.repository.database.wishlist_repository_abstract import WishlistRepositoryAbstract
from modules.shared.domain.repository.database.customer_repository_abstract import CustomerRepositoryAbstract
from modules.shared.domain.repository.database.product_repository_abstract import ProductRepositoryAbstract
from modules.wishlist.domain.repository.database.wishlist_product_repository_abstract import WishlistProductRepositoryAbstract
from modules.customer.infrastructure.database.models.customer_model import CustomerModel
from modules.wishlist.domain.entity.wishlist_product_list import WishlistProductList
from modules.product.infrastructure.database.models.product_model import ProductModel
from modules.product.domain.entity.product import Product


class WishlistService:
    def __init__(self):
        self.wishlist_repository = self.__get_wishlist_repository()
        self.wishlist_product_repository = self.__get_wishlist_product_repository()
        self.customer_repository = self.__get_customer_repository()
        self.product_repository = self.__get_product_repository()

    @inject()
    def __get_wishlist_repository(self, wishlist_repository: WishlistRepositoryAbstract):
        return wishlist_repository

    @inject()
    def __get_wishlist_product_repository(self, wishlist_product_repository: WishlistProductRepositoryAbstract):
        return wishlist_product_repository

    @inject()
    def __get_customer_repository(self, customer_repository: CustomerRepositoryAbstract):
        return customer_repository

    @inject()
    def __get_product_repository(self, product_repository: ProductRepositoryAbstract):
        return product_repository

    async def __get_customer_by_id(self, customer_id: str) -> CustomerModel:
        customer = await self.customer_repository.get_by_id(customer_id)
        if customer is None:
            raise HTTPException(
                detail="Customer Not Found",
                status_code=HTTPStatus.NOT_FOUND,
            )
        return customer

    def __get_wishlist_name(self, customer: CustomerModel) -> str:
        return f"wishlist_%s" % customer.id

    def __get_product_from_model(self, product_model: ProductModel) -> Product:
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

    async def __add_products_to_wishlist(self, wishlist_id: str, wishlist: WishlistProductList) -> None:
        for product_id in wishlist.products:
            product = await self.product_repository.get_by_id(product_id)
            if not product:
                raise HTTPException(
                    detail="Product Not Found",
                    status_code=HTTPStatus.NOT_FOUND,
                )
            await self.wishlist_product_repository.add_product(wishlist_id, product_id)

    async def get_by_customer_id(self, customer_id: str) -> dict:
        customer = await self.__get_customer_by_id(customer_id)
        if customer.wishlist_id is None:
            raise HTTPException(
                detail="Customer has no wishlist. Add products to create a wishlist",
                status_code=HTTPStatus.NOT_FOUND,
            )
        products_list = await self.wishlist_product_repository.get_products_by_wishlist_id(customer.wishlist_id)
        wishlist_products = [
            self.__get_product_from_model(product_model[0]) for product_model in products_list
        ]
        return {
            "wishlist_products": jsonable_encoder(wishlist_products)
        }

    async def set_by_customer_id(self, customer_id: str, wishlist: WishlistProductList) -> None:
        customer = await self.__get_customer_by_id(customer_id)
        if customer.wishlist_id is not None:
            wishlist_model = await self.wishlist_repository.get_by_id(customer.wishlist_id)
            if not wishlist_model:
                raise HTTPException(
                    detail="Wishlist Not Found",
                    status_code=HTTPStatus.NOT_FOUND,
                )

        if customer.wishlist_id is None:
            wishlist_model = await self.wishlist_repository.create(
                self.__get_wishlist_name(customer)
            )
            customer.wishlist_id = wishlist_model.id
            await self.customer_repository.update(customer)

        products_list = await (self.wishlist_product_repository
            .get_products_by_list(customer.wishlist_id, wishlist))
        if len(products_list) > 0:
            raise HTTPException(
                detail="One or more products already exists in the wishlist",
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            )

        await self.__add_products_to_wishlist(customer.wishlist_id, wishlist)

    async def remove_by_customer_id(self, customer_id: str, wishlist: WishlistProductList) -> None:
        customer = await self.__get_customer_by_id(customer_id)
        if customer.wishlist_id is not None:
            wishlist_model = await self.wishlist_repository.get_by_id(customer.wishlist_id)
            if not wishlist_model:
                raise HTTPException(
                    detail="Wishlist Not Found",
                    status_code=HTTPStatus.NOT_FOUND,
                )

        await self.wishlist_product_repository.remove_products_by_wishlist_id(customer.wishlist_id, wishlist)

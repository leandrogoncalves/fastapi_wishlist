import uuid
from datetime import datetime
from zoneinfo import ZoneInfo
from modules.core.config.env import DEFAULT_TINE_ZONE
from modules.core.config.database import get_session
from modules.core.config.security import generate_password_hash
from modules.customer.infrastructure.database.models.customer_model import CustomerModel
from modules.product.infrastructure.database.models.product_model import ProductModel
from modules.wishlist.infrastructure.database.models.wishlist_model import WishlistModel
from modules.wishlist.infrastructure.database.models.wishlist_product_model import WishlistProductModel

class DatabaseSeeder():

    async def seed(self):
        customer = await self.create_customer()
        product = await self.create_product()
        wishlist = await self.create_wishlist()
        await self.update_customer_wishlist(customer, wishlist)
        await self.create_wishlist_product(wishlist, product)
    async def create_customer(self) -> CustomerModel:
        print("Creating new customer")
        new_customer = CustomerModel(
            id=str(uuid.uuid4()),
            name="Customer Admin",
            email="admin@test.com",
            password=generate_password_hash("123456"),
            profile="admin",
            created_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE)),
            updated_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE))
        )
        async with get_session() as session:
            session.add(new_customer)
            await session.commit()
            print("New customer created")
            return new_customer

    async def create_product(self) -> ProductModel:
        print("Creating new product")
        product = ProductModel(
            id=str(uuid.uuid4()),
            title="Test Product",
            brand="Test Product Description",
            price=10.99,
            image="https://example.com/test_product.jpg",
            review_score=4.5,
            created_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE)),
            updated_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE))
        )
        async with get_session() as session:
            session.add(product)
            await session.commit()
            print("New product created")
            return product

    async def create_wishlist(self) -> WishlistModel:
        print("Creating new wishlist")
        new_wishlist = WishlistModel(
            id=str(uuid.uuid4()),
            name="wishlist_test",
            created_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE)),
            updated_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE))
        )
        async with get_session() as session:
            session.add(new_wishlist)
            await session.commit()
            print("New wishlist created")
            return new_wishlist

    async def update_customer_wishlist(self, customer: CustomerModel, wishilist: WishlistModel) -> WishlistModel:
        print("Updating customer wishlist")
        customer.wishlist_id = wishilist.id
        async with get_session() as session:
            customer.updated_at = datetime.now(ZoneInfo(DEFAULT_TINE_ZONE))
            session.add(customer)
            await session.commit()
            print("Customer wishlist updated")
            return customer

    async def create_wishlist_product(self, wishlist: WishlistModel, product: ProductModel):
        print("Creating wishlist product")
        async with get_session() as session:
            session.add(
                WishlistProductModel(
                    wishlist_id=wishlist.id,
                    product_id=product.id
                )
            )
            print("Wishlist product created")
            await session.commit()


if __name__ == '__main__':
    import asyncio
    asyncio.run(DatabaseSeeder().seed())
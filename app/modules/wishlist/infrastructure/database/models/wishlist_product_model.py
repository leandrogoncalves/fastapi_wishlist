from typing import Optional
from sqlmodel import Field, SQLModel


class WishlistProductModel(SQLModel, table=True):
    __tablename__: str = "wishlist_product"
    __table_args__: dict = {"extend_existing": True}

    wishlist_id: Optional[str] = Field(default=None, primary_key=True)
    product_id: Optional[str] = Field(default=None, primary_key=True)

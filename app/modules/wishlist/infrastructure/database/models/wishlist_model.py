from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import Table, Column, String, ForeignKey


wishlist_product = Table(
    "wishlist_product",
    SQLModel.metadata,
    Column("wishlist_id", ForeignKey("wishlists.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True),
)


class WishlistModel(SQLModel, table=True):
    __tablename__: str = "wishlists"

    id: Optional[str] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(100), nullable=True))
    created_at: Optional[datetime] = Field(default=None, nullable=True)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)
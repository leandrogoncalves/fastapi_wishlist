from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String
from modules.wishlist.infrastructure.database.models.wishlist_model import WishlistModel

class CustomerModel(SQLModel, table=True):
    __tablename__: str = "customers"

    id: Optional[str] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(100), nullable=False))
    email: str = Field(sa_column=Column(String(100), nullable=False))
    created_at: Optional[datetime] = Field(default=None, nullable=True)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)
    wishlist_id: Optional[str] = Field(default=None, foreign_key="wishlists.id")

    # wishlist: Optional["WishlistModel"] = Relationship(
    #     back_populates="customer",
    #     sa_relationship_kwargs={"lazy": "select"},
    #     link_model=lambda: WishlistModel
    # )


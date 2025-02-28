from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, String

class ProductModel(SQLModel, table=True):
    __tablename__: str = "products"

    id: Optional[str] = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String(100), nullable=False))
    price: float = Field(default=None, nullable=False)
    brand: str = Field(sa_column=Column(String(100), nullable=False))
    image: str = Field(default=None, nullable=False)
    review_score: float = Field(default=None, nullable=True)
    created_at: Optional[datetime] = Field(default=None, nullable=True)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)


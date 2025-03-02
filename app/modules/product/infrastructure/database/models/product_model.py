from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, String, TIMESTAMP

class ProductModel(SQLModel, table=True):
    __tablename__: str = "products"

    id: Optional[str] = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String(500), nullable=False))
    price: float = Field(default=None, nullable=False)
    brand: str = Field(sa_column=Column(String(100), nullable=False))
    image: Optional[str] = Field(sa_column=Column(String(1000), nullable=True))
    review_score: Optional[float] = Field(default=None, nullable=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=True)
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=True)
    )
    deleted_at: Optional[datetime] = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=True)
    )


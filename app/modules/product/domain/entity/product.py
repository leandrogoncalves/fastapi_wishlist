from typing import Optional
from pydantic import BaseModel, field_validator, HttpUrl


class Product(BaseModel):
    id: Optional[str] = None
    title: str
    brand: str
    price: float
    image: Optional[HttpUrl] = None
    reviewScore: Optional[float] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Confg:
        orm_mode = True

    @field_validator('price')
    def validate_name(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Value of price can not be negative.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "brand": self.brand,
            "image": str(self.image),
            "reviewScore": self.reviewScore,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class ProductUp(Product):
    id: Optional[str] = None
    title: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None
    reviewScore: Optional[int] = None
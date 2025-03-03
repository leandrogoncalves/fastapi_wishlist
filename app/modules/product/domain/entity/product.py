from typing import Optional
from pydantic import BaseModel, field_validator


class Product(BaseModel):
    id: Optional[str] = None
    title: str
    brand: str
    price: float
    image: Optional[str] = None
    reviewScore: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Confg:
        orm_mode = True

    @field_validator('price')
    def validate_name(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Value of price can not be negative.")
        return value

class ProductUp(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None
    reviewScore: Optional[int] = None
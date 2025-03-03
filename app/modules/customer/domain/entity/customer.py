from typing import Optional
import re
from pydantic import BaseModel, field_validator


class Customer(BaseModel):
    id: str = None
    name: str
    email: str
    password: str
    wishlist_id: Optional[str] = None
    is_admin: Optional[bool] = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Confg:
        orm_mode = True

    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long.")
        return value

    @field_validator('email')
    def validate_email(cls, value: str) -> str:
        if re.match( r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value) is None:
            raise ValueError("Invalid email address.")
        return value


class CustomerUp(Customer):
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    wishlist_id: Optional[str] = None
    is_admin: Optional[bool] = None
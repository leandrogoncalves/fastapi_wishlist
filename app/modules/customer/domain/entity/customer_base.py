from typing import Optional
import re
from pydantic import BaseModel, field_validator


class CustomerBase(BaseModel):
    id: Optional[str] = None
    name: str
    email: str

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

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "wishlist_id": self.wishlist_id,
            "profile": self.profile,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

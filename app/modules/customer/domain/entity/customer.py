from typing import Optional
from .customer_base import CustomerBase

class Customer(CustomerBase):
    password: Optional[str] = None
    wishlist_id: Optional[str] = None
    profile: Optional[str] = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class CustomerUp(Customer):
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    wishlist_id: Optional[str] = None
    profile: Optional[str] = None
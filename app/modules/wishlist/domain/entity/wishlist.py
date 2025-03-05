from typing import Optional
from pydantic import BaseModel


class Wishlist(BaseModel):
    id: Optional[str] = None
    name: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class WishlistUp(Wishlist):
    id: Optional[str] = None
    name: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
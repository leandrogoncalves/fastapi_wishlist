from typing import Optional
from pydantic import BaseModel


class WishlistProduct(BaseModel):
    wishlist_id: Optional[str] = None
    product_id: Optional[str] = None

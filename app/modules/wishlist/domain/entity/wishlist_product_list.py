from typing import Optional
from pydantic import BaseModel


class WishlistProductList(BaseModel):
    products: Optional[list] = None

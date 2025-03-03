from http import HTTPStatus
from fastapi import HTTPException
from modules.core.helpers.config_logger import get_logger
from modules.wishlist.domain.entity.wishlist_product_list import WishlistProductList

logger = get_logger()


def wishlist_validator(wishlist: WishlistProductList) -> WishlistProductList:

    fields = [
        'products',
    ]

    for field in fields:
        if not getattr(wishlist, field):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f"The field {field} could not be empty"
            )

    if len(wishlist.products) != len(set(wishlist.products)):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Duplicate products found in the wishlist"
        )

    return wishlist
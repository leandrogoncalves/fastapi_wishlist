from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["Wishlist"]
)


@router.get("/wishlist")
async def get_wishlists():
    return [{'id': 1}]


@router.get("/wishlist/{wishlist_id}")
async def get_wishlist_by_id(wishlist_id: int):
    return {'id': wishlist_id}


@router.post("/wishlist")
async def create_wishlist():
    return [{'id': 1}]


@router.put("/wishlist/{wishlist_id}")
async def update_wishlist(wishlist_id: int):
    return wishlist_id


@router.delete("/wishlist/{wishlist_id}")
async def delete_wishlist(wishlist_id: int):
    return {"id": wishlist_id}
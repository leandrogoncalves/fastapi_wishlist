from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["Products"]
)


@router.get("/products")
async def get_products():
    return [{'id': 1}]


@router.get("/products/{product_id}")
async def get_product_by_id(product_id: int):
    return {'id': product_id}


@router.post("/products")
async def create_product():
    return [{'id': 1}]


@router.put("/products/{product_id}")
async def update_product(product_id: int):
    return product_id


@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    return {"id": product_id}
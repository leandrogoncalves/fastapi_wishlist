from http import HTTPStatus
from fastapi import HTTPException
from modules.product.domain.entity.product import Product

def product_validator(product: Product) -> Product:

    fields = [
        'title',
        'brand',
        'price',
    ]

    for field in fields:
        if not getattr(product, field):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f"The field {field} could not be empty"
            )

    return product
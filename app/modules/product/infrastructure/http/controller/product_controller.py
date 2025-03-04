from typing import Annotated, List, Union
from http import HTTPStatus
from fastapi import APIRouter, Depends, Query, Path, HTTPException, Response, Request, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from modules.core.helpers.config_logger import get_logger
from modules.product.application.service.product_service import ProductService
from modules.product.domain.entity.product import Product, ProductUp

logger = get_logger()

bearer_scheme = HTTPBearer()

router = APIRouter(
    prefix="/api",
    tags=["Products"]
)


@router.get(
    path="/product",
    description="Get all products",
    summary="Get all products",
    response_model=List[Product],
    dependencies=[Security(bearer_scheme)]
)
async def get_products(
    product_service: Annotated[ProductService, Depends(ProductService)],
    page: int = Query(1, ge=1, title="Page Number", description="Page number"),
) -> JSONResponse:
    try:
        product_paginated = await product_service.get_all_paginated(page)
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content=product_paginated.to_dict()
        )
    except Exception as e:
        logger.error(f"Error getting all products: {e}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"}
        )


@router.get(
    path="/product/{product_id}",
    description="Get product by id or null",
    summary="Get product by id",
    response_model=Product,
    dependencies=[Security(bearer_scheme)]
)
async def get_product_by_id(
    product_service: Annotated[ProductService, Depends(ProductService)],
    product_id: str = Path(title="Product Id", description="Product Id")
) -> JSONResponse:
    try:
        return await product_service.get_by_id(product_id)
    except HTTPException as ehttp:
        logger.error(f"Error getting product: {ehttp}")
        return JSONResponse(
            status_code=ehttp.status_code,
            content={"error": ehttp.detail}
        )
    except Exception as e:
        logger.error(f"Error getting product by id: {e}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"}
        )


@router.post(
    path="/product",
    status_code=HTTPStatus.CREATED,
    description="Create a new product or fail",
    summary="Create a new product",
    response_model=Product,
    dependencies=[Security(bearer_scheme)]
)
async def create_product(
    request: Request,
    product_service: Annotated[ProductService, Depends(ProductService)],
    product: Product
) -> JSONResponse:
    try:
        if request.state.user.profile != "admin":
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Forbidden")

        return await product_service.store(product)
    except HTTPException as ehttp:
        logger.error(f"Error creating product: {ehttp}")
        return JSONResponse(
            status_code=ehttp.status_code,
            content={"error": ehttp.detail}
        )
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"}
        )


@router.put(
    path="/product/{product_id}",
    description="Update a product by Id or fail",
    summary="Update a product by id",
    response_model=Product,
    dependencies=[Security(bearer_scheme)]
)
async def update_product(
    request: Request,
    product_service: Annotated[ProductService, Depends(ProductService)],
    product_id: str,
    product: ProductUp
) -> JSONResponse:
    try:
        if request.state.user.profile != "admin":
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Forbidden")

        return await product_service.update(product_id, product)
    except HTTPException as ehttp:
        logger.error(f"Error updating product: {ehttp}")
        return JSONResponse(
            status_code=ehttp.status_code,
            content={"error": ehttp.detail}
        )
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"}
        )


@router.delete(
    path="/product/{product_id}",
    description="Delete a product or fail",
    summary="Update a product",
    response_model=None,
    dependencies=[Security(bearer_scheme)]
)
async def delete_product(
    request: Request,
    product_service: Annotated[ProductService, Depends(ProductService)],
    product_id: str
) -> Union[Response, JSONResponse]:
    try:
        if request.state.user.profile != "admin":
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Forbidden")

        await product_service.delete(product_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)
    except HTTPException as ehttp:
        logger.error(f"Error deleting product: {ehttp}")
        return JSONResponse(
            status_code=ehttp.status_code,
            content={"error": ehttp.detail}
        )
    except Exception as e:
        logger.error(f"Error deleting all products: {e}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"}
        )

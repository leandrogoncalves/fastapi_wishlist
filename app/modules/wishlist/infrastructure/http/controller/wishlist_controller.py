from typing import Annotated, Union
from http import HTTPStatus
from fastapi import APIRouter, Depends, Path, HTTPException, Response
from fastapi.responses import JSONResponse
from modules.core.helpers.config_logger import get_logger
from modules.wishlist.application.service.wishlist_service import WishlistService
from modules.wishlist.domain.entity.wishlist_product_list import WishlistProductList
from modules.wishlist.infrastructure.http.validator.wishlist_validator import wishlist_validator


logger = get_logger()

router = APIRouter(
    prefix="/api",
    tags=["Wishlist"]
)


@router.get("/customer/{customer_id}/wishlist",
    description="Get wishlist by customer id",
    summary="Get wishlist by customer id",
)
async def get_wishlist_by_customer_id(
    wishlist_service: Annotated[WishlistService, Depends(WishlistService)],
    customer_id: str = Path(title="Customer Id", description="Customer Id")
) -> JSONResponse:
    try:
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content=await wishlist_service.get_by_customer_id(customer_id)
        )
    except HTTPException as ehttp:
        logger.error(f"Error getting wishlist: {ehttp}")
        return JSONResponse(
            status_code=ehttp.status_code,
            content={"error": ehttp.detail}
        )
    except Exception as e:
        logger.error(f"Error getting all wishlist by customer: {e}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"}
        )


@router.post("/customer/{customer_id}/wishlist",
    description="Get wishlist by customer id",
    summary="Get wishlist by customer id",
    response_model=None
)
async def set_wishlist_by_customer_id(
    wishlist_service: Annotated[WishlistService, Depends(WishlistService)],
    customer_id: str = Path(title="Customer Id", description="Customer Id"),
    wishlist_products: WishlistProductList = Depends(wishlist_validator)
) -> Union[Response, JSONResponse]:
    try:
        await wishlist_service.set_by_customer_id(customer_id, wishlist_products)
        return Response(status_code=HTTPStatus.NO_CONTENT)
    except HTTPException as ehttp:
        logger.error(f"Error setting wishlist: {ehttp}")
        return JSONResponse(
            status_code=ehttp.status_code,
            content={"error": ehttp.detail}
        )
    except Exception as e:
        logger.error(f"Error setting all wishlist by customer: {e}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"}
        )

@router.delete("/customer/{customer_id}/wishlist",
    description="Remove product from wishlist by customer id",
    summary="Remove product from wishlist by customer id",
    response_model=None
)
async def set_wishlist_by_customer_id(
    wishlist_service: Annotated[WishlistService, Depends(WishlistService)],
    customer_id: str = Path(title="Customer Id", description="Customer Id"),
    wishlist_products: WishlistProductList = Depends(wishlist_validator)
) -> Union[Response, JSONResponse]:
    try:
        await wishlist_service.remove_by_customer_id(customer_id, wishlist_products)
        return Response(status_code=HTTPStatus.NO_CONTENT)
    except HTTPException as ehttp:
        logger.error(f"Error removing products from wishlist: {ehttp}")
        return JSONResponse(
            status_code=ehttp.status_code,
            content={"error": ehttp.detail}
        )
    except Exception as e:
        logger.error(f"Error removing products from wishlist by customer: {e}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"}
        )


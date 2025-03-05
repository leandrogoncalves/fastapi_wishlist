from typing import Annotated, List, Union
from http import HTTPStatus
from fastapi import APIRouter, Depends, Query, Path, HTTPException, Response, Request, Security
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from modules.core.helpers.config_logger import get_logger
from modules.customer.application.service.customer_service import CustomerService
from modules.customer.domain.entity.customer import Customer, CustomerUp
from modules.customer.domain.entity.customer_filtered import CustomerFiltered

logger = get_logger()

bearer_scheme = HTTPBearer()

router = APIRouter(
    prefix="/api",
    tags=["Customers"]
)


@router.get(
    path="/customer",
    description="Get all customers",
    summary="Get all customers",
    response_model=List[CustomerFiltered],
    dependencies=[Security(bearer_scheme)]
)
async def get_customers(
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    page: int = Query(1, ge=1, title="Page Number", description="Page number"),
) -> JSONResponse:
    try:
        customer_paginated = await customer_service.get_all_paginated(page)
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content=customer_paginated.to_dict()
        )
    except Exception as e:
        logger.error(f"Error getting all customers: {e}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"}
        )


@router.get(
    path="/customer/{customer_id}",
    description="Get customer by id or null",
    summary="Get customer by id",
    response_model=CustomerFiltered,
    dependencies=[Security(bearer_scheme)]
)
async def get_customer_by_id(
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    customer_id: str = Path(title="Customer Id", description="Customer Id")
) -> JSONResponse:
    try:
        response = await customer_service.get_by_id(customer_id)
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content=response.to_dict()
        )
    except HTTPException as ehttp:
        logger.error(f"Error getting customer: {ehttp}")
        return JSONResponse(
            status_code=ehttp.status_code,
            content={"error": ehttp.detail}
        )
    except Exception as e:
        logger.error(f"Error getting customer by id: {e}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"}
        )


@router.post(
    path="/customer",
    status_code=HTTPStatus.CREATED,
    description="Create a new customer or fail",
    summary="Create a new customer",
    response_model=CustomerFiltered,
    dependencies=[Security(bearer_scheme)]
)
async def create_customer(
    request: Request,
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    customer: Customer
) -> JSONResponse:
    # try:
        if request.state.user.profile != "admin":
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Forbidden")

        response = await customer_service.store(customer)
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content=response.to_dict()
        )
    # except HTTPException as ehttp:
    #     logger.error(f"Error creating customer: {ehttp}")
    #     return JSONResponse(
    #         status_code=ehttp.status_code,
    #         content={"error": ehttp.detail}
    #     )
    # except Exception as e:
    #     logger.error(f"Error creating customer: {e}")
    #     return JSONResponse(
    #         status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    #         content={"error": "Internal Server Error"}
    #     )


@router.put(
    path="/customer/{customer_id}",
    description="Update a customer by Id or fail",
    summary="Update a customer by id",
    response_model=CustomerFiltered,
    dependencies=[Security(bearer_scheme)]
)
async def update_customer(
    request: Request,
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    customer_id: str,
    customer: CustomerUp
) -> JSONResponse:
    try:
        if request.state.user.profile != "admin":
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Forbidden")
        response = await customer_service.update(customer_id, customer)
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content=response.to_dict()
        )
    except HTTPException as ehttp:
        logger.error(f"Error updating customer: {ehttp}")
        return JSONResponse(
            status_code=ehttp.status_code,
            content={"error": ehttp.detail}
        )
    except Exception as e:
        logger.error(f"Error updating customer: {e}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"}
        )


@router.delete(
    path="/customer/{customer_id}",
    description="Delete a customer or fail",
    summary="Update a customer",
    response_model=None,
    dependencies=[Security(bearer_scheme)]
)
async def delete_customer(
    request: Request,
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    customer_id: str
) -> Union[Response, JSONResponse]:
    try:
        if request.state.user.profile != "admin":
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Forbidden")

        await customer_service.delete(customer_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)
    except HTTPException as ehttp:
        logger.error(f"Error deleting customer: {ehttp}")
        return JSONResponse(
            status_code=ehttp.status_code,
            content={"error": ehttp.detail}
        )
    except Exception as e:
        logger.error(f"Error deleting all customers: {e}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"}
        )

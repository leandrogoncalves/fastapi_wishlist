from typing import Annotated, List
from http import HTTPStatus
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from modules.core.helpers.config_logger import get_logger
from modules.customer.application.service.customer_service import CustomerService
from modules.customer.domain.entity.customer import Customer

logger = get_logger()

router = APIRouter(
    prefix="/api",
    tags=["Customers"]
)


@router.get("/customers",
            description="Get all customers",
            summary="Get all customers",
            response_model=List[Customer]
            )
async def get_customers(
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    page: int = Query(1, ge=1),
) -> JSONResponse:
    # try:
        customer_paginated = await customer_service.get_all_paginated(page)
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content=customer_paginated.to_dict()
        )
    # except Exception as e:
    #     logger.error(f"Error getting all customers: {e}")
    #     return JSONResponse(
    #         status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    #         content={"error": "Internal Server Error"}
    #     )


@router.get("/customers/{customer_id}",
            description="Get customer by id or null",
            summary="Get customer by id",
            response_model=Customer
            )
async def get_customer_by_id(customer_id: int):
    return {'id': customer_id}


@router.post("/customers",
            status_code=HTTPStatus.CREATED,
            description="Create a new customer or fail",
            summary="Create a new customer",
            response_model=Customer
            )
async def create_customer(customer: Customer):
    return [{'id': 1}]


@router.put("/customers/{customer_id}",
            description="Update a customer by Id or fail",
            summary="Update a customer by id",
            response_model=Customer
            )
async def update_customer(customer_id: int, customer: Customer):
    return customer_id


@router.delete("/customers/{customer_id}",
                description="Delete a customer or fail",
                summary="Update a customer",
                response_model=None
                )
async def delete_customer(customer_id: int):
    return {"id": customer_id}

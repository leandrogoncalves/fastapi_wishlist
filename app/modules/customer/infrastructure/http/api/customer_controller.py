from typing import Annotated
from http import HTTPStatus
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from modules.core.helpers.config_logger import get_logger
from modules.customer.application.service.customer_service import CustomerService
from modules.customer.domain.entity.customer import Customer

logger = get_logger()

router = APIRouter(
    prefix="/api",
    tags=["Customers"]
)


@router.get("/customers")
async def get_customers(customer_service: Annotated[CustomerService, Depends(CustomerService)]):
    try:
        all_customers = await customer_service.get_all()
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={"customers": all_customers}
        )
    except Exception as e:
        logger.error(f"Error getting all customers: {e}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"}
        )


@router.get("/customers/{customer_id}")
async def get_customer_by_id(customer_id: int):
    return {'id': customer_id}


@router.post("/customers")
async def create_customer(customer: Customer):
    return [{'id': 1}]


@router.put("/customers/{customer_id}")
async def update_customer(customer_id: int, customer: Customer):
    return customer_id


@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int):
    return {"id": customer_id}
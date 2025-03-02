from http import HTTPStatus
from fastapi import HTTPException
from modules.customer.domain.entity.customer import Customer

def customer_validator(customer: Customer) -> Customer:

    fields = [
        'name',
        'email',
    ]

    for field in fields:
        if not getattr(customer, field):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f"The field {field} could not be empty"
            )

    return customer
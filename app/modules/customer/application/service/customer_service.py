from http import HTTPStatus
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from pythondi import inject
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from modules.core.config.env import PAGE_SIZE
from modules.core.config.env import DEFAULT_TINE_ZONE
from modules.customer.domain.repository.database.customer_repository_abstract import CustomerRepositoryAbstract
from modules.customer.infrastructure.database.models.customer_model import CustomerModel
from modules.customer.domain.entity.customer import Customer
from modules.customer.domain.entity.customer_paginated import CustomerPaginated

class CustomerService:

    def __init__(self):
        self.repository = self._get_customer_repository()

    @inject()
    def _get_customer_repository(self, repository: CustomerRepositoryAbstract):
        return repository

    async def get_all_paginated(self, page: int) -> CustomerPaginated:
        total = await self.count_all()
        total_pages = round(total / PAGE_SIZE)
        offset = (page - 1) * PAGE_SIZE
        data = await self.repository.get_all_customers(offset, PAGE_SIZE)
        customer_data = [self._get_customer(customer) for customer in data]
        return CustomerPaginated(
            page=page,
            total_pages=total_pages or 1,
            total_results=total,
            results_in_page=len(customer_data),
            data=jsonable_encoder(customer_data)
        )

    async def count_all(self) -> int:
        return await self.repository.count()

    async def get_by_id(self, customer_id: str) -> Optional[Customer]:
        customer_model: CustomerModel = await self.repository.get_by_id(customer_id)
        if customer_model is None:
            raise HTTPException(
                detail="Customer Not Found",
                status_code=HTTPStatus.NOT_FOUND,
            )
        return self._get_customer(customer_model)

    async def store(self, customer: Customer) -> CustomerModel:
        customer_model: CustomerModel = await self.repository.get_by_email(customer.email)
        if isinstance(customer_model, CustomerModel):
            raise HTTPException(
                detail=f"Customer already exists with this email address: {customer.email}",
                status_code=HTTPStatus.PRECONDITION_FAILED,
            )
        new_customer = await self.repository.create(customer)
        return self._get_customer(new_customer)

    async def update(self, customer_id: str, customer: Customer) -> Customer:
        customer_updated = await self.repository.update(customer_id, customer)
        return self._get_customer(customer_updated)

    async def delete(self, customer_id: int) -> None:
        await self.repository.delete(customer_id)


    def _get_customer(self, customer_model: CustomerModel) -> Customer:
        return Customer(
            id=customer_model.id,
            name=customer_model.name,
            email=customer_model.email,
            created_at=customer_model.created_at.astimezone(ZoneInfo(DEFAULT_TINE_ZONE)).strftime("%d/%m/%Y %H:%M:%S")
                if isinstance(customer_model.created_at, datetime)
                else customer_model.created_at,
            updated_at=customer_model.updated_at.astimezone(ZoneInfo(DEFAULT_TINE_ZONE)).strftime("%d/%m/%Y %H:%M:%S")
                if isinstance(customer_model.updated_at, datetime)
                else customer_model.updated_at,
        )
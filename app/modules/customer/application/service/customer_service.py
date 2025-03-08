import uuid
from http import HTTPStatus
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from pythondi import inject
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from modules.core.config.env import PAGE_SIZE
from modules.core.config.env import DEFAULT_TINE_ZONE
from modules.core.config.security import generate_password_hash
from modules.shared.domain.repository.database.customer_repository_abstract import CustomerRepositoryAbstract
from modules.customer.infrastructure.database.models.customer_model import CustomerModel
from modules.customer.domain.entity.customer import Customer
from modules.customer.domain.entity.customer_filtered import CustomerFiltered
from modules.customer.domain.entity.customer_paginated import CustomerPaginated


class CustomerService():

    def __init__(self):
        self.repository = self.__get_customer_repository()

    @inject()
    def __get_customer_repository(self, repository: CustomerRepositoryAbstract):
        return repository

    async def __validate_unique_email(self, customer) -> None:
        customer_model: CustomerModel = await self.repository.get_by_email(customer.email)
        if isinstance(customer_model, CustomerModel):
            raise HTTPException(
                detail=f"Customer already exists with this email address: {customer.email}",
                status_code=HTTPStatus.PRECONDITION_FAILED,
            )

    def __get_customer_filtered(self, customer_model: CustomerModel) -> CustomerFiltered:
        return CustomerFiltered(
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

    def __validate_customer(self, customer_model: CustomerModel) -> None:
        if customer_model is None:
            raise HTTPException(
                detail="Customer Not Found",
                status_code=HTTPStatus.NOT_FOUND,
            )

    async def get_all_paginated(self, page: int) -> CustomerPaginated:
        total = await self.count_all()
        total_pages = round(total / PAGE_SIZE)
        offset = (page - 1) * PAGE_SIZE
        data = await self.repository.get_all_customers(offset, PAGE_SIZE)
        customer_data = [self.__get_customer_filtered(customer) for customer in data]
        return CustomerPaginated(
            page=page,
            total_pages=total_pages or 1,
            total_results=total,
            results_in_page=len(customer_data),
            data=jsonable_encoder(customer_data)
        )

    async def count_all(self) -> int:
        return await self.repository.count()

    async def get_by_id(self, customer_id: str) -> Optional[CustomerFiltered]:
        customer_model: CustomerModel = await self.repository.get_by_id(customer_id)
        self.__validate_customer(customer_model)
        return self.__get_customer_filtered(customer_model)

    async def store(self, customer: Customer) -> CustomerFiltered:
        await self.__validate_unique_email(customer)
        new_customer = CustomerModel(
            id=str(uuid.uuid4()),
            name=customer.name,
            email=customer.email,
            profile=customer.profile if customer.profile else "viewer",
            password=generate_password_hash(customer.password) if customer.password else None,
            created_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE)),
            updated_at=datetime.now(ZoneInfo(DEFAULT_TINE_ZONE))
        )
        return self.__get_customer_filtered(await self.repository.create(new_customer))

    async def update(self, customer_id: str, customer: Customer) -> CustomerFiltered:
        customer_founded: CustomerModel = await self.repository.get_by_id(customer_id)
        self.__validate_customer(customer_founded)
        await self.__validate_unique_email(customer)
        if customer.name:
            customer_founded.name = customer.name
        if customer.email:
            customer_founded.email = customer.email
        if customer.password:
            customer_founded.password = generate_password_hash(customer.password)
        if customer.profile:
            customer_founded.is_aprofiledmin = customer.profile
        customer_updated = await self.repository.update(customer_founded)
        return self.__get_customer_filtered(customer_updated)

    async def delete(self, customer_id: int) -> None:
        customer_model: CustomerModel = await self.repository.get_by_id(customer_id)
        self.__validate_customer(customer_model)
        await self.repository.delete(customer_model)

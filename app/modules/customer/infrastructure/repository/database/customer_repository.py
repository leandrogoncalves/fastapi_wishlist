import uuid
from http import HTTPStatus
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlmodel import select
from sqlalchemy import func
from fastapi import HTTPException
from modules.customer.domain.repository.database.customer_repository_abstract import CustomerRepositoryAbstract
from modules.customer.infrastructure.database.models.customer_model import CustomerModel
from modules.customer.domain.entity.customer import Customer
from modules.core.config.database import get_session


class CustomerRepository(CustomerRepositoryAbstract):

    async def get_all_customers(self, offset: int, limit: int) -> list:
        async with get_session() as session:
            query = select(CustomerModel).offset(offset).limit(limit)
            result = await session.execute(query)
            customers = result.scalars().all()
            return customers

    async def count(self) -> int:
        async with get_session() as session:
            query = select(func.count()).select_from(CustomerModel)
            result = await session.execute(query)
            total = result.scalar_one()
            return total

    async def get_by_id(self, customer_id):
        async with get_session() as session:
            query = select(CustomerModel).filter(CustomerModel.id == customer_id)
            result = await session.execute(query)
            customer: CustomerModel = result.scalar_one_or_none()
            return customer

    async def create(self, customer: Customer):
        new_customer = CustomerModel(
            id=str(uuid.uuid4()),
            name=customer.name,
            email=customer.email,
            created_at=datetime.now(ZoneInfo("America/Sao_Paulo")),
            updated_at=datetime.now(ZoneInfo("America/Sao_Paulo"))
        )
        async with get_session() as session:
            session.add(new_customer)
            await session.commit()
            return new_customer

    async def update(self, customer_id: str, customer: Customer) -> CustomerModel:
        customer_founded = await self.get_by_id(customer_id)
        if customer_founded is None:
            raise HTTPException(
                detail="Customer Not Found",
                status_code=HTTPStatus.NOT_FOUND,
            )
        async with get_session() as session:
            customer_founded.name = customer.name
            customer_founded.email = customer.email
            customer_founded.updated_at = datetime.now()
            session.add(customer_founded)
            await session.commit()
            session.refresh(customer)
            return customer_founded

    async def delete(self, customer_id: str):
        customer_founded = await self.get_by_id(customer_id)
        if customer_founded is None:
            raise HTTPException(
                detail="Customer Not Found",
                status_code=HTTPStatus.NOT_FOUND,
            )
        async with get_session() as session:
            await session.delete(customer_founded)
            await session.commit()
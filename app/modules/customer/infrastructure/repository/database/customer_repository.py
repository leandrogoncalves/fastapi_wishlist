from typing import List
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlmodel import select
from sqlalchemy import func
from modules.core.config.env import DEFAULT_TINE_ZONE
from modules.shared.domain.repository.database.customer_repository_abstract import CustomerRepositoryAbstract
from modules.customer.infrastructure.database.models.customer_model import CustomerModel
from modules.core.config.database import get_session


class CustomerRepository(CustomerRepositoryAbstract):

    async def get_all_customers(self, offset: int, limit: int) -> List[CustomerModel]:
        async with get_session() as session:
            query = select(CustomerModel).offset(offset).where(CustomerModel.deleted_at.is_(None)).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()

    async def count(self) -> int:
        async with get_session() as session:
            query = select(func.count()).select_from(CustomerModel).where(CustomerModel.deleted_at.is_(None))
            result = await session.execute(query)
            return result.scalar_one()

    async def get_by_id(self, customer_id: str) -> CustomerModel:
        async with get_session() as session:
            query = select(CustomerModel).where(
                CustomerModel.id == customer_id,
                CustomerModel.deleted_at.is_(None)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> CustomerModel:
        async with get_session() as session:
            query = select(CustomerModel).where(CustomerModel.email == email)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def create(self, new_customer: CustomerModel) -> CustomerModel:
        async with get_session() as session:
            session.add(new_customer)
            await session.commit()
            return new_customer

    async def update(self, customer_founded: CustomerModel) -> CustomerModel:
        async with get_session() as session:
            customer_founded.updated_at = datetime.now(ZoneInfo(DEFAULT_TINE_ZONE))
            session.add(customer_founded)
            await session.commit()
            return customer_founded

    async def delete(self, customer_founded: CustomerModel) -> None:
        async with get_session() as session:
            customer_founded.deleted_at = datetime.now(ZoneInfo(DEFAULT_TINE_ZONE))
            session.add(customer_founded)
            # await session.delete(customer_founded)
            await session.commit()

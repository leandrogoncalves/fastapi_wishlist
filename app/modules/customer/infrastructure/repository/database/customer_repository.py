from modules.customer.domain.repository.database.customer_repository_abstract import CustomerRepositoryAbstract
from modules.customer.infrastructure.database.models.customer_model import CustomerModel
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.core.config.deps import get_session
from sqlmodel import select
from sqlalchemy import func


class CustomerRepository(CustomerRepositoryAbstract):

    def get_all_customers(self, page: int, offset: int) -> list:
        return [{'id': 1, 'name': 'John Doe'}]

    async def count(self) -> int:
        async with get_session() as session:
            query = select(func.count()).select_from(CustomerModel)
            result = await session.execute(query)
            total = result.scalar_one()
            print(total)
            return total

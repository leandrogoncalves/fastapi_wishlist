from pythondi import inject
from modules.core.config.env import PAGE_SIZE
from modules.customer.domain.repository.database.customer_repository_abstract import CustomerRepositoryAbstract
from modules.customer.domain.entity.customer_paginated import CustomerPaginated

class CustomerService:

    def __init__(self):
        self.repository = self._get_repository()

    @inject()
    def _get_repository(self, repository: CustomerRepositoryAbstract):
        return repository

    async def get_all_paginated(self, page) -> CustomerPaginated:
        total = await self.count_all()
        total_pages = round(total / PAGE_SIZE)
        offset = (page - 1) * PAGE_SIZE
        data = self.repository.get_all_customers(page, offset)
        return CustomerPaginated(page=page, total_pages=total_pages, total_results=total, data=data)

    async def count_all(self) -> int:
        return await self.repository.count()
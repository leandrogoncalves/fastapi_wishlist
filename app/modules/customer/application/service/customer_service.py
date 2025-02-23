from pythondi import inject
from modules.customer.domain.repository.database.customer_repository_abstract import CustomerRepositoryAbstract


class CustomerService:
    @inject()
    async def get_all(self, repository: CustomerRepositoryAbstract) -> list:
        return repository.get_all_customers()
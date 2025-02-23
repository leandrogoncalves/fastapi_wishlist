from pythondi import inject
from modules.customer.domain.repository.database.customer_repository_abstract import CustomerRepositoryAbstract


class CustomerService:

    def __init__(self):
        self.repository = self._get_repository()

    @inject()
    def _get_repository(self, repository: CustomerRepositoryAbstract):
        return repository

    async def get_all(self) -> list:
        return self.repository.get_all_customers()
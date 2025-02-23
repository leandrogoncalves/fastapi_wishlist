from modules.customer.domain.repository.database.customer_repository_abstract import CustomerRepositoryAbstract

class CustomerRepository(CustomerRepositoryAbstract):
    def get_all_customers(self) -> list:
        return [{'id': 1, 'name': 'John Doe'}]
from pythondi import Provider
from pythondi import configure

from modules.customer.domain.repository.database.customer_repository_abstract import CustomerRepositoryAbstract
from modules.customer.infrastructure.repository.database.customer_repository import CustomerRepository

provider = Provider()
provider.bind(CustomerRepositoryAbstract, CustomerRepository)

config = configure(provider=provider)
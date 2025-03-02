from pythondi import Provider
from pythondi import configure

from modules.customer.domain.repository.database.customer_repository_abstract import CustomerRepositoryAbstract
from modules.customer.infrastructure.repository.database.customer_repository import CustomerRepository
from modules.product.domain.repository.database.product_repository_abstract import ProductRepositoryAbstract
from modules.product.infrastructure.repository.database.product_repository import ProductRepository

provider = Provider()
provider.bind(CustomerRepositoryAbstract, CustomerRepository)
provider.bind(ProductRepositoryAbstract, ProductRepository)

config = configure(provider=provider)
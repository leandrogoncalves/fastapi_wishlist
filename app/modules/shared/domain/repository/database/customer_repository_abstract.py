from abc import ABC, abstractmethod
from typing import List
from modules.customer.infrastructure.database.models.customer_model import CustomerModel
from modules.customer.domain.entity.customer import Customer


class CustomerRepositoryAbstract(ABC):
    @abstractmethod
    def get_all_customers(self, offset: int, limit: int) -> List[CustomerModel]: raise NotImplementedError

    @abstractmethod
    async def count(self) -> int: raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, customer_id: str) -> CustomerModel: raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> CustomerModel: raise NotImplementedError

    @abstractmethod
    async def create(self, customer: CustomerModel) -> CustomerModel: raise NotImplementedError

    @abstractmethod
    async def update(self, customer_id: str, customer: Customer) -> CustomerModel: raise NotImplementedError

    @abstractmethod
    async def delete(self, customer_id: str) -> None: raise NotImplementedError
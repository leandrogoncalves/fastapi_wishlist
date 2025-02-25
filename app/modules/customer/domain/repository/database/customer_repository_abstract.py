from abc import ABC, abstractmethod

class CustomerRepositoryAbstract(ABC):
    @abstractmethod
    def get_all_customers(self, page: int, offset: int) -> list: raise NotImplementedError
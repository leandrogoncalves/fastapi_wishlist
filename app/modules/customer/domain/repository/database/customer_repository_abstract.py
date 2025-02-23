from abc import ABC, abstractmethod

class CustomerRepositoryAbstract(ABC):
    @abstractmethod
    def get_all_customers(self) -> list: raise NotImplementedError
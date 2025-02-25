from typing import List
from pydantic import BaseModel
from modules.customer.domain.entity.customer import Customer


class CustomerPaginated(BaseModel):
    page: int
    total_pages: int
    total_results: int
    data: list #List[Customer]

    def to_dict(self):
        return {
            'page': self.page,
            'total_pages': self.total_pages,
            'total_results': self.total_results,
            'data': self.data
        }

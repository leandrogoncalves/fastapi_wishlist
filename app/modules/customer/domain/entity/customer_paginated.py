from typing import Optional
from pydantic import BaseModel
from modules.core.config.env import PAGE_SIZE

class CustomerPaginated(BaseModel):
    page: int
    total_pages: int
    total_results: int
    results_in_page: int = PAGE_SIZE
    data: Optional[list] = None

    def to_dict(self):
        return {
            'page': self.page,
            'total_pages': self.total_pages,
            'total_results': self.total_results,
            'results_in_page': self.results_in_page,
            'data': self.data
        }

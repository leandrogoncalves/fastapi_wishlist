from abc import ABC, abstractmethod
from modules.wishlist.infrastructure.database.models.wishlist_model import WishlistModel


class WishlistRepositoryAbstract(ABC):
    @abstractmethod
    async def create(self, wishlist_name: str) -> WishlistModel: raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, wishlist_id: str) -> WishlistModel: raise NotImplementedError

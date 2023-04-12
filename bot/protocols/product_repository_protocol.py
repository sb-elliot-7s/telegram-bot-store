from abc import ABC, abstractmethod

from schemas import Brand, Category


class ProductRepositoryProtocol(ABC):

    @abstractmethod
    async def search(self, product_name: str):
        pass

    @abstractmethod
    async def get_products(self, brand: str, category: str, page: int = 1) -> list:
        pass

    @abstractmethod
    async def get_categories(self, brand: str) -> list[Category]:
        pass

    @abstractmethod
    async def get_brands(self) -> list[Brand]:
        pass

    @abstractmethod
    async def get_product(self, product_id: str | int):
        pass

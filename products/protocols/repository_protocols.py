from abc import ABC, abstractmethod


class ProductRepositoryProtocol(ABC):
    @abstractmethod
    async def get_brands(self): pass

    @abstractmethod
    async def get_categories(self, brand: str): pass

    @abstractmethod
    async def count_of_products(self, brand: str, category: str): pass

    @abstractmethod
    async def get_products(self, brand: str, category: str, page: int | None = None) -> list:
        pass

    @abstractmethod
    async def search(self, title: str): pass

    @abstractmethod
    async def get_specifications(self, product_id: str | int): pass

    @abstractmethod
    async def product(self, product_id: int | str): pass

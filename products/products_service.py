from dataclasses import dataclass

from protocols.products_repository_protocol import ProductRepositoryProtocol


@dataclass
class ProductsService:
    repository: ProductRepositoryProtocol

    async def get_brands(self):
        return await self.repository.get_brands()

    async def get_categories(self, brand: str):
        return await self.repository.get_categories(brand=brand)

    async def count_of_products(self, brand: str, category: str):
        return await self.repository.count_of_products(brand=brand, category=category)

    async def get_products(self, brand: str, category: str, page: int | None = None) -> list:
        return await self.repository.get_products(brand=brand, category=category, page=page)

    async def search(self, title: str):
        return await self.repository.search(title=title)

    async def get_specifications(self, product_id: str | int):
        return await self.repository.get_specifications(product_id=product_id)

    async def product(self, product_id: int | str):
        return await self.repository.product(product_id=product_id)

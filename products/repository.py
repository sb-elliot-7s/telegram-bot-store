from dataclasses import dataclass

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from cache import RedisCache
from configs import get_configs
from protocols.products_repository_protocol import ProductRepositoryProtocol
from s3_storage import S3Storage
from schemas import ProductSchema, Brand, Category
from utils import get_specification_util


@dataclass
class ProductRepository(ProductRepositoryProtocol):
    brand_collection: AsyncIOMotorCollection = None
    category_collection: AsyncIOMotorCollection = None
    products_collection: AsyncIOMotorCollection = None
    app_redis = RedisCache(host=get_configs().redis_host, port=get_configs().redis_port)

    async def get_brands(self):
        return [Brand(**br).dict() async for br in self.brand_collection.find()]

    async def get_categories(self, brand: str):
        return [Category(**cat).dict() async for cat in self.category_collection.find({'brand': brand})]

    @app_redis.cache(custom_key='count')
    async def count_of_products(self, brand: str, category: str):
        return await self.products_collection.count_documents(filter={'brand': brand, 'category': category})

    @app_redis.cache(default_json=str)
    async def get_products(self, brand: str, category: str, page: int | None = None) -> list:
        cursor = self.products_collection.find({'brand': brand, 'category': category})
        if page:
            skip = (page - 1) * get_configs().page_size
            limit = get_configs().page_size * page
            cursor = cursor.limit(limit).skip(skip)
        s3_storage = S3Storage()
        return [
            ProductSchema(
                **pr, photo_url=await s3_storage.generate_url(pr.get('images')[0])
            ).dict(by_alias=False, exclude_none=True)
            for pr in await cursor.to_list(length=3 if page else None)
        ]

    @staticmethod
    def __convert(txt: str):
        return txt.replace('(', '\(').replace(')', '\)')

    async def search(self, title: str):
        filter_ = {'title': {'$regex': self.__convert(title), '$options': 'si'}}
        if (product := await self.products_collection.find_one(filter=filter_)) is None:
            return None
        s3_storage = S3Storage()
        return ProductSchema(
            **product, photo_url=await s3_storage.generate_url(filename=product.get('images')[0])
        ).dict(by_alias=False)

    @app_redis.cache(custom_key='specifications', is_one_product=True)
    async def get_specifications(self, product_id: str | int):
        product = ProductSchema(**await self.products_collection.find_one({'_id': ObjectId(product_id)}))
        return {'result': await get_specification_util(product_schema=product)}

    @app_redis.cache(custom_key='product', is_one_product=True)
    async def product(self, product_id: int | str):
        product = await self.products_collection.find_one({'_id': ObjectId(product_id)})
        s3_storage = S3Storage()
        return ProductSchema(**product, photo_url=await s3_storage.generate_url(filename=product.get('images')[0])) \
            .dict(exclude_none=True, by_alias=False) if product else None

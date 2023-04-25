import asyncio

import motor.motor_asyncio
import pymongo

from configs import get_configs

client = motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://{get_configs().mongo_host}:{get_configs().mongo_port}')

database = client.database

brand_collection = database.brand
category_collection = database.category

products_collection = database.products_collection
service_center_collection = database.service_centre


async def create_index():
    await products_collection \
        .create_index([('brand', pymongo.ASCENDING), ('category', pymongo.ASCENDING)])


if __name__ == '__main__':
    asyncio.run(create_index())

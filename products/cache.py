import logging
from dataclasses import dataclass, field
from typing import Callable, Any, Iterable

import orjson
from redis import asyncio as aioredis

logging.basicConfig(level=logging.DEBUG, filename='ccc.log')


@dataclass
class RedisCache:
    host: str
    port: int
    redis: aioredis.Redis = field(init=False)
    ONE_DAY = 86400
    ONE_HOUR = 3600

    def __post_init__(self):
        self.redis_cache = aioredis.from_url(f'redis://{self.host}:{self.port}')

    async def __save_to_cache_and_return_data(self, name: str, ex: int, func: Callable, default_json: Any,
                                              args: Iterable, kwargs: dict):
        data = await func(*args, **kwargs)
        await self.redis_cache.set(name=name, value=orjson.dumps(data, default=default_json), ex=ex)
        return data

    @staticmethod
    async def __prepare_key(*, is_one_product: bool = False, kwargs: dict, custom_key: str):
        if is_one_product:
            key = f'{custom_key}:{kwargs.get("product_id")}'
        else:
            st = page if (page := kwargs.get('page')) else custom_key
            key = f'{kwargs.get("brand")}:{kwargs.get("category")}:{st}'
        return key

    def cache(
            self, ex_time: int = ONE_HOUR, custom_key: str | None = None, default_json: Any = None,
            is_one_product: bool = False):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                key = await self.__prepare_key(is_one_product=is_one_product, custom_key=custom_key, kwargs=kwargs)
                data_from_cache = await self.redis_cache.get(name=key)
                if data_from_cache is None:
                    options = {
                        'name': key,
                        'ex': ex_time,
                        'func': func,
                        'default_json': default_json,
                        'args': args,
                        'kwargs': kwargs
                    }
                    return await self.__save_to_cache_and_return_data(**options)
                return orjson.loads(data_from_cache)

            return wrapper

        return decorator

    async def remove(self):
        await self.redis_cache.flushall()

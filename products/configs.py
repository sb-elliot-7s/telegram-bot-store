from functools import lru_cache

from pydantic import BaseSettings


class Configs(BaseSettings):
    page_size: int

    bucket_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    expires_in_boto3: int

    redis_host: str
    redis_port: int

    mongo_host: str
    mongo_port: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_configs() -> Configs: return Configs()

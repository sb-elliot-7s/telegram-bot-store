from functools import lru_cache

from pydantic import BaseSettings


class Configs(BaseSettings):
    token: str
    payments_token: str
    kafka_broker: str

    grpc_host: str

    phone: int
    telegram_account: str

    bot_name: str
    avito_profile_url: str

    default_city_name: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_configs() -> Configs: return Configs()

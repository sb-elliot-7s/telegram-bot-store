from datetime import datetime
from typing import Any

import orjson
from pydantic import BaseModel

from configs import get_configs
from constants import GroupID


class ShippingResponseSchema(BaseModel):
    country_code: str | None
    state: str | None
    city: str | None
    street_line1: str | None
    street_line2: str | None
    post_code: str | None


class UpdateUserSchema(BaseModel):
    id: str | int | None
    email: str | None
    phone_number: str | None

    shipping_address: ShippingResponseSchema | None


class UserSchema(UpdateUserSchema):
    is_bot: bool | None
    first_name: str | None
    last_name: str | None
    username: str | None
    fullname: str | None
    date_joined: datetime | None
    language_code: str | None

    def to_mongo_object(self):
        return {**self.dict(exclude_none=True, exclude={'id'}), '_id': self.id}


class KafkaSettingsSchema(BaseModel):
    bootstrap_servers: Any = get_configs().kafka_broker
    group_id: str = GroupID.USER_GROUP.value
    value_deserializer: Any = lambda x: orjson.loads(x)

from datetime import datetime
from typing import Any

import orjson
from pydantic import BaseModel, Field

from configs import get_configs
from constants import GroupID


class KafkaSettingsSchema(BaseModel):
    bootstrap_servers: Any = get_configs().kafka_broker
    group_id: str = GroupID.PAYMENTS_GROUP_ID.value
    value_deserializer: Any = lambda x: orjson.loads(x)


class ShippingResponseSchema(BaseModel):
    country_code: str | None
    state: str | None
    city: str | None
    street_line1: str | None
    street_line2: str | None
    post_code: str | None


class OrderInfo(BaseModel):
    name: str | None
    phone_number: str | None
    email: str | None
    shipping_address: ShippingResponseSchema | None


class SuccessfulPayment(BaseModel):
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: str
    order_info: OrderInfo | None


class FromUserSchema(BaseModel):
    id: int
    is_bot: bool
    first_name: str | None
    last_name: str | None
    username: str | None


class PaymentResponseSchema(BaseModel):
    message_id: int
    user: FromUserSchema = Field(alias='from_')
    date: datetime
    payment_date: datetime
    successful_payment: SuccessfulPayment | None

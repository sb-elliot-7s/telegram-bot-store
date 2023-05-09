from datetime import datetime
from typing import Any

import orjson.orjson
from aiogram.types import LabeledPrice, InlineKeyboardMarkup
from google._upb._message import RepeatedCompositeContainer
from pydantic import BaseModel, Field

from configs import get_configs


class User(BaseModel):
    id: int
    is_bot: bool | None
    first_name: str | None
    last_name: str | None
    fullname: str | None
    username: str | None
    language_code: str | None
    date_joined: datetime


class Brand(BaseModel):
    id: int
    value: str


class Category(BaseModel):
    id: int
    name: str
    brand: str


class Product(BaseModel):
    id: int | str
    title: str
    images: list | None
    photo_urls: list | None
    telegram_file_ids: list | None

    description: str | None
    descr_from_excel: str | None
    brand: str | None
    category: str | None

    recommend_price: str | None
    wholesale_price: float | None
    minimum_retail_price: float | None

    availability: str | None
    photo_url: str | None

    class Config:
        json_dumps = orjson.dumps
        json_loads = orjson.loads


class ProductResponseSchema(BaseModel):
    count_documents: int | None
    products: RepeatedCompositeContainer

    class Config:
        arbitrary_types_allowed = True


class PaymentSchema(BaseModel):
    chat_id: int | str | None
    title: str
    description: str
    currency: str
    prices: list[LabeledPrice]
    photo_url: str | bytes | None = None
    photo_height: int | None = None
    photo_width: int | None = None
    photo_size: int | None = None
    need_name: bool | None = None
    need_email: bool | None = None
    need_phone_number: bool | None = None
    need_shipping_address: bool | None = None
    is_flexible: bool | None = None
    payload: str
    start_parameter: str | None = None
    max_tip_amount: int | None = None,
    suggested_tip_amounts: list[int] | None = None,
    provider_data: dict | None = None,
    send_phone_number_to_provider: bool | None = None,
    send_email_to_provider: bool | None = None,
    message_thread_id: int | None = None,
    disable_notification: bool | None = None,
    protect_content: bool | None = None,
    reply_to_message_id: int | None = None,
    allow_sending_without_reply: bool | None = None,
    reply_markup: InlineKeyboardMarkup | None = None,
    provider_token: str = get_configs().payments_token

    class Config:
        arbitrary_types_allowed = True


class CallbackDataSchema(BaseModel):
    level: str | None
    brand: str | None
    category: str | None
    page: int | None


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
    from_: FromUserSchema = Field(alias='from')
    date: datetime
    successful_payment: SuccessfulPayment


class KafkaSettingsSchema(BaseModel):
    bootstrap_servers: list | str = get_configs().kafka_broker
    value_serializer: Any = lambda x: orjson.dumps(x)
    compression_type: str = 'gzip'


class ServiceCenterSchema(BaseModel):
    id: str
    name: str
    url: str | None
    phone: str | None
    region: str | None
    address: str | None
    latitude: str | None
    longitude: str | None

from dataclasses import dataclass

from aiogram.types import CallbackQuery, Message, ParseMode, InputFile
from aiogram.utils.exceptions import MessageToDeleteNotFound

from constants import Topic, Brand, KEY_INFO
from constants import WELCOME_TEXT, CONTACTS_TEXT, SELECT_BRAND_TEXT
from kafka_producer_service import KafkaService
from keyboards import create_brand_keyboard, create_categories_keyboard, \
    get_start_button_markup, create_order_price_list_buttons, create_order_price_and_info_button, \
    create_address_service_center_button
from mixins import HandlersMixin
from schemas import User
from utils import telegram_text_format, delete_message_after_sleep


@dataclass
class Handlers(HandlersMixin):

    @staticmethod
    async def start_handler(message: Message):
        user = User(
            fullname=message.from_user.full_name, date_joined=message.date,
            **message.from_user.to_python())
        await KafkaService().produce(topic=Topic.SAVE_USER.value, value=user.dict(exclude_none=True))
        await message.answer(text=WELCOME_TEXT.format(user=user.fullname), reply_markup=get_start_button_markup())

    @staticmethod
    async def contacts_handler(message: Message):
        await message.answer(
            text=telegram_text_format(CONTACTS_TEXT),
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=create_order_price_and_info_button()
        )
        await delete_message_after_sleep(message=message, sleep_time=2)

    @staticmethod
    async def catalog_handler(message: Message):
        await message.answer(text=SELECT_BRAND_TEXT, reply_markup=await create_brand_keyboard())
        await delete_message_after_sleep(is_delete=False, message=message, sleep_time=3)

    @staticmethod
    async def order_price_list_handler(message: Message):
        await message.answer(text='Какой бренд вас интересует?', reply_markup=create_order_price_list_buttons())

    @staticmethod
    async def get_key_info_handler(message: Message):
        await message.answer(
            text=KEY_INFO,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=create_address_service_center_button()
        )

    @staticmethod
    async def brands(message: Message, **kwargs):
        await message.answer(text='Выберите производителя:', reply_markup=await create_brand_keyboard())

    @staticmethod
    async def categories(callback_query: CallbackQuery, brand: str, **kwargs):
        await callback_query.message.answer(
            text='Теперь выберите категорию товара:', reply_markup=await create_categories_keyboard(brand=brand))

    @staticmethod
    async def answer_document(callback_query: CallbackQuery, brand: str):
        await callback_query.message.answer_document(
            document=InputFile(
                path_or_bytesio=f'price_lists/{brand}_price.xlsx',
                filename=f'Цены {brand.title()}.xlsx'),
        )

    async def send_order_price_list(self, callback_query: CallbackQuery, callback_data: dict):
        match callback_data.get('brand'):
            case Brand.LIFAN.value:
                await self.answer_document(callback_query=callback_query, brand=Brand.LIFAN.value)
            case Brand.LONCIN.value:
                await self.answer_document(callback_query=callback_query, brand=Brand.LONCIN.value)
        try:
            await delete_message_after_sleep(sleep_time=.1, message=callback_query.message)
        except MessageToDeleteNotFound as e:
            pass

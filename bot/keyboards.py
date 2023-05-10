from typing import Any

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.callback_data import CallbackData

from constants import MAIN_BUTTONS
from grpc_service import GRPCProductsClient

menu_callback_data = CallbackData('menu', 'level', 'brand', 'category', 'page')

product_callback_data = CallbackData('product', 'product_id', 'show_info')

pay_product_callback_data = CallbackData('pay', 'product_id')

order_price_list_callback_data = CallbackData('order_price_list', 'brand')

service_center_callback_data = CallbackData('service_center', 'brand')


def create_service_center_callback_data(brand: str):
    return service_center_callback_data.new(brand=brand)


def create_order_price_list_callback_data(brand: str):
    return order_price_list_callback_data.new(brand=brand)


def create_pay_callback_data(product_id: int):
    return pay_product_callback_data.new(product_id=product_id)


def create_product_callback_data(product_id: int, show_info: bool = False):
    return product_callback_data.new(product_id=product_id, show_info=show_info)


def create_menu_command_callback_data(level: int, brand: str | None = None, category: str | None = '0', page: int = 1):
    return menu_callback_data.new(level=level, brand=brand, category=category, page=page)


def get_start_button_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    return markup.add(*(KeyboardButton(text=text) for text in MAIN_BUTTONS))


def create_markup(row_width: int = 3, inline_keyboard: Any = None, **kwargs):
    return InlineKeyboardMarkup(row_width=row_width, inline_keyboard=inline_keyboard, **kwargs)


async def create_brand_keyboard() -> InlineKeyboardMarkup:
    level = 0
    markup = create_markup()
    brands = await GRPCProductsClient().get_brands()
    return markup.add(
        *(InlineKeyboardButton(
            text=brand.value, callback_data=create_menu_command_callback_data(level=level + 1, brand=brand.value)
        ) for brand in brands)
    )


async def create_categories_keyboard(brand: str) -> InlineKeyboardMarkup:
    level = 1
    markup = create_markup(row_width=2)
    categories = await GRPCProductsClient().get_categories(brand=brand.lower())
    buttons = (InlineKeyboardButton(
        text=cat.name,
        callback_data=create_menu_command_callback_data(
            level=level + 1, brand=brand, category=cat.name, page=1))
        for cat in categories
    )
    return markup.add(*buttons)


def create_next_buttons(level: int, brand: str | None, category: str | None, page: int):
    markup = create_markup(row_width=1)
    next_button = InlineKeyboardButton(
        text='Загрузить ещё ?',
        callback_data=create_menu_command_callback_data(level=level, brand=brand, category=category, page=page + 1)
    )
    return markup.add(next_button)


def create_pay_info_buttons(product_id: int, show_info: bool = True):
    markup = create_markup()
    return markup.add(
        InlineKeyboardButton(text='Купить', callback_data=create_pay_callback_data(product_id=product_id)),
        InlineKeyboardButton(text='Характеристики',
                             callback_data=create_product_callback_data(product_id=product_id, show_info=show_info)),
    )


def create_order_price_list_buttons():
    markup = create_markup()
    return markup.add(
        InlineKeyboardButton(text='Lifan', callback_data=create_order_price_list_callback_data(brand='lifan')),
        InlineKeyboardButton(text='Loncin', callback_data=create_order_price_list_callback_data(brand='loncin'))
    )


def create_order_price_and_info_button():
    markup = create_markup()
    return markup.add(
        InlineKeyboardButton(text='Запросить прайс', callback_data='price_list'),
        InlineKeyboardButton(text='Информация', callback_data='key_info')
    )


def choose_brands_service_center():
    markup = create_markup()
    return markup.add(
        InlineKeyboardButton(text='Lifan', callback_data=create_service_center_callback_data('lifan')),
        InlineKeyboardButton(text='Loncin', callback_data=create_service_center_callback_data('loncin'))
    )


def create_address_service_center_button():
    markup = create_markup()
    return markup.add(
        InlineKeyboardButton(text='Сервисные центры', callback_data='service_center')
    )


def loncin_service_center_keyboard():
    markup = create_markup(row_width=1)
    return markup.add(
        InlineKeyboardButton(text='Все сервисные центры', callback_data='show_service_center'),
        InlineKeyboardButton(text='Ближайший к вашему городу', callback_data='show_your_city_service_center')
    )

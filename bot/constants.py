from enum import Enum

from aiogram.utils.markdown import bold, text

from configs import get_configs
from utils import telegram_text_format


class Button(str, Enum):
    START = 'start'
    CONTACTS = 'Контакты'
    CATALOG = 'Каталог'
    ORDER_PRICE_LIST = 'Заказать прайс'
    HELP = 'help'


class Brand(str, Enum):
    LONCIN = 'loncin'
    LIFAN = 'lifan'


class Category(str, Enum):
    GENERATORY = 'generator'
    ENGINE = 'engine'
    MOTOPOMPY = 'motompompy'
    MOTORY_LODOCHNYE = 'motory_lodochnye'


def convert_category(category: str):
    return {
        'генераторы': 'generator',
        'моторы лодочные': 'motory_lodochnye',
        'мотопомпы': 'motopompy',
        'двигатели': 'engine'
    }.get(category.lower())


MAIN_BUTTONS = (Button.CONTACTS.value, Button.CATALOG.value)
SELECT_BRAND_TEXT = 'Выберите производителя'

WELCOME_TEXT = '{user} добро пожаловать в интернет магазин'

HELP_TEXT = f'Для поиска определённого товара - напишите @{get_configs().bot_name} поиск и название товара. ' \
            f'(Например @{get_configs().bot_name} поиск loncin lc152f )\n\n' \
            'Чтобы показать список товаров бренда в определенной категории - ' \
            f'напишите @{get_configs().bot_name} cписок ' \
            '[ lifan или loncin ] [ двигатели | генераторы | мотопомпы | моторы лодочные ]\n\n'

CONTACTS_TEXT = f'Связь:  \n\n' \
                f'Telegram: @{get_configs().telegram_account}\n\n' \
                f'Телефон: +{get_configs().phone}\n\n' \
                f'Профиль на авито: {get_configs().avito_profile_url}'

KEY_INFO = text(
    f"{bold('Гарантия: ')}\n"
    f"{telegram_text_format('Lifan - 1 год со дня продажи')}\n"
    f"{telegram_text_format('Loncin - гарантийный сертификат на 2 года')}\n\n",
    text(bold('Полный комплект документов и инструкция на русском языке\n\n')),
    text(bold('Строгий контроль качества перед продажей\n\n')),
    text(bold('Клиентская поддержка на всех этапах')),
    sep=''
)


class Topic(str, Enum):
    SAVE_USER = 'save_user'
    UPDATE_USER = 'update_user'
    SAVE_PAYMENTS_DATA = 'save_payments_data'

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineQuery, CallbackQuery, BotCommand, ContentType, InputFile
from aiogram.utils.exceptions import MessageToDeleteNotFound

from configs import get_configs
from constants import Button, HELP_TEXT
from grpc_service import GRPCProductsClient
from handlers import Handlers
from keyboards import menu_callback_data, product_callback_data, \
    pay_product_callback_data, order_price_list_callback_data, service_center_callback_data
from payments_handlers import PaymentsHandler
from schemas import CallbackDataSchema
from service_center_handler import ServiceCenterHandler
from shipping_handlers import ShippingHandlers
from utils import delete_message_after_sleep

bot = Bot(token=get_configs().token)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class ServiceCenterStates(StatesGroup):
    city_name = State()


@dp.inline_handler(Text(contains='список', ignore_case=True), state='*')
async def inline_products(inline_query: InlineQuery, state: FSMContext):
    await state.finish()
    await PaymentsHandler(grcp_service_client=GRPCProductsClient()) \
        .brands_and_categories_inline(inline_query=inline_query)


@dp.inline_handler(Text(contains='поиск', ignore_case=True), state='*')
async def search_product(inline_query: InlineQuery, state: FSMContext):
    await state.finish()
    await PaymentsHandler(grcp_service_client=GRPCProductsClient()) \
        .search_inline(inline_query=inline_query)


@dp.message_handler(Command(Button.START.value))
async def start_command(message: types.Message):
    await Handlers().start_handler(message=message)


@dp.message_handler(Command(Button.HELP.value), state='*')
async def help_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=HELP_TEXT)


@dp.message_handler(Text(equals=Button.CONTACTS.value), state='*')
async def contacts_command(message: types.Message, state: FSMContext):
    await state.finish()
    await Handlers().contacts_handler(message=message)


@dp.message_handler(Text(equals=Button.CATALOG.value), state='*')
async def catalog_command(message: types.Message, state: FSMContext):
    await state.finish()
    await Handlers().catalog_handler(message=message)


@dp.message_handler(Text(equals=Button.ORDER_PRICE_LIST.value))
async def order_price_list_command(message: types.Message):
    await Handlers().order_price_list_handler(message=message)


@dp.callback_query_handler(menu_callback_data.filter())
async def root(callback_query: CallbackQuery, callback_data: dict):
    schema = CallbackDataSchema(**callback_data)
    levels = {
        '1': Handlers().categories,
        '2': PaymentsHandler(grcp_service_client=GRPCProductsClient()).products
    }
    await levels[schema.level](callback_query=callback_query, **schema.dict(exclude={'level'}))
    try:
        await callback_query.message.delete()
    except MessageToDeleteNotFound:
        pass


@dp.pre_checkout_query_handler(lambda x: True)
async def process_checkout_query_command(pre_checkout_query: types.PreCheckoutQuery):
    await PaymentsHandler(grcp_service_client=GRPCProductsClient()) \
        .process_pre_checkout_query(bot=bot, pre_checkout_query=pre_checkout_query)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment_command(message: types.Message):
    await PaymentsHandler(grcp_service_client=GRPCProductsClient()) \
        .process_successful_payment(message=message)


@dp.shipping_query_handler(lambda query: True)
async def process_shipping_query_command(shipping_query: types.ShippingQuery):
    await ShippingHandlers().process_shipping_query(bot=bot, shipping_query=shipping_query)


@dp.callback_query_handler(product_callback_data.filter())
async def specifications(callback_query: CallbackQuery, callback_data: dict):
    await PaymentsHandler(grcp_service_client=GRPCProductsClient()) \
        .specifications(callback_query=callback_query, product_id=callback_data.get('product_id'))


@dp.callback_query_handler(pay_product_callback_data.filter())
async def pay(callback_query: CallbackQuery, callback_data: dict):
    await PaymentsHandler(grcp_service_client=GRPCProductsClient()) \
        .pay(bot=bot, callback_query=callback_query, product_id=callback_data.get('product_id'))


@dp.callback_query_handler(order_price_list_callback_data.filter())
async def order_price_list(callback_query: CallbackQuery, callback_data: dict):
    await Handlers().send_order_price_list(callback_data=callback_data, callback_query=callback_query)


@dp.callback_query_handler(Text(equals='price_list'))
async def get_price_list(callback_query: CallbackQuery):
    await Handlers().order_price_list_handler(callback_query.message)


@dp.callback_query_handler(Text(equals='key_info'))
async def get_key_info(callback_query: CallbackQuery):
    await Handlers().get_key_info_handler(message=callback_query.message)


@dp.callback_query_handler(Text(equals='service_center'))
async def choose_service_center_brands(callback_query: CallbackQuery):
    await ServiceCenterHandler(grpc_service=GRPCProductsClient()).brands_service_center(message=callback_query.message)


@dp.callback_query_handler(Text(equals='show_service_center'))
async def show_list_address_service_center(callback_query: CallbackQuery):
    await callback_query.message.answer_document(
        document=InputFile(
            path_or_bytesio='service_center_loncin.numbers', filename='Сервисные центры Loncin.numbers')
    )


@dp.callback_query_handler(service_center_callback_data.filter())
async def check_service_center(callback_query: CallbackQuery, callback_data: dict):
    await ServiceCenterHandler(grpc_service=GRPCProductsClient()) \
        .show_brand_service_center(callback_query=callback_query, callback_data=callback_data)


@dp.callback_query_handler(Text(equals='show_your_city_service_center'))
async def write_your_city(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(text='Напишите ваш город: ')
    await state.set_state(ServiceCenterStates.city_name.state)
    await delete_message_after_sleep(message=callback_query.message, sleep_time=.2)


@dp.message_handler(state=ServiceCenterStates.city_name)
async def city_service_center_handler(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.delete()
        await state.finish()
        answ = await message.answer(text='ок')
        return await answ.delete()
    res = await ServiceCenterHandler(grpc_service=GRPCProductsClient()) \
        .get_service_center(city=message.text, message=message, state=state,
                            my_state=ServiceCenterStates.city_name.state)
    if res:
        await state.finish()


async def set_commands(dp):
    await dp.bot.set_my_commands(commands=[BotCommand(command='help', description='Вызов справки по коммандам')])


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, on_startup=set_commands)

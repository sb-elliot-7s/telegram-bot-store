from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from configs import get_configs
from constants import Brand
from grpc_service import GRPCProductsClient
from keyboards import choose_brands_service_center, loncin_service_center_keyboard
from utils import delete_message_after_sleep


@dataclass
class ServiceCenterHandler:
    grpc_service: GRPCProductsClient

    async def get_service_center(self, message: Message, city: str, state: FSMContext, my_state):
        if len(city) > 2:
            addresses = await self.grpc_service.get_service_center(city=city)
            for address in addresses:
                await message.answer_location(latitude=address.latitude, longitude=address.longitude)
                await message.answer(text=address.address)
            return True
        else:
            await message.answer(text='Должно быть минимум три буквы. Повторите ваш запрос или напишите отмена')
            await state.set_state(my_state)
            return False

    @staticmethod
    async def brands_service_center(message: Message):
        await message.answer(text='Выберите производителя:', reply_markup=choose_brands_service_center())

    async def show_brand_service_center(self, callback_query: CallbackQuery, callback_data: dict):
        match callback_data.get('brand'):
            case Brand.LIFAN.value:
                results = await self.grpc_service.get_service_center(city=get_configs().default_city_name)
                if address := results[0]:
                    await callback_query.message.answer_location(latitude=address.latitude, longitude=address.longitude)
                    await callback_query.message.answer(text=address.address)
            case Brand.LONCIN.value:
                await callback_query.message.answer(text='Показать: ', reply_markup=loncin_service_center_keyboard())

        await delete_message_after_sleep(message=callback_query.message, sleep_time=1)

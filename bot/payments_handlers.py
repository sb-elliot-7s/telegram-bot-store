import asyncio
import datetime
import uuid
from dataclasses import dataclass

import math
from aiogram import Bot
from aiogram.types import CallbackQuery, InputMediaPhoto, ParseMode, PreCheckoutQuery, InputInvoiceMessageContent, \
    InlineQuery, Message
from aiogram.utils.markdown import bold, text

from constants import Topic
from grpc_service import GRPCProductsClient
from kafka_producer_service import KafkaService
from keyboards import create_pay_info_buttons, create_next_buttons
from mixins import HandlersMixin
from schemas import PaymentResponseSchema
from utils import telegram_text_format, delete_message_after_sleep


@dataclass
class PaymentsHandler(HandlersMixin):
    grcp_service_client: GRPCProductsClient

    @staticmethod
    async def specifications(callback_query: CallbackQuery, product_id: str | int):
        result = await GRPCProductsClient().get_specifications(product_id=product_id)
        await callback_query.message.reply(text=result)

    async def pay(self, bot: Bot, callback_query: CallbackQuery, product_id: str):
        product = await GRPCProductsClient().get_product(product_id=product_id)
        decription = product.description[:255] if product.description \
            else product.descr_from_excel[:255] or 'Описания пока что нет'
        prices = [self.create_labeled_price(label=product.title, amount=int(
            product.minimum_retail_price or product.recommend_price) * 100)]
        await bot.send_invoice(**self.create_payment_data(
            chat_id=callback_query.message.chat.id,
            title=product.title[:32],
            description=decription,
            prices=prices,
            payload=f'{product.id}:payload',
            photo_url=product.photo_url,
        ))

    @staticmethod
    async def products(callback_query: CallbackQuery, category: str, brand: str, page: int):
        result = await GRPCProductsClient().get_products(brand=brand, category=category, page=page)
        for product in result.products:
            title = product.title
            price = int(product.minimum_retail_price or product.recommend_price)
            description_condition = product.description or product.descr_from_excel or 'Описания пока что нет'
            inp_media_photo = {
                'media': product.telegram_file_ids[0],
                'caption': text(
                    bold(title),
                    text(price, '₽', '\n'),
                    text(telegram_text_format(description_condition)),
                    sep='\n')[:1000],
                'parse_mode': ParseMode.MARKDOWN_V2
            }
            media = [
                InputMediaPhoto(**inp_media_photo), *[InputMediaPhoto(img) for img in product.telegram_file_ids[1:4]]
            ]
            await callback_query.message.answer_media_group(media=media)
            await callback_query.message.answer(
                text='Действия с товаром: ', reply_markup=create_pay_info_buttons(product_id=product.id))
        markup = create_next_buttons(level=2, brand=brand, category=category, page=page)
        total_cnt_pages = math.ceil(result.count_documents / 3)
        if total_cnt_pages == 0:
            msg = await callback_query.message.answer(text='В данный момент нет товаров в этой категории')
            return await delete_message_after_sleep(message=msg, sleep_time=2)
        if page != total_cnt_pages:
            await callback_query.message.answer(text=f'Страница {page} из {total_cnt_pages}', reply_markup=markup)

    @staticmethod
    async def process_pre_checkout_query(bot: Bot, pre_checkout_query: PreCheckoutQuery):
        product_id = pre_checkout_query.invoice_payload.split(':')[0]
        product = await GRPCProductsClient().get_product(product_id=product_id)
        if product.availability:
            return await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)
        return await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=False,
                                                   error_message='Товара нет в наличии')

    @staticmethod
    async def process_successful_payment(message: Message):
        schema = PaymentResponseSchema(**message.to_python())
        await KafkaService().produce(
            topic=Topic.UPDATE_USER.value,
            value={
                'shipping_address': schema.successful_payment.order_info.shipping_address.dict(exclude_none=True),
                'email': schema.successful_payment.order_info.email,
                'phone_number': schema.successful_payment.order_info.phone_number,
                'id': schema.from_.id
            }
        )
        await KafkaService().produce(topic=Topic.SAVE_PAYMENTS_DATA.value,
                                     value={**schema.dict(), 'payment_date': datetime.datetime.now()})
        msg = await message.answer(text='Спасибо за вашу покупку')
        await delete_message_after_sleep(message=msg, sleep_time=4)

    """INLINE QUERIES"""

    async def brands_and_categories_inline(self, inline_query: InlineQuery):
        queries = inline_query.query.split()
        offset = int(inline_query.offset) if inline_query.offset else 0
        count = len(queries)
        if count > 2:
            brand, *category = queries[1:]
            category = ' '.join(category)
            products = await GRPCProductsClient().get_products(brand=brand.lower(), category=category.lower())
            if products and len(products.products) > 0:
                results = [
                    self.get_inline_query_result_article(
                        id_=str(uuid.uuid4()),
                        title=product.title,
                        description=f"""{int(product.minimum_retail_price
                                             or product.recommend_price or product.wholesale_price or 100)} ₽""",
                        thumb_url=product.photo_url,
                        input_message_content=InputInvoiceMessageContent(
                            **self.create_payment_data(
                                title=product.title[:32],
                                description=product.description[:255] or product.descr_from_excel[:255],
                                payload=f'{product.id}:payload',
                                prices=[self.create_labeled_price(
                                    label=product.title[:32],
                                    amount=int(
                                        product.minimum_retail_price
                                        or product.recommend_price or product.wholesale_price or 100
                                    ) * 100
                                )],
                                photo_url=product.photo_url
                            )
                        )
                    ) for product in self.get_products_results(offset=offset, products=products.products)
                ]
                await self.return_inline_query_answer(
                    inline_query=inline_query, results=results, offset=offset, is_personal=True)

    async def search_inline(self, inline_query: InlineQuery):
        queries = inline_query.query.split()
        await asyncio.sleep(.75)
        if len(queries) > 1:
            title = ' '.join(queries[1:])
            product = await GRPCProductsClient().search(product_name=title)
            if product is not None:
                price = int(product.minimum_retail_price or
                            product.recommend_price or product.wholesale_price or 100)
                await self.inline_query_answer_with_invoice_message_content(
                    inline_query=inline_query,
                    id_=str(uuid.uuid4()),
                    title=product.title,
                    description=f'{price} ₽',
                    photo_url=product.photo_url,
                    payload=f'{product.id}:payload',
                    prices=[self.create_labeled_price(label=product.title, amount=price * 100)],
                    is_personal=True
                )

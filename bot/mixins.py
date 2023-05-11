from aiogram.types import LabeledPrice, InlineKeyboardMarkup, InputMessageContent, InlineQueryResultArticle, \
    InlineQuery, InputInvoiceMessageContent

from schemas import PaymentSchema, Product


class HandlersMixin:
    @staticmethod
    def create_payment_data(
            *,
            chat_id: int | None = None,
            title: str,
            description: str,
            payload: str,
            currency: str = 'rub',
            prices: list[LabeledPrice],
            max_tip_amount: int | None = None,
            suggested_tip_amounts: list[int] | None = None,
            start_parameter: str | None = None,
            provider_data: dict | None = None,
            photo_url: str | None | bytes = None,
            photo_size: int | None = None,
            photo_width: int | None = 1024,
            photo_height: int | None = 1024,
            need_name: bool | None = True,
            need_phone_number: bool | None = True,
            need_email: bool | None = True,
            need_shipping_address: bool | None = True,
            send_phone_number_to_provider: bool | None = None,
            send_email_to_provider: bool | None = None,
            is_flexible: bool | None = None,
            message_thread_id: int | None = None,
            disable_notification: bool | None = None,
            protect_content: bool | None = None,
            reply_to_message_id: int | None = None,
            allow_sending_without_reply: bool | None = None,
            reply_markup: InlineKeyboardMarkup | None = None

    ) -> dict:
        return PaymentSchema(
            chat_id=chat_id, title=title, description=description, payload=payload,
            currency=currency, prices=prices, max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts, start_parameter=start_parameter, provider_data=provider_data,
            photo_url=photo_url, photo_size=photo_size, photo_width=photo_width, photo_height=photo_height,
            need_name=need_name, need_email=need_email, need_phone_number=need_phone_number,
            need_shipping_address=need_shipping_address, send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider, is_flexible=is_flexible, message_thread_id=message_thread_id,
            disable_notification=disable_notification, protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup
        ).dict(exclude_none=True)

    @staticmethod
    def get_inline_query_result_article(
            *, id_: str | int, title: str, thumb_url: str, thumb_width: int = 900, thumb_height: int = 900,
            description: str, input_message_content: InputMessageContent
    ):
        return InlineQueryResultArticle(
            id=id_,
            title=title,
            thumb_url=thumb_url,
            thumb_width=thumb_width,
            thumb_height=thumb_height,
            description=description,
            input_message_content=input_message_content
        )

    async def inline_query_answer_with_invoice_message_content(
            self, *, inline_query: InlineQuery,
            id_: int | str, title: str, description: str,
            thumb_width: int = 900, thumb_height: int = 900, photo_url: str,
            is_personal: bool = True, payload: str, prices: list[LabeledPrice],
    ):
        await inline_query.answer(
            results=[
                self.get_inline_query_result_article(
                    id_=id_,
                    title=title,
                    description=description,
                    thumb_width=thumb_width,
                    thumb_height=thumb_height,
                    thumb_url=photo_url,
                    input_message_content=InputInvoiceMessageContent(
                        **self.create_payment_data(
                            chat_id=None, title=title, description=description, payload=payload, prices=prices,
                            photo_url=photo_url,
                        )
                    )
                )
            ],
            is_personal=is_personal
        )

    @staticmethod
    def get_products_results(offset: int, size: int = 50, products: list = None) -> list[Product]:
        count_of_products = len(products)
        if offset >= count_of_products:
            return []
        elif offset + size >= count_of_products:
            return list(products[offset:count_of_products + 1])
        else:
            return list(products[offset: offset + size])

    @staticmethod
    def create_labeled_price(label: str, amount: int):
        return LabeledPrice(label=label, amount=amount)

    @staticmethod
    async def return_inline_query_answer(
            inline_query: InlineQuery, results: list, offset: int, is_personal: bool = True):
        if len(results) < 50:
            await inline_query.answer(results=results, is_personal=is_personal)
        else:
            await inline_query.answer(results=results, is_personal=is_personal, next_offset=str(offset + 50))

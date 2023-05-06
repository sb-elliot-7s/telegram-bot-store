import asyncio

from aiogram.types import Message


def telegram_text_format(text: str):
    return text. \
        replace('_', '\\_'). \
        replace('*', '\\*'). \
        replace('[', '\\['). \
        replace(']', '\\]'). \
        replace('(', '\\('). \
        replace(')', '\\)'). \
        replace('~', '\\~'). \
        replace('`', '\\`'). \
        replace('>', '\\>'). \
        replace('#', '\\#'). \
        replace('+', '\\+'). \
        replace('-', '\\-'). \
        replace('=', '\\='). \
        replace('|', '\\|'). \
        replace('{', '\\{'). \
        replace('}', '\\}'). \
        replace('.', '\\.'). \
        replace('!', '\\!')


async def delete_message_after_sleep(*, is_delete: bool = True, message: Message, sleep_time: float):
    if is_delete:
        await asyncio.sleep(sleep_time)
        await message.delete()

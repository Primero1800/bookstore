import asyncio

import telegram
from django.conf import settings



async def send_telegram_message(message):
    """
    Асинхронная функция для отправки сообщения в ТГ.
    """
    try:
        bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
        chat_id = settings.TELEGRAM_CHAT_ID
        await bot.send_message(chat_id=chat_id, text=message)
        return 200
    except Exception as ex:
        await asyncio.sleep(0)
        return ex


def send_message_to_bot(instance, **kwargs):
    if settings.TELEGRAM_SEND_NOTIFICATIONS:
        asyncio.run(send_telegram_message(message=instance))
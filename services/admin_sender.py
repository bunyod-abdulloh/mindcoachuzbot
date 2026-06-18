import asyncio
import logging

from aiogram.utils.exceptions import RetryAfter, BotBlocked, ChatNotFound

from loader import bot

# Adminga yuboriladigan xabarlar navbati
admin_queue: asyncio.Queue = asyncio.Queue()


async def admin_sender_worker():
    """
    Bitta worker — adminga xabarlarni ketma-ket (parallel emas) yuboradi.
    Shu tufayli webhook'dagi burst yo'qoladi va Telegram 429 bermaydi.
    """
    while True:
        chat_id, text, kwargs = await admin_queue.get()
        try:
            while True:
                try:
                    await bot.send_message(chat_id=chat_id, text=text, **kwargs)
                    break
                except RetryAfter as e:
                    # Telegram o'zi qancha kutishni aytadi
                    await asyncio.sleep(e.timeout)
                except (BotBlocked, ChatNotFound) as e:
                    logging.warning(f"Adminga yuborib bo'lmadi: {e}")
                    break
        except Exception as e:
            logging.exception(e)
        finally:
            admin_queue.task_done()
            await asyncio.sleep(0.1)  # xabarlar orasida bo'shliq


async def send_to_admin(chat_id: int, text: str, **kwargs):
    """Handler'lardan chaqiriladigan qulay funksiya — faqat navbatga qo'yadi."""
    await admin_queue.put((chat_id, text, kwargs))
import asyncio
import logging

from aiogram.utils.exceptions import RetryAfter, BotBlocked, ChatNotFound, UserDeactivated

from loader import bot

admin_queue: asyncio.Queue = asyncio.Queue()
_worker_started = False


async def admin_sender_worker():
    global _worker_started
    _worker_started = True
    logging.warning("✅ admin_sender_worker ISHGA TUSHDI")
    while True:
        chat_id, text, kwargs = await admin_queue.get()
        try:
            while True:
                try:
                    await bot.send_message(chat_id=chat_id, text=text, **kwargs)
                    logging.warning(f"✅ Adminga yuborildi: {chat_id}")
                    break
                except RetryAfter as e:
                    logging.warning(f"⏳ RetryAfter {e.timeout}s")
                    await asyncio.sleep(e.timeout)
                except (BotBlocked, ChatNotFound, UserDeactivated) as e:
                    logging.warning(f"❌ Adminga yuborilmadi: {e}")
                    break
        except Exception as e:
            logging.exception(f"❌ admin_sender xatosi: {e}")
        finally:
            admin_queue.task_done()
            await asyncio.sleep(0.1)


async def send_to_admin(chat_id, text, **kwargs):
    if not _worker_started:
        logging.error("⚠️ Worker ishga tushmagan! Xabar navbatda qotib qoladi.")
    await admin_queue.put((chat_id, text, kwargs))
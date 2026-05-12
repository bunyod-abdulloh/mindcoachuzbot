from aiogram import Dispatcher

from data.config import ADMINS
from services.error_service import notify_exception_to_admin


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(ADMINS[0], "Bot ishga tushdi")

    except Exception as err:
        await notify_exception_to_admin(err=err)

from threading import Thread
from aiogram import executor
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


# --- Aiogram startup ---
async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    await db.create()
    await db.create_tables()

# --- Main ---
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)

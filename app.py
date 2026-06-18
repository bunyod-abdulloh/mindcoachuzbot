import asyncio

import middlewares, filters, handlers

from aiogram import executor

from data.config import WEB_APP_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from loader import dp, bot, db
from services.admin_sender import admin_sender_worker
from utils.notify_admins import on_startup_notify

WEBHOOK_URL = f"{WEB_APP_URL}{WEBHOOK_PATH}"


async def on_startup(dispatcher):
    asyncio.create_task(admin_sender_worker())

    try:
        await on_startup_notify(dispatcher)
        print("✅ Notify done")
    except Exception as e:
        print(f"❌ Notify error: {e}")

    try:
        await db.create()
        await db.create_tables()
        print("✅ DB ready")
    except Exception as e:
        print(f"❌ DB error: {e}")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(WEBHOOK_URL)
        print(f"✅ Webhook set: {WEBHOOK_URL}")
    except Exception as e:
        print(f"❌ Webhook error: {e}")


async def on_shutdown(dispatcher):
    try:
        await bot.delete_webhook()
    finally:
        await bot.session.close()


if __name__ == "__main__":
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

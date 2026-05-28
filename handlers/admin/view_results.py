from aiogram import types

from handlers.private.portret import handle_portret_main
from keyboards.inline.callback_data import user_select_cb
from loader import dp


@dp.callback_query_handler(user_select_cb.filter(), state="*")
async def select_user(call: types.CallbackQuery, callback_data: dict):
    telegram_id = int(callback_data["id"])
    page = int(callback_data["page"])

    await call.answer()
    await handle_portret_main(
        call, {
            "action": "portrait",
            "lang": "uz",
            "page": page,
            "tg_id": telegram_id
        },
        True
    )

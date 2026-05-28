from aiogram import types

from keyboards.inline.base import back_ikb
from keyboards.inline.callback_data import appointment_cb
from loader import dp
from locales.core import APPOINTMENT_TEXT


@dp.callback_query_handler(appointment_cb.filter(action="appointment"))
async def happointment_main(call: types.CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")

    await call.message.edit_text(
        text=APPOINTMENT_TEXT[lang],
        reply_markup=back_ikb(lang=lang)
    )

from aiogram import types

from keyboards.inline.base import back_ikb
from keyboards.inline.callback_data import lessons_cb
from loader import dp
from locales.core import LESSONS_TEXT


@dp.callback_query_handler(lessons_cb.filter(action="lessons"))
async def hlessons_main(call: types.CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")

    await call.message.edit_text(
        text=LESSONS_TEXT[lang],
        reply_markup=back_ikb(
            lang=lang,
        ), disable_web_page_preview=True
    )

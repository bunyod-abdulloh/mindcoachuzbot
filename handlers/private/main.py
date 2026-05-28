from aiogram import types

from keyboards.inline.base import main_ikb
from keyboards.inline.callback_data import language_cb
from loader import dp, udb
from locales.core import WELCOME_TEXT
from utils.set_bot_commands import set_user_commands


@dp.callback_query_handler(language_cb.filter(action="language"))
async def handle_main(event: types.CallbackQuery | types.Message, callback_data: dict):
    lang = callback_data.get("value")
    user_id = event.from_user.id

    text = WELCOME_TEXT[lang].format(
        name=event.from_user.full_name,
    )

    reply_markup = main_ikb(lang=lang)

    await set_user_commands(user_id, lang)
    await udb.set_language(lang, int(user_id))

    if isinstance(event, types.Message):
        await event.answer(
            text=text,
            reply_markup=reply_markup
        )
    else:
        await event.message.edit_text(
            text=text,
            reply_markup=reply_markup
        )

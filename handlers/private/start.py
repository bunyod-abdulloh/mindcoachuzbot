from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from handlers.private.main import handle_main
from keyboards.inline.base import language_ikb
from keyboards.inline.base import main_ikb
from keyboards.inline.callback_data import back_cb
from loader import dp, udb
from locales.core import CHOOSE_LANGUAGE


@dp.message_handler(CommandStart(), state="*")
async def handle_start(message: types.Message, state: FSMContext):
    await state.finish()

    telegram_id = int(message.from_user.id)

    user = await udb.check_user(telegram_id)

    if user:
        lang = await udb.get_language(telegram_id)

        await handle_main(message, {
            "action": "language",
            "value": lang
        })
        return
    else:
        await udb.add_user(telegram_id)
        await message.answer(
            text=CHOOSE_LANGUAGE,
            reply_markup=language_ikb()
        )


@dp.message_handler(commands=['lang'], state="*")
async def handle_lang(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text=CHOOSE_LANGUAGE,
        reply_markup=language_ikb()
    )


@dp.callback_query_handler(back_cb.filter(page="main"))
async def back_main_handler(call: types.CallbackQuery, callback_data: dict):
    lang = callback_data["lang"]

    text = "Главное меню" if lang == "ru" else "Asosiy menyu"

    await call.message.edit_text(
        text=text,
        reply_markup=main_ikb(lang))

    await call.answer()

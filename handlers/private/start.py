from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from handlers.private.ru_main import handle_ru_main
from handlers.private.uz_main import handle_uz_main
from keyboards.default.uz_user import language_keyboard
from loader import dp, udb
from locales.ru_locale import RU_TEXTS
from locales.uz_locale import UZ_TEXTS


@dp.message_handler(CommandStart(), state="*")
async def handle_start(message: types.Message, state: FSMContext):
    await state.finish()

    telegram_id = int(message.from_user.id)

    user = await udb.check_user(telegram_id)

    if user:
        lang = await udb.get_language(telegram_id)

        if lang == "ru":
            await handle_ru_main(message, state)
        else:
            await handle_uz_main(message, state)
        return
    else:
        await udb.add_user(telegram_id)
        await message.answer(
            text=UZ_TEXTS["choose_language"],
            reply_markup=language_keyboard()
        )


@dp.message_handler(commands=['lang'], state="*")
async def handle_lang(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text=UZ_TEXTS["choose_language"],
        reply_markup=language_keyboard()
    )


@dp.message_handler(commands=["cancel"], state="*")
async def handle_cancel_state(message: types.Message, state: FSMContext):
    await state.finish()

    lang = await udb.get_language(int(message.from_user.id))

    if lang == "ru":
        text = RU_TEXTS['cancel_state']
    else:
        text = UZ_TEXTS['cancel_state']

    await message.answer(text=text)

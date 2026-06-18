import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.inline.admin import admin_support_ikb
from keyboards.inline.base import back_ikb
from keyboards.inline.callback_data import user_support_cb
from loader import dp, bot, appdb
from locales.core import USER_SUPPORT


@dp.callback_query_handler(user_support_cb.filter(), state="*")
async def h_support_main(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await state.finish()

    lang = callback_data.get("lang", None)

    await call.message.edit_text(
        text=USER_SUPPORT[lang]['alert'],
        reply_markup=back_ikb(
            lang=lang
        )
    )
    await state.set_state("user_support")


@dp.message_handler(state="user_support", content_types=['text'])
async def h_support_process(message: types.Message, state: FSMContext):
    text = message.text
    telegram_id = int(message.from_user.id)

    athlete = await appdb.check_athlete(
        telegram_id=telegram_id
    )

    result_text = str()

    if athlete:
        user = await appdb.get_athlete_full(telegram_id=telegram_id)

        user_data = (
            f"Ism sharif: {user['full_name']}\n"
            f"Tel raqam: {user['phonr_number']}\n"
            f"Sport turi: {user['sport_type']}\n"
            f"Tajriba: {user['sport_years']}\n"
            f"Qiziqishlar: {user['hobbies']}\n\n"
        )

        result_text = user_data + text

    elif not athlete:
        result_text = text

    await message.answer(
        text=USER_SUPPORT['success']
    )

    await asyncio.sleep(1)

    await bot.send_message(
        chat_id=ADMINS[1],
        text=f"Foydalanuvchidan xabar qabul qilindi!\n\n"
             f"{result_text}",
        reply_markup=admin_support_ikb(
            telegram_id=telegram_id
        )
    )

    await state.finish()

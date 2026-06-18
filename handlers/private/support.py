from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.inline.admin import admin_support_ikb
from keyboards.inline.base import back_ikb
from keyboards.inline.callback_data import user_support_cb
from loader import dp, appdb, udb
from locales.core import USER_SUPPORT
from services.admin_sender import send_to_admin


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
    text = f"Xabar matni:\n\n{message.text}"
    telegram_id = int(message.from_user.id)

    athlete = await appdb.check_athlete(telegram_id=telegram_id)

    if athlete:
        user = await appdb.get_athlete_full(telegram_id=telegram_id)
        result_text = (
            f"Ism sharif: {user['full_name']}\n"
            f"Tel raqam: {user['phone_number']}\n"  # 'phonr_number' xatosi tuzatildi
            f"Sport turi: {user['sport_type']}\n"
            f"Tajriba: {user['sport_years']}\n"
            f"Qiziqishlar: {user['hobbies']}\n\n"
                      ) + text
    else:
        result_text = text

    lang = await udb.get_language(
        telegram_id=telegram_id
    )
    # Foydalanuvchiga darrov javob
    await message.answer(text=USER_SUPPORT[lang]['success'])

    # sleep yo'q, to'g'ridan-to'g'ri send yo'q — faqat navbatga qo'yamiz
    await send_to_admin(
        chat_id=ADMINS[1],
        text=f"Foydalanuvchidan xabar qabul qilindi!\n\n{result_text}",
        reply_markup=admin_support_ikb(telegram_id=telegram_id),
    )

    await state.finish()

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp
from locales.ru_locale import RU_TEXTS


@dp.message_handler(F.text == RU_TEXTS["menu_appointment"], state="*")
async def handle_ru_appointment_main(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text="Для записи на приём свяжитесь с психологом.\n\n"
             "Номер телефона:\n\n"
             "Telegram: https://t.me/psixologAbdullayev"
    )

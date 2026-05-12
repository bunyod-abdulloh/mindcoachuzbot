from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp
from locales.ru_locale import RU_TEXTS


@dp.message_handler(F.text == RU_TEXTS["menu_lessons"], state="*")
async def handle_ru_lessons_main(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text=RU_TEXTS["menu_lessons"]
    )

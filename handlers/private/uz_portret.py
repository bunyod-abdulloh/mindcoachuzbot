from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp
from locales.uz_locale import UZ_TEXTS


@dp.message_handler(F.text == UZ_TEXTS['menu_portret'], state="*")
async def handle_uz_portret_main(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text=message.text
    )

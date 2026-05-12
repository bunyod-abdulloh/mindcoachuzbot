from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.default.uz_user import uz_main_dkb
from loader import dp, udb
from locales.uz_locale import UZ_TEXTS
from utils.set_bot_commands import set_user_commands


@dp.message_handler(F.text == "🇺🇿 O'zbekcha", state="*")
async def handle_uz_main(message: types.Message, state: FSMContext):
    await state.finish()
    await set_user_commands(message.bot, message.from_user.id, "uz")
    await message.answer(
        text=UZ_TEXTS["welcome"].format(
            name=message.from_user.full_name
        ) + f"\n\n{UZ_TEXTS['help_text']}",
        reply_markup=uz_main_dkb()
    )
    await udb.set_language("uz", int(message.from_user.id))

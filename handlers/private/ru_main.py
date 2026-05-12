from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.default.ru_user import ru_main_dkb
from loader import dp, udb
from locales.ru_locale import RU_TEXTS
from utils.set_bot_commands import set_user_commands


@dp.message_handler(F.text == "🇷🇺 Русский", state="*")
async def handle_ru_main(message: types.Message, state: FSMContext):
    await state.finish()
    await set_user_commands(message.bot, message.from_user.id, "ru")
    await message.answer(
        text=RU_TEXTS["welcome"].format(
            name=message.from_user.full_name
        ) + f"\n\n{RU_TEXTS['help_text']}",
        reply_markup=ru_main_dkb()
    )
    await udb.set_language("ru", int(message.from_user.id))

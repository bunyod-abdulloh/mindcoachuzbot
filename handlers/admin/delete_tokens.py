from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from loader import dp, appdb


@dp.message_handler(F.text == "tokens", user_id=ADMINS[0], state="*")
async def hdelete_tokens(message: types.Message, state: FSMContext):
    await state.finish()

    blacklisted_count = await appdb.blacklisted_count()
    outstanding_count = await appdb.outstanding_count()

    await appdb.delete_blacklisted_tokens()
    await appdb.delete_outstanding_tokens()

    await message.answer(
        f"✅ Tozalandi!\n"
        f"🔴 Blacklisted: {blacklisted_count} ta\n"
        f"⚪ Outstanding: {outstanding_count} ta"
    )

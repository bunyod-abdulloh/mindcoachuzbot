from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters import IsBotAdminFilter
from loader import dp, appdb


@dp.message_handler(IsBotAdminFilter(), F.text == "🚀 Test yoqish", state="*")
async def honn_tests(message: types.Message, state: FSMContext):
    await state.finish()

    await appdb.on_off_tests(value=True)

    await message.answer(
        text="Testlar yoqildi!"
    )


@dp.message_handler(IsBotAdminFilter(), F.text == "🛑 Test o'chirish", state="*")
async def hoff_tests(message: types.Message, state: FSMContext):
    await state.finish()

    await appdb.on_off_tests(value=False)

    await message.answer(
        text="Testlar o'chirildi!"
    )

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters import IsBotAdminFilter
from keyboards.inline.admin import on_off_buttons
from keyboards.inline.callback_data import on_off_cb
from loader import dp, appdb


@dp.message_handler(IsBotAdminFilter(), F.text == "🚀 Test yoqish/o'chirish", state="*")
async def hon_off_start(message: types.Message, state: FSMContext):
    await state.finish()

    tests = await appdb.check_test_status()

    test_str = "Testlar holati\n\n"

    for test in tests:
        test_str += f"{test['code']} | {test['is_active']}\n"

    await message.answer(
        text=test_str,
        reply_markup=on_off_buttons()
    )


@dp.callback_query_handler(on_off_cb.filter(action="on_off"), state="*")
async def hon_off_process(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await state.finish()

    value = callback_data["value"]

    if value == "on":
        await appdb.on_off_tests(value=True)
        await call.answer(
            text="Testlar yoqildi!"
        )
    elif value == "off":
        await appdb.on_off_tests(value=True)
        await call.answer(
            text="Testlar o'chirildi!"
        )
    else:
        await call.message.edit_text(
            text="Admin bosh sahifasi"
        )

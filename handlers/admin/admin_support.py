import asyncio

import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.callback_data import admin_support_cb
from loader import dp, bot


@dp.callback_query_handler(admin_support_cb.filter(action="cancel"), state="*")
async def h_admin_support_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text(
        text="Rad etildi!"
    )


@dp.callback_query_handler(admin_support_cb.filter(action="answer"), state="*")
async def h_adm_support_answer(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await state.finish()

    telegram_id = callback_data.get("telegram_id", None)

    await call.message.edit_text(
        text="Xabaringizni kiriting\n\nMatnli va ovozli xabar yuborsangiz bo'ladi"
    )
    await state.update_data(
        telegram_id=telegram_id
    )
    await state.set_state(
        "adm_support_answer"
    )


@dp.message_handler(state="adm_support_answer", content_types=['text', 'voice'])
async def adm_support_answer_process(message: types.Message, state: FSMContext):
    data = await state.get_data()

    telegram_id = data.get("telegram_id", None)

    admin_text = "Bot admini xabaringizga javob berdi / Администратор бота ответил на ваше сообщение\n\n"

    try:
        if message.content_type == "text":
            await bot.send_message(
                chat_id=telegram_id,
                text=admin_text + message.text
            )

        elif message.content_type == "voice":
            await bot.send_voice(
                chat_id=telegram_id,
                voice=message.voice.file_id,
                caption=admin_text
            )

        await asyncio.sleep(1)

        await message.answer(
            text="Xabar foydalanuvchiga yuborildi!"
        )
    except aiogram.exceptions.BotBlocked or Exception:
        await message.answer(
            text="Xabar foydalanuvchiga yuborilmadi! Foydalanuvchi botdan foydalanishni to'xtatgan!"
        )
    await state.finish()

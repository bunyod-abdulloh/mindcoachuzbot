import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (
    BotBlocked, ChatNotFound, UserDeactivated, RetryAfter,
)

from keyboards.inline.callback_data import admin_support_cb
from loader import dp, bot


async def with_retry(factory):
    """RetryAfter (429) bo'lsa Telegram aytgan vaqt kutib qayta yuboradi."""
    while True:
        try:
            return await factory()
        except RetryAfter as e:
            await asyncio.sleep(e.timeout)


@dp.callback_query_handler(admin_support_cb.filter(action="cancel"), state="*")
async def h_admin_support_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(text="Rad etildi!")


@dp.callback_query_handler(admin_support_cb.filter(action="answer"), state="*")
async def h_adm_support_answer(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    telegram_id = callback_data.get("value")

    await call.message.edit_text(
        text="Xabaringizni kiriting\n\nMatnli va ovozli xabar yuborsangiz bo'ladi"
    )
    await state.set_state("adm_support_answer")
    await state.update_data(telegram_id=telegram_id)


@dp.message_handler(state="adm_support_answer", content_types=['text', 'voice'])
async def adm_support_answer_process(message: types.Message, state: FSMContext):
    data = await state.get_data()
    telegram_id = data.get("telegram_id")

    admin_text = (
        "Bot admini xabaringizga javob berdi / "
        "Администратор бота ответил на ваше сообщение\n\n"
    )

    try:
        if message.content_type == "text":
            await with_retry(lambda: bot.send_message(
                chat_id=telegram_id,
                text=admin_text + message.text,
            ))
        elif message.content_type == "voice":
            await with_retry(lambda: bot.send_voice(
                chat_id=telegram_id,
                voice=message.voice.file_id,
                caption=admin_text,
            ))

        await message.answer(text="Xabar foydalanuvchiga yuborildi!")

    except (BotBlocked, ChatNotFound, UserDeactivated):
        await message.answer(
            text="Xabar foydalanuvchiga yuborilmadi! "
                 "Foydalanuvchi botdan foydalanishni to'xtatgan!"
        )
    except Exception as e:
        logging.exception(e)
        await message.answer(text="Xatolik yuz berdi, qayta urinib ko'ring.")
    finally:
        await state.finish()

from typing import List

import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from filters.admins import IsBotAdminFilter
from keyboards.default.admin_buttons import admin_main_btns
from keyboards.default.user_buttons import main_dkb
from loader import dp, udb, adb, bot
from magic_filter import F
from services.texts import ADMIN_WARNING_TEXT
from states.admin import AdminStates
from utils.db_functions import send_message_to_users, send_media_group_to_users


@dp.message_handler(IsBotAdminFilter(), Command(commands="admin"))
async def admin_main_page(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Admin panel", reply_markup=admin_main_btns)


@dp.message_handler(IsBotAdminFilter(), F.text == "Foydalanuvchilar soni")
async def user_count(message: types.Message):
    count = await udb.count_users()
    await message.answer(f"Foydalanuvchilar soni: {count}")


@dp.message_handler(IsBotAdminFilter(), F.text == "Yaxin tozalash")
async def handle_delete_from_yaxin(message: types.Message):
    count = await adb.delete_from_yaxin()
    await message.answer(f"{count} ta qator o'chirildi!")


@dp.message_handler(IsBotAdminFilter(), F.text == "Leo tozalash")
async def handle_delete_from_yaxin(message: types.Message):
    count = await adb.delete_from_leo()
    await message.answer(f"{count} ta qator o'chirildi!")


@dp.message_handler(IsBotAdminFilter(), F.text == "Ayzenk tozalash")
async def handle_delete_from_yaxin(message: types.Message):
    count = await adb.delete_from_ayzenk()
    await message.answer(f"{count} ta qator o'chirildi!")


@dp.message_handler(IsBotAdminFilter(), F.text == "✅ Oddiy post yuborish", state="*")
async def send_to_bot_users(message: types.Message, state: FSMContext):
    await state.finish()
    send_status = await adb.get_send_status()
    if send_status:
        await message.answer("Xabar yuborish jarayoni yoqilgan! Hisobot kelganidan so'ng xabar yuborishingiz mumkin!")
    else:
        await message.answer(text=ADMIN_WARNING_TEXT)
        await AdminStates.SEND_TO_USERS.set()


@dp.message_handler(state=AdminStates.SEND_TO_USERS, content_types=types.ContentTypes.ANY)
async def send_to_bot_users_two(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Xabar yuborish boshlandi!", reply_markup=main_dkb)
    success_count, failed_count = await send_message_to_users(message)

    await adb.update_send_status(False)
    await message.answer(
        f"Xabar {success_count} ta foydalanuvchiga yuborildi!\n{failed_count} ta foydalanuvchi botni bloklagan."
    )


@dp.message_handler(IsBotAdminFilter(), F.text == "🎞 Mediagroup post yuborish")
async def send_media_to_bot(message: types.Message):
    send_status = await adb.get_send_status()
    if send_status:
        await message.answer("Xabar yuborish jarayoni yoqilgan! Hisobot kelganidan so'ng xabar yuborishingiz mumkin!")
    else:
        await message.answer(text=ADMIN_WARNING_TEXT)
        await AdminStates.SEND_MEDIA_TO_USERS.set()


@dp.message_handler(state=AdminStates.SEND_MEDIA_TO_USERS, content_types=types.ContentTypes.ANY, is_media_group=True)
async def send_media_to_bot_second(message: types.Message, album: List[types.Message], state: FSMContext):
    await state.finish()
    await message.answer(text="Xabar yuborish boshlandi!", reply_markup=main_dkb)
    try:

        media_group = types.MediaGroup()

        for obj in album:
            file_id = obj.photo[-1].file_id if obj.photo else obj[obj.content_type].file_id
            media_group.attach(
                {"media": file_id, "type": obj.content_type, "caption": obj.caption}
            )

    except Exception as err:
        await message.answer(f"Media qo'shishda xatolik!: {err}")
        return

    success_count, failed_count = await send_media_group_to_users(media_group)

    await adb.update_send_status(False)
    await message.answer(
        f"Media {success_count} ta foydalanuvchiga yuborildi!\n{failed_count} ta foydalanuvchi botni bloklagan."
    )


@dp.message_handler(IsBotAdminFilter(), F.text == "user", state="*")
async def handle_user_datas(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text="Telegram ID kiriting"
    )
    await state.set_state("get_user_datas")


@dp.message_handler(state="get_user_datas", content_types=['text'])
async def handle_user_data_state(message: types.Message, state: FSMContext):
    user_datas = await bot.get_chat(chat_id=message.text)
    await message.answer(
        text=f"{user_datas}"
    )
    await state.finish()


@dp.message_handler(IsBotAdminFilter(), F.text == "add_datas", state="*")
async def handle_add_fullnames(message: types.Message, state: FSMContext):
    await state.finish()

    users = await udb.select_all_users()

    for u in users:
        try:
            full_name = (await bot.get_chat(chat_id=u['telegram_id'])).full_name
            username = (await bot.get_chat(chat_id=u['telegram_id'])).username

            await udb.set_full_name(full_name, u['telegram_id'])
            await udb.set_username(username, u['telegram_id'])
        except asyncpg.exceptions.StringDataRightTruncationError:
            pass
        except Exception:
            continue

    await message.answer(
        text="Ma'lumotlar qo'shildi!"
    )

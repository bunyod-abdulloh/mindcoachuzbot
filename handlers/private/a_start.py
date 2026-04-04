from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Command
from magic_filter import F

from keyboards.default.user_buttons import main_dkb
from keyboards.inline.user_ibuttons import user_main_ikb, gender_ikb
from loader import dp, udb
from states.user import UserAnketa


@dp.message_handler(CommandStart(), state="*")
async def start(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    await state.finish()
    user = await udb.check_user(user_id)

    if user:
        await message.answer(
            text="Bosh sahifa", reply_markup=main_dkb
        )
        await message.answer(
            text="Kerakli bo'limni tanlang", reply_markup=user_main_ikb()
        )
    else:
        fullname = message.from_user.full_name
        username = message.from_user.username
        await udb.add_user(user_id, fullname, username)
        await message.answer(
            text="Jinsingizni tanlang", reply_markup=gender_ikb()
        )
        await UserAnketa.GET_GENDER.set()


@dp.callback_query_handler(state=UserAnketa.GET_GENDER)
async def handle_get_gender(call: types.CallbackQuery):
    gender = call.data

    telegram_id = str(call.from_user.id)
    await udb.set_gender(gender, telegram_id)

    await call.message.edit_text(
        text="Yoshingizni kiriting\n\n<b>Namuna: 35</b>"
    )
    await UserAnketa.GET_AGE.set()


@dp.message_handler(state=UserAnketa.GET_AGE, content_types=types.ContentType.TEXT)
async def handle_get_user_age(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        age = message.text.strip()
        telegram_id = str(message.from_user.id)
        await udb.set_age(age, telegram_id)

        await message.answer(
            text="Bosh sahifa", reply_markup=user_main_ikb()
        )
        await state.finish()
    else:
        await message.answer(
            text="Faqat raqam kiritilishi lozim!"
        )


@dp.message_handler(Command("id"), state="*")
async def handle_get_user_id(message: types.Message):
    await message.answer(
        text=f"Sizning id raqamingiz:\n\n"
             f"<code>{message.from_user.id}</code>"
    )

@dp.message_handler(F.text == "🏡 Bosh sahifa", state="*")
async def handle_main_page(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text=message.text, reply_markup=user_main_ikb()
    )


@dp.message_handler(Command("id"), state="*")
async def handle_return_tg_id(message: types.Message, state: FSMContext):
    await message.answer(
        text=f"Sizning id raqamingiz:\n\n<code>{message.from_user.id}</code>"
    )

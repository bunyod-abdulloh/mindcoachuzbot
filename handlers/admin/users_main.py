from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters import IsBotAdminFilter
from handlers.private.portret import handle_portret_main
from keyboards.inline.admin import users_pagination_ikb, search_type_ikb
from keyboards.inline.callback_data import users_page_cb, select_type_cb
from loader import dp, appdb


@dp.callback_query_handler(F.data == "admin_back_search", state="*")
@dp.message_handler(IsBotAdminFilter(), F.text == "💪 Sportchi natijalari")
async def show_users(event: types.Message | types.CallbackQuery):
    if isinstance(event, types.CallbackQuery):
        obj = event.message.edit_text
    else:
        obj = event.answer

    await obj(
        text="Qidiriv turini tanlang\n\n"
             "1. Tugmalar orqali sportchini qidirib natijalarini ko'rish\n\n"
             "2. Telefon raqam kiritish orqali sportchi natijalarini ko'rish",
        reply_markup=search_type_ikb()
    )


@dp.callback_query_handler(select_type_cb.filter())
async def hselect_search_type(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    search_type = callback_data["value"]

    if search_type == "1":
        await call.message.edit_text(
            text="Foydalanuvchilar ro'yxati:",
            reply_markup=await users_pagination_ikb(page=1)
        )
    else:
        await call.message.edit_text(
            text="Sportchi telefon raqamini kiriting"
        )
        await state.set_state("search_athlete")


@dp.message_handler(IsBotAdminFilter(), commands=["cancel"], state="*")
async def hcancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text="Qidiruv bekor qilindi!"
    )


@dp.message_handler(state="search_athlete", content_types=['text'])
async def hsearch_by_phone(message: types.Message, state: FSMContext):
    phone = message.text.strip()

    athlete = await appdb.get_athlete_by_phone(
        phone_number=phone
    )

    if not athlete:
        await message.answer(
            text="Topilmadi!\n\n"
                 "Qidiruvni bekor qilish uchun /cancel buyrug'ini kiriting!"
        )
    else:
        await handle_portret_main(
            message, {
                "action": "portrait",
                "lang": "uz",
                "tg_id": athlete['telegram_id']
            },
            True
        )
        await state.finish()


@dp.callback_query_handler(users_page_cb.filter(), state="*")
async def paginate_users(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=0)
    action = callback_data["action"]
    current_page = int(callback_data["page"])

    if action == "prev":
        new_page = current_page - 1
    elif action == "next":
        new_page = current_page + 1
    else:
        new_page = current_page
    try:
        await call.message.edit_text(
            text=f"Sportchilar ro'yxati | {new_page} - sahifa",
            reply_markup=await users_pagination_ikb(page=new_page)
        )
        return
    except Exception:
        pass

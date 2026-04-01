from aiogram import types
from data.config import ADMINS
from loader import dp
from magic_filter import F
from services.error_service import notify_exception_to_admin
from utils.projects import get_all_projects, send_projects_page


@dp.callback_query_handler(F.data == "projects", state="*")
async def interviews_projects_hr_one(call: types.CallbackQuery):
    extract = await get_all_projects()
    if extract:
        current_page = 1
        all_pages = len(extract)
        await send_projects_page(extract=extract, current_page=current_page, all_pages=all_pages, call=call)
    else:
        await call.message.edit_text(text="Hozircha suhbat va loyihalar bo'limi ishga tushmadi!")



@dp.callback_query_handler(F.data.startswith("prev_projects:"))
async def interviews_projects_hr_prev(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    extract = await get_all_projects()
    if not extract:
        return

    current_page = int(call.data.split(':')[1])
    all_pages = len(extract)
    current_page = all_pages if current_page == 1 else current_page - 1
    await send_projects_page(extract=extract, current_page=current_page, all_pages=all_pages, call=call)


@dp.callback_query_handler(F.data.startswith("alert_projects"))
async def interviews_projects_hr_alert(call: types.CallbackQuery):
    current_page = call.data.split(":")[1]
    await call.answer(text=f"Siz {current_page} - sahifadasiz", show_alert=True)


@dp.callback_query_handler(F.data.startswith("next_projects:"))
async def interviews_projects_hr_next(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    try:
        current_page, all_pages = map(int, call.data.split(':')[1:])
        if current_page == all_pages:
            current_page = 1
        else:
            current_page += 1
        extract = await get_all_projects()
        if extract:
            await send_projects_page(extract=extract, current_page=current_page, all_pages=all_pages, call=call)
    except IndexError:
        await call.answer(text="Boshqa sahifa mavjud emas!", show_alert=True)
    except Exception as err:
        await notify_exception_to_admin(err=err)

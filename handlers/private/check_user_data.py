from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from magic_filter import F

from loader import dp


@dp.callback_query_handler(F.text == "user_check_data", state="*")
async def handle_user_check_data(call: CallbackQuery, state: FSMContext):
    pass
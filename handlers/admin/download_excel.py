import os

from aiogram import types
from aiogram.types import InputFile
from magic_filter import F

from filters import IsBotAdminFilter
from loader import dp
from services.export_to_xls import export_athletes_to_excel


@dp.message_handler(IsBotAdminFilter(), F.text == "📄 Excel yuklab olish", state="*")
async def send_athletes_excel(message: types.Message):
    file_path = await export_athletes_to_excel()

    try:
        await message.answer_document(
            document=InputFile(file_path),
            caption="Sportchilar ro'yxati va test natijalari (Excel)."
        )
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    # for n in data:
    #     print(n['full_name'])
    #     tests = json.loads(n['tests'])
    #     print(tests.get('eysenc', "Topshirmagan"))

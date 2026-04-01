from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin_ibuttons import are_you_sure_markup, select_treatments_ikb
from keyboards.inline.callback_datas import check_appointment_cb, select_treatments_cb
from keyboards.inline.user_ibuttons import tests_page_ikb
from loader import dp, adldb, bot
from states.admin import AdminStates


@dp.callback_query_handler(check_appointment_cb.filter(action="cancel"), state="*")
async def handle_check_consultation(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=0)
    patient_id = int(callback_data.get("patient"))
    appointment_id = int(callback_data.get("appointment"))
    await state.update_data(
        patient_id=patient_id, appointment_id=appointment_id
    )

    await call.message.answer(
        text="Rad etilish sababini kiriting"
    )
    await AdminStates.СANCEL_CONSULTATION.set()


@dp.message_handler(state=AdminStates.СANCEL_CONSULTATION, content_types=types.ContentType.TEXT)
async def handle_check_consultation_st(message: types.Message, state: FSMContext):
    patient_id = (await state.get_data()).get("patient_id")
    appointment_id = (await state.get_data()).get("appointment_id")
    telegram_id = await adldb.get_patient_telegram_by_id(patient_id)

    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=f"Konsultasiya uchun so'rovingiz rad etildi!\n\nSabab:\n\n<b>{message.text}</b>"
        )
    except Exception as err:
        await message.answer(
            text=f"{err}"
        )

    await adldb.cancel_appointment(
        appointment_id=appointment_id
    )
    await message.answer(
        text="Xabar foydalanuvchiga yuborildi!\n\nFoydalanuvchi ma'lumotlari o'chirilsinmi?",
        reply_markup=are_you_sure_markup()
    )
    await AdminStates.DELETE_USER_DATAS.set()


@dp.callback_query_handler(state=AdminStates.DELETE_USER_DATAS)
async def handle_delete_user_datas(call: types.CallbackQuery, state: FSMContext):
    if call.data == "yes":
        patient_id = int((await state.get_data()).get("patient_id"))
        await adldb.delete_patient_datas(patient_id=patient_id)
        await call.message.edit_text(
            text="Ma'lumot o'chirildi!"
        )
    elif call.data == "no":
        await call.message.edit_text(
            text="Rahmat!"
        )
    await state.finish()


@dp.callback_query_handler(check_appointment_cb.filter(action="check"), state="*")
async def handle_check_appointment(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=0)
    await state.finish()
    patient_id = callback_data.get("patient", None)
    appointment_id = callback_data.get("appointment", None)

    await call.message.answer(
        text="Davolanish oldin/keyinligini tanlang",
        reply_markup=select_treatments_ikb(
            appointment_id=appointment_id, patient_id=patient_id)
    )


@dp.callback_query_handler(select_treatments_cb.filter(action="after"), state="*")
@dp.callback_query_handler(select_treatments_cb.filter(action="before"), state="*")
async def handle_save_treatment_before(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    treatment_stage = str(callback_data.get("action"))
    patient_id = int(callback_data.get("patient"))
    appointment_id = int(callback_data.get("appointment"))

    patient_telegram = await adldb.get_patient_telegram_by_id(
        patient_id=patient_id
    )

    appointment_date = await adldb.set_appointment(
        treatment_stage=treatment_stage, appointment_id=appointment_id
    )

    out_date = appointment_date.strftime("%H:%M | %d.%m.%Y")

    await bot.send_message(
        chat_id=patient_telegram,
        text=f"Konsultasiya uchun qabul tasdiqlandi!\n\n"
             f"Sana: {out_date}\n"
             f"Shifokor: Dr.Gavhar Darvish\n\n"
             f"Qabulga kelishdan oldin testlarni ishlashni unutmang!",
        reply_markup=tests_page_ikb()
    )

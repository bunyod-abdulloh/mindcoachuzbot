from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.consultation_ikbs import confirm_reenter_ibtn
from keyboards.inline.user_ibuttons import user_main_ikb

from loader import dp, adldb
from magic_filter import F
from services.texts import patient_dict


@dp.callback_query_handler(F.data == "personal_cabinet", state="*")
async def handle_personal_cabinet_main(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    patient = await adldb.get_patient(telegram_id=str(call.from_user.id))

    if patient:
        full_name = patient['name']
        gender = patient_dict[patient['gender']]
        age = patient['age']
        phone = patient['phone']
        marital_status = patient_dict[patient['marital_status']]
        absence_children = patient_dict[patient['absence_children']]
        work = patient['work']
        result_eeg = patient['result_eeg']

        await call.message.edit_text(
            text=f"Sizning ma'lumotlaringiz\n\n"
                 f"1. Ism sharif: {full_name}\n"
                 f"2. Jins: {gender}\n"
                 f"3. Yosh: {age}\n"
                 f"4. Turmush holati: {marital_status}\n"
                 f"5. Farzandlar: {absence_children}\n"
                 f"6. Ish soha: {work}\n"
                 f"7. EEG natijasi: {result_eeg}\n"
                 f"8. Telefon raqam: {phone}\n\n"
                 f"O'zgartirmoqchi bo'lsangiz kerakli tartib raqamni tanlang",
            reply_markup=confirm_reenter_ibtn()
        )
        await state.update_data(
            personal_cabinet=True
        )
    else:
        await call.answer(
            text="Ushbu bo'lim faqat qabulga yozilganlar uchun ishlaydi!", show_alert=True
        )


@dp.callback_query_handler(F.data == "pr_cabinet_back", state="*")
async def handle_back_to_main(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        text="Bosh sahifa", reply_markup=user_main_ikb()
    )
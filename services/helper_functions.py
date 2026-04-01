from datetime import datetime, date

import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.default.user_buttons import main_dkb
from keyboards.inline.admin_ibuttons import check_patient_datas_ikbs
from loader import udb, adldb, bot
from services.consultation import week_days, patient_dict
from services.texts import personal_data
from states.user import UserAnketa


COMPANY_ID = 1


async def notify_admin(photo_file_id, full_name, gender, age, marital_status,
                       absence_children, work, eeg_result, phone, telegram_id,
                       username, consultation_info):
    caption = (
        f"<b>Ism sharifi:</b> {full_name}\n"
        f"<b>Jinsi:</b> {gender}\n"
        f"<b>Yoshi:</b> {age}\n"
        f"<b>Oilaviy holati:</b> {marital_status}\n"
        f"<b>Farzandlari:</b> {absence_children}\n"
        f"<b>Ish sohasi:</b> {work}\n"
        f"<b>EEG natijasi:</b> {eeg_result}\n"
        f"<b>Telefon raqami:</b> {phone}\n"
        f"<b>Konsultatsiya sanasi:</b> {consultation_info['date']} | {consultation_info['day']} | {consultation_info['time']}\n"
        f"<b>Davomiyligi:</b> {consultation_info['duration']} daqiqa\n"
    )

    # Send message to admin
    await bot.send_photo(
        chat_id=ADMINS[1],
        photo=photo_file_id,
        caption=f"<b>Yangi bemor ma'lumotlari qabul qilindi!</b>\n\n"
                f"{caption}"
                f"<b>Telegram ID:</b> <code>{telegram_id}</code>\n"
                f"<b>Telegram username:</b>  @{username}\n\n"
                f"<b>Testlar natijasini CRMdan ko'rishingiz mumkin!</b>",
        reply_markup=check_patient_datas_ikbs(patient_telegram=telegram_id)
    )

    # Send message to patient
    await bot.send_photo(
        chat_id=telegram_id,
        photo=photo_file_id,
        caption=f"{caption}\n"
                f"Ma'lumotlaringiz qabul qilindi!\n\nUshbu bo'lim hozirda test rejimida ishlamoqda!\n\n"
                f"Shifokor ish kunlari va qabul vaqtlari haqiqiy emas!\n\nTest rejimi tugagach bot orqali xabar qilamiz!"
    )


async def add_appointment(patient_id, age, consultation_info):
    # Parse user input (Toshkent vaqti)
    appointment_datetime = datetime.strptime(
        f"{consultation_info['date']} {consultation_info['time']}",
        "%d-%m-%Y %H:%M"
    )

    # Lokal vaqt sifatida belgilash
    tz = pytz.timezone("Asia/Tashkent")
    local_dt = tz.localize(appointment_datetime)

    # UTC ga aylantirish va tzinfo olib tashlash (naive datetime)
    utc_dt = local_dt.astimezone(pytz.UTC).replace(tzinfo=None)

    age_group = "adult" if age >= 17 else "child"
    doctor_id = await adldb.get_doctor_id()

    await adldb.add_to_appointments(
        patient_id=patient_id,
        doctor_id=doctor_id,
        company_id=COMPANY_ID,
        consultation_duration=consultation_info['duration'],
        age_group=age_group,
        appointment_date=utc_dt
    )


# 1. O'zbekcha simptom nomlari
uzbek_symptoms = {
    1: "Bosh og‘rig‘i bormi?",
    2: "Bosh aylanishi bormi?",
    3: "Ko‘ngil aynishi bormi?",
    4: "Qorin og‘rishi bormi?",
    5: "Tomoqda bo‘g‘ilish hissi bormi?",
    6: "Yurak urib ketishi bormi?",
    7: "Uyqu buzilishi bormi?",
    8: "Kayfiyatsizlik bormi?",
    9: "Yig‘lash bormi?",
    10: "Befarqlik bormi?"
}

# 2. Inglizcha kalitlari
english_symptoms = {
    1: "headache",
    2: "dizziness",
    3: "nausea",
    4: "abdominal_pain",
    5: "feeling_choking",
    6: "heart_palpitations",
    7: "sleep_disturbance",
    8: "low_mood",
    9: "crying",
    10: "indifference"
}


async def handle_tests_main(event: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(event, types.CallbackQuery):
        user_id = event.from_user.id
        message_obj = event.message
    else:
        user_id = event.from_user.id
        message_obj = event

    check_user = await udb.check_user(telegram_id=str(user_id))

    await state.finish()

    if check_user:
        await message_obj.answer(text=main_dkb_words['tests'], reply_markup=tests_main_dkb)
        return
    else:
        await message_obj.answer(text=personal_data['age'])
        await UserAnketa.GET_AGE.set()


# import csv
#
# result = {}
#
# with open('darvish_users.json', mode='r', encoding='utf-8') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         telegram_id = int(row['telegram_id'])
#         fio = row['fio'] if row['fio'] not in ('null', 'None', '') else None
#         phone = row['phone'] if row['phone'] not in ('null', 'None', '') else None
#         result[telegram_id] = {'fio': fio, 'phone': phone}
#


users_data = {}

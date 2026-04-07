from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from keyboards.inline.admin_ibuttons import check_patient_datas_ikbs
from keyboards.inline.consultation_ikbs import create_free_time_keyboard
from loader import dp, adldb, bot, udb
from services.consultation import show_consultation_dates_menu
from services.texts import week_days, patient_dict
from states.user import UserAnketa


@dp.callback_query_handler(F.data.startswith("duration_"), state="*")
async def handle_consultation_duration(call: types.CallbackQuery, state: FSMContext):
    duration = call.data.split("_")[1]
    await state.update_data(
        consultation_duration=duration
    )
    await show_consultation_dates_menu(call=call)


@dp.callback_query_handler(F.data.startswith("date_"), state="*")
async def handle_choose_date(call: types.CallbackQuery, state: FSMContext):
    _, day_code, date_str, time_range = call.data.split("_")

    start_time, end_time = time_range.split("-")
    busy_times = []

    formatted_date = datetime.strptime(date_str, "%d-%m-%Y").date()

    doctor_time = await adldb.get_doctor_time(
        formatted_date=formatted_date
    )

    for time in doctor_time:
        busy_times.append(time['appointment_time'])

    keyboard = create_free_time_keyboard(start_str=start_time, end_str=end_time, busy_times=busy_times)

    if len(keyboard['inline_keyboard']) == 1:
        await call.answer(
            text="Bu sanada qabul to'lgan!", show_alert=True
        )
        return

    await call.answer()
    await call.message.edit_text(
        f"📅 Sana: {date_str} | {week_days[day_code]}\n\n🕒 Ish vaqti: {start_time} - {end_time}\n\n"
        f"Kerakli vaqtni tanlang", reply_markup=keyboard
    )
    await state.update_data(
        consultation_date=date_str, consultation_day=day_code
    )


@dp.callback_query_handler(F.data.startswith("select_time-"), state="*")
async def handle_select_time(call: types.CallbackQuery, state: FSMContext):
    time = call.data.split("-")[1]
    await state.update_data(consultation_time=time)
    await call.message.edit_text(
        text="To'lov cheki rasmini yuboring"
    )
    await UserAnketa.PAYMENT.set()


@dp.message_handler(state=UserAnketa.PAYMENT, content_types=types.ContentType.PHOTO)
async def handle_consultation_chek(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photo_id = message.photo[-1].file_id

    # Ma'lumotlar yetarliligini tekshirish
    if len(data) not in (4, 10):
        await message.answer("Xatolik mavjud! Ma'lumotlaringizni qayta kiriting!")
        return await state.finish()

    try:
        telegram_id = str(message.from_user.id)
        # Asosiy qabul ma'lumotlari
        consultation_duration = data.get("consultation_duration")
        consultation_date = data.get("consultation_date")
        consultation_day = data.get("consultation_day")
        consultation_time = data.get("consultation_time")

        # Bemorga tegishli ma'lumotlarni olish
        if len(data) == 4:
            # Foydalanuvchi avval ro'yxatdan o'tgan
            patient = await adldb.get_patient(telegram_id)
            full_name = patient["name"]
            gender = patient["gender"]
            age = patient["age"]
            marital_status = patient["marital_status"]
            absence_children = patient["absence_children"]
            work = patient["work"]
            result_eeg = patient["result_eeg"]
            phone = patient["phone"]
        else:
            # Yangi bemor
            full_name = data["user_full_name"]
            marital_status = data["marital_status"]
            absence_children = data["absence_children"]
            work = data["work"]
            result_eeg = data["eeg_result"]
            phone = data["phone"]
            patient_info = await udb.get_user_gender_age(telegram_id)
            gender = patient_info["gender"]
            age = patient_info["age"]

        # Yosh toifasini aniqlash
        age_group = "adult" if int(age) >= 18 else "child"

        # Qabul sanasini yaratish
        naive_dt = datetime.strptime(
            f"{consultation_date} {consultation_time}",
            "%d-%m-%Y %H:%M"
        )

        # foydalanuvchi kiritgan vaqt - Asia/Tashkent
        local_dt = naive_dt.replace(tzinfo=ZoneInfo("Asia/Tashkent"))

        # UTC ga o‘giramiz
        utc_dt = local_dt.astimezone(ZoneInfo("UTC"))

        # DB uchun tzsiz yuboramiz
        appointment_date = utc_dt.replace(tzinfo=None)

        # Bemorni bazaga qo‘shish (yoki yangilash)
        patient_id = await adldb.add_patient(
            telegram_id=str(message.from_user.id),
            name=full_name,
            phone=phone,
            marital_status=marital_status,
            absence_children=absence_children,
            work=work,
            result_eeg=result_eeg
        )

        # Qabulni bazaga qo‘shish
        appointment_id = await adldb.add_to_appointments(
            patient_id=patient_id,
            consultation_duration=consultation_duration,
            age_group=age_group,
            appointment_date=appointment_date
        )

        # Foydalanuvchiga matn tayyorlash
        text = (
            f"1. Ism sharif: {full_name}\n"
            f"2. Jins: {patient_dict[gender]}\n"
            f"3. Yosh: {age}\n"
            f"4. Oilaviy holat: {patient_dict[marital_status]}\n"
            f"5. Farzandlar: {patient_dict[absence_children]}\n"
            f"6. Ish sohasi: {work.capitalize()}\n"
            f"7. EEG natijasi: {result_eeg.capitalize()}\n"
            f"8. Telefon raqam: {phone}\n"
            f"9. Qabul kuni va vaqti: {consultation_time} | {consultation_date} | {consultation_day.capitalize()}\n"
            f"10. Qabul davomiyligi: {consultation_duration} daqiqa\n\n"
        )

        # Foydalanuvchiga tasdiqlash xabari
        send_check = "Qabul tasdiqlanganidan so'ng testlarni ishlashni unutmang!"

        if len(data) == 4:
            await message.answer(
                f"Qabulga yozildingiz! Qabulingiz haqidagi xabar adminga yuborildi.\n\n"
                f"Kiritgan ma'lumotlaringizda xatolik bo'lsa, admin Siz bilan bog'lanadi.\n\n"
                f"{send_check}"
            )
        else:
            await message.answer_photo(
                photo=photo_id,
                caption=f"Ma'lumotlaringiz qabul qilindi!\n\n{text}"
                        f"{send_check}"
            )

        # Adminga xabar yuborish
        await bot.send_photo(
            chat_id=ADMINS[0],
            photo=photo_id,
            caption=f"Yangi qabul ma'lumotlari!\n\n{text}",
            reply_markup=check_patient_datas_ikbs(appointment_id=appointment_id, patient_id=patient_id)
        )

        await state.finish()

    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}")
        await state.finish()

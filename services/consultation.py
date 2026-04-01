from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta, time

from keyboards.inline.consultation_ikbs import confirm_reenter_ibtn, show_consultation_dates_keyboard
from loader import adldb
from services.texts import personal_data, consultation_text, patient_dict, week_days
from states.user import UserAnketa


async def check_patient_datas(event: types.Message | types.CallbackQuery, state: FSMContext) -> str | None:
    patient = await adldb.get_patient(telegram_id=str(event.from_user.id))

    # --- Patient mavjud emas ---
    if not patient:
        text = f"{consultation_text}\n\n{personal_data['fullname']}\n\n"

        if isinstance(event, types.CallbackQuery):
            await event.message.edit_text(text)
        else:
            await event.answer(text)

        await UserAnketa.FULL_NAME.set()
        return None

    # --- Patient mavjud bo'lsa ---
    await state.finish()

    full_name = patient['name']
    gender = patient_dict[patient['gender']]
    age = patient['age']
    marital_status = patient_dict[patient['marital_status']]
    absence_children = patient_dict[patient['absence_children']]
    work = patient['work']
    result_eeg = patient['result_eeg']
    phone = patient['phone']

    text = (
        f"{consultation_text}\n\n"
        f"Ma'lumotlaringiz saqlangan\n\n"
        f"1. Ism sharif: {full_name}\n"
        f"2. Jins: {gender}\n"
        f"3. Yosh: {age}\n"
        f"4. Oilaviy holat: {marital_status}\n"
        f"5. Farzandlar: {absence_children}\n"
        f"6. Ish sohasi: {work.capitalize()}\n"
        f"7. EEG natijasi: {result_eeg.capitalize()}\n"
        f"8. Telefon raqam: {phone}\n\n"
        f"Barchasi to'g'ri bo'lsa <b>Tasdiqlash</b> tugmasini, "
        f"to'g'ri bo'lmasa kerakli tugmani bosing"
    )

    kb = confirm_reenter_ibtn(if_consultation=True)

    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text=text, reply_markup=kb)
    else:
        await event.answer(text, reply_markup=kb)

    return None


def float_to_time_str(hour_float):
    hours = int(hour_float)
    minutes = int((hour_float - hours) * 60)
    return time(hour=hours, minute=minutes).strftime("%H:%M")


def generate_workday_text(doctor: list) -> str:
    lines = ["Konsultasiya sanasini tanlang\n\n"
             "<b>Ish kun va vaqtlari</b>\n"]
    for day in doctor:
        start_hour = float_to_time_str(hour_float=day['start_hour'])
        end_hour = float_to_time_str(hour_float=day['end_hour'])
        day_name = week_days.get(day['code'], day['code'].capitalize())
        lines.append(f"{day_name} | {start_hour} - {end_hour}")
    return "\n".join(lines)


def get_upcoming_work_dates_with_hours(doctor: list[dict], days_ahead=60) -> dict[
    str, dict[str, list[str] | list[str]]]:
    """
    doctor - quyidagi ko‘rinishda bo‘ladi:
    [
        {'code': 'dushanba', 'start_hour': 9.0, 'end_hour': 17.0},
        {'code': 'seshanba', 'start_hour': 9.0, 'end_hour': 17.0},
        ...
    ]
    """
    day_code_to_weekday = {
        "dushanba": 0,
        "seshanba": 1,
        "chorshanba": 2,
        "payshanba": 3,
        "juma": 4,
        "shanba": 5,
        "yakshanba": 6
    }

    today = datetime.today().date()
    dates_by_day = {}

    for day in doctor:
        code = day['code']
        start_hour = float_to_time_str(day['start_hour'])
        end_hour = float_to_time_str(day['end_hour'])
        weekday_number = day_code_to_weekday[code]

        dates = []
        for i in range(days_ahead):
            current_date = today + timedelta(days=i)
            if current_date.weekday() == weekday_number:
                dates.append(current_date.strftime("%d-%m-%Y"))

        dates_by_day[code] = {
            "dates": dates,
            "time": f"{start_hour}-{end_hour}"
        }

    return dates_by_day


async def show_consultation_dates_menu(call: types.CallbackQuery):
    doctor = await adldb.get_doctor_work_days()

    text = generate_workday_text(doctor)

    dates_by_day = get_upcoming_work_dates_with_hours(doctor)

    keyboard = show_consultation_dates_keyboard(dates_by_day=dates_by_day)

    await call.message.edit_text(text=text, reply_markup=keyboard)


async def check_edit_personal_data(state: FSMContext, message: types.Message | types.CallbackQuery):
    data = await state.get_data()

    if data.get("personal_cabinet"):
        await state.finish()
    else:
        await check_patient_datas(event=message, state=state)

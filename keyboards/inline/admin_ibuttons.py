from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import check_appointment_cb, select_treatments_cb


def check_patient_datas_ikbs(appointment_id, patient_id):
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(
            text="❌ Rad qilish", callback_data=check_appointment_cb.new(
                action="cancel", appointment=appointment_id, patient=patient_id
            )
        ),
        InlineKeyboardButton(
            text="✅ Tasdiqlash", callback_data=check_appointment_cb.new(
                action="check", appointment=appointment_id, patient=patient_id
            )
        )
    )
    return btn


def select_treatments_ikb(appointment_id, patient_id):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="🕒💊 Oldin", callback_data=select_treatments_cb.new(
                action="before", appointment=appointment_id, patient=patient_id
            )
        ),
        InlineKeyboardButton(
            text="Keyin ✅💊", callback_data=select_treatments_cb.new(
                action="after", appointment=appointment_id, patient=patient_id
            )
        )
    )
    return kb


def patient_message_ikbs(telegram_id):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="Xabar yuborish", callback_data=f"admin_message:{telegram_id}"
        )
    )
    return kb


def are_you_sure_markup():
    inline_keyboard = [[
        InlineKeyboardButton(text="❌ No", callback_data='no'),
        InlineKeyboardButton(text="✅ Yes", callback_data='yes')
    ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard

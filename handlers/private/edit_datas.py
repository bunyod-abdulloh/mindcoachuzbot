from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.consultation_ikbs import (
    marital_status_ikb,
    select_gender_btn,
    absence_children_ikb
)
from loader import dp, udb, adldb
from services.consultation import check_edit_personal_data
from services.texts import personal_data, edited_text
from states.user import UserEditDatas


# ====================================================================
#                          HELPERS
# ====================================================================

async def edit_field(
        call: types.CallbackQuery,
        text: str,
        state_to_set,
        keyboard=None
):
    """Callback bosilganda matn chiqarish + state o‘rnatish."""
    await call.answer()
    await call.message.edit_text(text=text, reply_markup=keyboard)
    await state_to_set.set()


async def save_and_continue(
        event: types.Message | types.CallbackQuery,
        state: FSMContext,
        text: str = None
):
    """O‘zgarishni saqlab bo‘lgach umumiy javob + ma’lumotlarni ko‘rsatish."""

    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text or edited_text)
    else:
        await event.answer(text or edited_text)

    # ma'lumotlarni qayta ko‘rsatish
    await check_edit_personal_data(
        state=state,
        message=event
    )


# ====================================================================
#                        EDIT CALLBACKS
# ====================================================================

@dp.callback_query_handler(F.data == "edit_fullname", state="*")
async def edit_fullname(call: types.CallbackQuery):
    await edit_field(call, personal_data['fullname'], UserEditDatas.EDIT_FULLNAME)


@dp.callback_query_handler(F.data == "edit_gender", state="*")
async def edit_gender(call: types.CallbackQuery):
    await edit_field(call, personal_data['gender'], UserEditDatas.EDIT_GENDER, select_gender_btn())


@dp.callback_query_handler(F.data == "edit_age", state="*")
async def edit_age(call: types.CallbackQuery):
    await edit_field(call, personal_data['age'], UserEditDatas.EDIT_AGE)


@dp.callback_query_handler(F.data == "edit_marital_status", state="*")
async def edit_marital_status(call: types.CallbackQuery):
    await edit_field(call, personal_data['marital_status'], UserEditDatas.EDIT_MARITAL_STATUS, marital_status_ikb())


@dp.callback_query_handler(F.data == "edit_absence_children", state="*")
async def edit_absence_children(call: types.CallbackQuery):
    await edit_field(call, personal_data['childrens'], UserEditDatas.EDIT_ABSENCE_CHILDREN, absence_children_ikb())


@dp.callback_query_handler(F.data == "edit_work", state="*")
async def edit_work(call: types.CallbackQuery):
    await edit_field(call, personal_data['work'], UserEditDatas.EDIT_WORK)


@dp.callback_query_handler(F.data == "edit_eeg", state="*")
async def edit_eeg(call: types.CallbackQuery):
    await edit_field(call, personal_data['result_eeg'], UserEditDatas.EDIT_EEG)


@dp.callback_query_handler(F.data == "edit_phone", state="*")
async def edit_phone(call: types.CallbackQuery):
    await edit_field(call, personal_data['phone'], UserEditDatas.EDIT_PHONE)


# ====================================================================
#                      SAVE USER INPUT HANDLERS
# ====================================================================

# === FULL NAME ===
@dp.message_handler(state=UserEditDatas.EDIT_FULLNAME)
async def set_fullname(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer("Faqat harf kiritilishi lozim!")
        return

    telegram_id = str(message.from_user.id)

    await udb.set_fullname(message.text, telegram_id)

    patient = await adldb.check_patient(telegram_id)
    if patient:
        await adldb.set_patient_fullname(message.text, telegram_id)

    await save_and_continue(message, state)


# === GENDER ===
@dp.callback_query_handler(state=UserEditDatas.EDIT_GENDER)
async def set_gender(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    gender = call.data.split("_")[1]
    telegram_id = str(call.from_user.id)

    await udb.set_gender(gender, telegram_id)

    patient = await adldb.check_patient(telegram_id)
    if patient:
        await adldb.set_patient_gender(gender, telegram_id)

    await save_and_continue(call, state)


# === AGE ===
@dp.message_handler(state=UserEditDatas.EDIT_AGE)
async def set_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if not (1 <= age <= 120):
            raise ValueError

        telegram_id = str(message.from_user.id)
        await udb.set_age(str(age), telegram_id)

        patient = await adldb.check_patient(telegram_id)
        if patient:
            await adldb.set_patient_age(str(age), telegram_id)

        await save_and_continue(message, state)

    except ValueError:
        await message.answer(personal_data['warn_age'])


# === MARITAL STATUS ===
@dp.callback_query_handler(state=UserEditDatas.EDIT_MARITAL_STATUS)
async def set_marital_status(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    marital_status = call.data
    telegram_id = str(call.from_user.id)

    await udb.set_marital_status(marital_status, telegram_id)

    patient = await adldb.check_patient(telegram_id)
    if patient:
        await adldb.set_patient_marital_status(marital_status, telegram_id)

    await save_and_continue(call, state)


# === CHILDREN ===
@dp.callback_query_handler(state=UserEditDatas.EDIT_ABSENCE_CHILDREN)
async def set_absence_children(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    absence_children = call.data.split("_")[2]
    telegram_id = str(call.from_user.id)

    await udb.set_absence_children(absence_children, telegram_id)

    patient = await adldb.check_patient(telegram_id)
    if patient:
        await adldb.set_patient_absence_children(absence_children, telegram_id)

    await save_and_continue(call, state)


# === WORK ===
@dp.message_handler(state=UserEditDatas.EDIT_WORK)
async def set_work(message: types.Message, state: FSMContext):
    await udb.set_work(message.text.lower(), str(message.from_user.id))

    patient = await adldb.check_patient(str(message.from_user.id))
    if patient:
        await adldb.set_patient_work(message.text.lower(), str(message.from_user.id))

    await save_and_continue(message, state)


# === EEG ===
@dp.message_handler(state=UserEditDatas.EDIT_EEG)
async def set_eeg(message: types.Message, state: FSMContext):
    await udb.set_result_eeg(message.text.lower(), str(message.from_user.id))

    patient = await adldb.check_patient(str(message.from_user.id))
    if patient:
        await adldb.set_patient_result_eeg(message.text.lower(), str(message.from_user.id))

    await save_and_continue(message, state)


# === PHONE ===
@dp.message_handler(state=UserEditDatas.EDIT_PHONE)
async def set_phone(message: types.Message, state: FSMContext):
    phone = message.text.strip()
    print
    if phone[1:].isdigit():
        telegram_id = str(message.from_user.id)
        await udb.set_phone(phone, telegram_id)

        patient = await adldb.check_patient(telegram_id)
        if patient:
            await adldb.set_patient_phone(phone, telegram_id)

        await save_and_continue(message, state)
    else:
        await message.answer(personal_data['warn_phone'])

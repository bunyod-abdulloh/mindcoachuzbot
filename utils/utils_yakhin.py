# Helper function to handle user data update and state transitions
import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import yxndb, stdb


async def calculate_and_send_results(call: types.CallbackQuery, state: FSMContext):
    scales = {
        "Xavotir mezoni": "xavotir",
        "Nevrotik - depressiya mezoni": "nevrotikdep",
        "Asteniya mezoni": "astenik",
        "Isterik toifadagi javob mezoni": "isterik",
        "Obsessiv-fobik buzilishlar mezoni": "obsessivfobik",
        "Vegetativ buzilishlar mezoni": "vegetativ",
    }

    # Ma'lumotlarni bir marta yig'ib olish
    result = {
        text: scale_value
        for text, scale_value in zip(
            scales.keys(),
            await asyncio.gather(
                *[
                    yxndb.select_datas_temporary(telegram_id=call.from_user.id, scale_type=scale)
                    for scale in scales.values()
                ]
            ),
        )
    }

    # Ma'lumotlarni birlashtirish
    last_result = "\n".join(f"{text}: {scale}" for text, scale in result.items())

    # Nevrotik holatni aniqlash
    nevrotik_detected = any(number < -1.28 for number in result.values())
    nevrotik_text = "Nevrotik holat aniqlandi!" if nevrotik_detected else "Nevrotik holat aniqlanmadi!"

    footer_text = (
        "Mezonlardagi ko'rsatkichlar + 1.28 dan yuqori bo'lsa sog'lomlik darajasini, - 1.28 dan past bo'lsa "
        "nevrotik holat borligidan dalolat beradi. Ikkisini o'rtasidagi ko'rsatkich esa noturg'un psixik "
        "moslashuvchanlikni bildiradi."
    )

    result_message = (
        f"Test turi: Yaxin, Mendelevich | Nevrotik holatni aniqlash\n\n"
        f"{last_result}\n\n{nevrotik_text}\n\n{footer_text}"
    )

    # Xabarni yangilash
    await call.message.edit_text(text=result_message)

    await yxndb.delete_user_yaxintemporary(telegram_id=call.from_user.id)

    yakhin_stt = {
        "anxiety": float(list(result.values())[0]),
        "depression": float(list(result.values())[1]),
        "asthenia": float(list(result.values())[2]),
        "hysteroid_response": float(list(result.values())[3]),
        "obsessive_phobic": float(list(result.values())[4]),
        "vegetative": float(list(result.values())[5]),
        "neurotic_detected": nevrotik_detected
    }

    await state.update_data(yakhin=yakhin_stt)

    await stdb.set_test_result(
        telegram_id=str(call.from_user.id), test_type="Yaxin", result=f"{nevrotik_detected}"
    )

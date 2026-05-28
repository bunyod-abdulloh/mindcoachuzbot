from aiogram import types

from keyboards.inline.base import back_ikb
from keyboards.inline.callback_data import profile_cb, users_page_cb
from loader import dp, appdb
from locales.core import RESULT_ALERT
from locales.ru_locale import EYSENCK_RESULTS_RU, MILLMAN_RESULT_RU
from locales.uz_locale import EYSENCK_RESULTS_UZ, MILLMAN_RESULT_UZ
from services.eysenck_helper import build_eysenck_response
from services.helpers import personal_datas_uz, personal_datas_ru, savollar_result
from services.millman_helper import build_millman_response


@dp.callback_query_handler(profile_cb.filter(action="portrait"))
async def handle_portret_main(event: types.CallbackQuery | types.Message, callback_data: dict, is_admin: bool = False):
    lang_code = callback_data["lang"]
    telegram_id = int(event.from_user.id)

    if is_admin:
        page = callback_data.get("page", 0)
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(
            types.InlineKeyboardButton(
                text="◀️ Orqaga",
                callback_data=users_page_cb.new(action="stay", page=page)
            )
        )
        telegram_id = callback_data["tg_id"]

    else:
        kb = back_ikb(
            lang=lang_code
        )

    await event.answer(
        text=RESULT_ALERT[lang_code]
    )

    athlete = await appdb.check_athlete(telegram_id)
    if not athlete:
        text = "Siz ro'yxatdan o'tmagansiz!" if lang_code == "uz" else "Вы не зарегистрированы!"
        await event.answer(text=text, show_alert=True)
        return

    user = await appdb.get_athlete_full(telegram_id)
    response_text = ""

    eysenc_results = await appdb.get_last_test_results(
        test_type="eysenc",
        user_id=user["user_id"]
    )

    if eysenc_results:
        eysenck_lang = EYSENCK_RESULTS_UZ if lang_code == "uz" else EYSENCK_RESULTS_RU
        response_text = build_eysenck_response(
            raw_scores=eysenc_results["scores"],
            lang=eysenck_lang
        )

    millman_results = await appdb.get_last_test_results(
        test_type="millman",
        user_id=user["user_id"]
    )

    if millman_results:
        millman_lang = MILLMAN_RESULT_UZ if lang_code == "uz" else MILLMAN_RESULT_RU
        response_text += build_millman_response(
            raw_scores=millman_results["scores"],
            lang=millman_lang,
            lang_code=lang_code
        )

    savolnoma_results = await appdb.get_last_test_results(
        test_type="4savollar",
        user_id=user["user_id"]
    )
    response_text += savollar_result(
        result=savolnoma_results, lang=lang_code
    )

    text = (
        personal_datas_uz(data=user, response_text=response_text)
        if lang_code == "uz"
        else personal_datas_ru(data=user, response_text=response_text)
    )

    if isinstance(event, types.Message):
        btn = types.InlineKeyboardMarkup(row_width=1)
        btn.add(
            types.InlineKeyboardButton(
                text="◀️ Ortga", callback_data="admin_back_search"
            )
        )
        await event.answer(
            text=text,
            parse_mode="MARKDOWN",
            reply_markup=btn
        )
    else:
        await event.message.edit_text(
            text=text,
            parse_mode="MARKDOWN",
            reply_markup=kb
        )

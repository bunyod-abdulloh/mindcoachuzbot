import json

from locales.ru_locale import SAVOLNOMA_RESULT_RU, RESULT_WARNING_RU
from locales.uz_locale import SAVOLNOMA_RESULT_UZ, RESULT_WARNING_UZ


def savollar_result(result, lang):
    if result:
        score = json.loads(result["scores"])

        if lang == "uz":
            text = (f"\n\n{SAVOLNOMA_RESULT_UZ['title']['text']} "
                    f"{SAVOLNOMA_RESULT_UZ['options'][score['zarurat']]}\n\n"
                    f"{RESULT_WARNING_UZ}")
            return text
        else:
            text = (f"\n\n{SAVOLNOMA_RESULT_RU['title']['text']} "
                    f"{SAVOLNOMA_RESULT_RU['options'][score['zarurat']]}\n\n"
                    f"{RESULT_WARNING_RU}")
            return text
    return None


def personal_datas_uz(data, response_text):
    text = (
        f"👤 Ism sharif: {data['full_name']}\n"
        f"📞 Telefon raqam: {data['phone_number']}\n"
        f"🏅 Sport turi: {data['sport_type'].capitalize()}\n"
        f"📆 Tajriba: {data['sport_years']}\n"
        f"🎯 Qiziqishlar: {data['hobbies']}\n\n"
        f"{response_text}"
    )
    return text


def personal_datas_ru(data, response_text):
    text = (
        f"👤 Ф.И.О.: {data['full_name']}\n"
        f"📞 Номер телефона: {data['phone_number']}\n"
        f"🏅 Вид спорта: {data['sport_type'].capitalize()}\n"
        f"📆 Опыт: {data['sport_years']}\n"
        f"🎯 Интересы: {data['hobbies']}\n\n"
        f"{response_text}"
    )
    return text


def get_level_millman(value: int, lang_type) -> str | None:
    if lang_type == "uz":
        if value < 0:
            return "Past"
        elif value == 0:
            return "O'rta"
        return "Yuqori"
    return None


def millman_result(millman_results, lang, lang_type):
    scores = json.loads(millman_results["scores"])

    emotional_resilience = get_level_millman(value=scores['emotional_resilience'], lang_type=lang_type)
    self_regulation = get_level_millman(value=scores['self_regulation'], lang_type=lang_type)
    scale_motivation = get_level_millman(value=scores['scale_motivation'], lang_type=lang_type)
    scale_resistance = get_level_millman(value=scores['scale_resistance'], lang_type=lang_type)
    q17 = scores['q17'].capitalize() if scores['q17'] else None

    text = (
        f"\n\n{lang['emotional_resilience']}: {scores['emotional_resilience']} ball | {emotional_resilience}\n\n"
        f"{lang['self_regulation']}: {scores['self_regulation']} ball | {self_regulation}\n\n"
        f"{lang['scale_motivation']}: {scores['scale_motivation']} ball | {scale_motivation}\n\n"
        f"{lang['scale_resistance']}: {scores['scale_resistance']} ball | {scale_resistance}\n\n"
        f"{lang['q17']}: {q17}")

    return text

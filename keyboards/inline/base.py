from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from data.config import WEB_APP_URL
from keyboards.inline.callback_data import back_cb, language_cb, appointment_cb, lessons_cb, profile_cb, user_support_cb


def language_ikb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="🇺🇿 O'zbekcha", callback_data=language_cb.new(
                action="language", value="uz"
            )
        ),
        InlineKeyboardButton(
            text="🇷🇺 Русский", callback_data=language_cb.new(
                action="language", value="ru"
            )
        )
    )
    return kb


def main_ikb(lang: str) -> InlineKeyboardMarkup:
    texts = {
        "uz": {
            "test": "🧠 Test ishlash",
            "appointment": "📅 Qabulga yozilish",
            "lessons": "📚 Psixologik tayyorgarlik darslari",
            "portrait": "👤 Psixologik portret",
            "support": "🤖 Botga yozish"
        },
        "ru": {
            "test": "🧠 Пройти тест",
            "appointment": "📅 Записаться на прием",
            "lessons": "📚 Занятия по психологической подготовке",
            "portrait": "👤 Психологический портрет",
            "support": "🤖 Написать в бот",
        }
    }

    current = texts.get(lang, texts["uz"])

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(
            text=current["test"],
            web_app=WebAppInfo(url=f"{WEB_APP_URL}/home/?lang={lang}")
        ),
        InlineKeyboardButton(
            text=current["appointment"],
            callback_data=appointment_cb.new(action="appointment", lang=lang)
        ),
        InlineKeyboardButton(
            text=current["lessons"],
            callback_data=lessons_cb.new(action="lessons", lang=lang)
        ),
        InlineKeyboardButton(
            text=current["portrait"],
            callback_data=profile_cb.new(action="portrait", lang=lang)
        ),
        InlineKeyboardButton(
            text=current['support'], callback_data=user_support_cb.new(
                action="support", lang=lang
            )
        )
    )
    return kb


def back_ikb(lang: str, admin: bool = False) -> InlineKeyboardMarkup:
    texts = {
        "uz": "◀️ Ortga",
        "ru": "◀️ Назад",
    }

    kb = InlineKeyboardMarkup()
    if admin:
        page = "admin"
    else:
        page = "main"
    kb.add(
        InlineKeyboardButton(
            text=texts.get(lang, texts["uz"]),
            callback_data=back_cb.new(page=page, lang=lang)
        )
    )
    return kb

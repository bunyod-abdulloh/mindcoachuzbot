from aiogram.types import ReplyKeyboardMarkup

from locales.uz_locale import UZ_TEXTS


def language_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🇺🇿 O'zbekcha", "🇷🇺 Русский")
    return kb


def uz_main_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(UZ_TEXTS['menu_lessons'])
    kb.row(UZ_TEXTS['menu_test'], UZ_TEXTS['menu_appointment'])
    kb.row(UZ_TEXTS['menu_portret'])

    return kb

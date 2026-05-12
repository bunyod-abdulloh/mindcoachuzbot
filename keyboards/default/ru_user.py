from aiogram.types import ReplyKeyboardMarkup

from locales.ru_locale import RU_TEXTS


def ru_main_dkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(RU_TEXTS['menu_lessons'])
    kb.row(RU_TEXTS['menu_test'], RU_TEXTS['menu_appointment'])
    kb.row(RU_TEXTS['menu_portret'])

    return kb

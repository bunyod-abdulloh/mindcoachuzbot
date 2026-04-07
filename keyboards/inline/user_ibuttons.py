from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, LoginUrl

from data.config import WEB_APP_URL

WEBAPP_URL = f"{WEB_APP_URL}/bot/test/main/"

def key_returner_projects(items, current_page, all_pages):
    keys = InlineKeyboardMarkup(row_width=5)
    for item in items:
        keys.insert(
            InlineKeyboardButton(
                text=f"{item['rank']}",
                callback_data=f"projects:{item['id']}"
            )
        )
    keys.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=f"prev_projects:{current_page}"
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=f"alert_projects:{current_page}"
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=f"next_projects:{current_page}"
        )
    )
    return keys


def interviews_first_ibuttons(items, current_page, all_pages, selected):
    builder = InlineKeyboardMarkup(row_width=5)
    for item in items:
        if selected == item['sequence']:
            builder.insert(
                InlineKeyboardButton(
                    text=f"[ {item['sequence']} ]",
                    callback_data=f"select_projects:{item['id']}:{current_page}"
                )
            )
        else:
            builder.insert(
                InlineKeyboardButton(
                    text=f"{item['sequence']}",
                    callback_data=f"select_pts:{item['id']}:{current_page}"
                )
            )
    builder.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=f"prev_pts:{current_page}:{items[0]['id']}"
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=f"alert_pts:{current_page}"
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=f"next_pts:{current_page}:{items[0]['id']}"
        )
    )
    return builder



def gender_ikb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="🌺 Ayol", callback_data="female"
        ),
        InlineKeyboardButton(
            text="👤 Erkak", callback_data="male"
        )
    )
    return kb


def user_main_ikb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(
        text="🧑‍💻 Testlar | So'rovnomalar",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    )
    kb.add(
        InlineKeyboardButton(
            text="✍️ Qabulga yozilish", callback_data="doctor_appointment"
        )
    )
    kb.add(
        InlineKeyboardButton(
            text="🎙 Suhbat va loyihalar", callback_data="projects"
        )
    )
    kb.add(
        InlineKeyboardButton(
            text="👤 Shaxsiy kabinet", callback_data="personal_cabinet"
        )
    )
    return kb

def tests_page_ikb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(
        text="🚀 Testlar",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    )
    return kb


def check_user_data_ikb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="Qayta kiritish", callback_data="user_re-enter_data", style="danger"
        )
    )
    kb.add(
        InlineKeyboardButton(
            text="Tasdiqlash", callback_data="user_check_data", style="success"
        )
    )
    return kb

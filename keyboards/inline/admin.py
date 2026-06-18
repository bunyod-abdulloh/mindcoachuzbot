from distutils.command.install import value
from math import ceil

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import user_select_cb, users_page_cb, select_type_cb, on_off_cb, admin_support_cb
from loader import appdb


def search_type_ikb():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="1", callback_data=select_type_cb.new(
                action="search_type", value=1
            )
        ),
        InlineKeyboardButton(
            text="2", callback_data=select_type_cb.new(
                action="search_type", value=2
            )
        )
    )
    return kb


PAGE_SIZE = 15


async def users_pagination_ikb(page: int = 1) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)

    total_users = await appdb.get_count_athlets()
    total_pages = max(1, ceil(total_users / PAGE_SIZE))

    page = max(1, min(page, total_pages))
    offset = (page - 1) * PAGE_SIZE

    users = await appdb.get_users_page(limit=PAGE_SIZE, offset=offset)

    for user in users:
        kb.add(
            InlineKeyboardButton(
                text=user["full_name"],
                callback_data=user_select_cb.new(
                    id=user["telegram_id"],
                    page=page
                )
            )
        )

    nav_buttons = []

    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text="◀️ Oldingi",
                callback_data=users_page_cb.new(action="prev", page=page)
            )
        )

    nav_buttons.append(
        InlineKeyboardButton(
            text=f"{page}/{total_pages}",
            callback_data=users_page_cb.new(action="stay", page=page)
        )
    )

    if page < total_pages:
        nav_buttons.append(
            InlineKeyboardButton(
                text="Keyingi ▶️",
                callback_data=users_page_cb.new(action="next", page=page)
            )
        )

    kb.row(*nav_buttons)
    kb.add(
        InlineKeyboardButton(
            text="◀️ Ortga", callback_data="admin_back_search"
        )
    )
    return kb


def on_off_buttons():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="Yoqish", callback_data=on_off_cb.new(
                action="on_off", value="on"
            )
        ),
        InlineKeyboardButton(
            text="O'chirish", callback_data=on_off_cb.new(
                action="on_off", value="off"
            )
        )
    )
    kb.add(
        InlineKeyboardButton(
            text="◀️ Ortga", callback_data=on_off_cb.new(
                action="on_off", value="back"
            )
        )
    )
    return kb


def admin_support_ikb(telegram_id):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="Rad etish",
            callback_data=admin_support_cb.new(
                action="cancel", value=telegram_id
            ))
    ),
    InlineKeyboardButton(
        text="Javob berish",
        callback_data=admin_support_cb.new(
            action="answer", value=telegram_id
        )
    )
    return kb

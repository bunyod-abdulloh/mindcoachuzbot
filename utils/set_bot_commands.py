from aiogram.types import BotCommand, BotCommandScopeChat

from locales.ru_locale import RU_TEXTS
from locales.uz_locale import UZ_TEXTS

COMMANDS = {
    "uz": [
        BotCommand("start", UZ_TEXTS['commands']['start']),
        BotCommand("lang", UZ_TEXTS['commands']['lang']),
        BotCommand("cancel", UZ_TEXTS['commands']['cancel']),
        BotCommand("admin", "Admin panel")
    ],
    "ru": [
        BotCommand("start", RU_TEXTS['commands']['start']),
        BotCommand("lang", RU_TEXTS['commands']['lang']),
        BotCommand("cancel", RU_TEXTS['commands']['cancel']),
        BotCommand("admin", "Admin panel")
    ],
}


async def set_user_commands(bot, user_id: int, lang: str):
    commands = COMMANDS.get(lang, COMMANDS["uz"])
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeChat(chat_id=user_id),
    )
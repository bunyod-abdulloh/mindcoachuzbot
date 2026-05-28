from aiogram.utils.callback_data import CallbackData

# ================== USER ==================
language_cb = CallbackData("language", "action", "value")
profile_cb = CallbackData("profile", "action", "lang")
appointment_cb = CallbackData("appointment", "action", "lang")
lessons_cb = CallbackData("lessons", "action", "lang")
back_cb = CallbackData("back", "page", "lang")

# ================== ADMIN ==================
select_type_cb = CallbackData("select_type", "action", "value")
users_page_cb = CallbackData("users", "action", "page")
user_select_cb = CallbackData("user", "id", "page")
on_off_cb = CallbackData("on_off", "action", "value")

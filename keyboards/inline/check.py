from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup



check_button = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subs")
    ]]
)

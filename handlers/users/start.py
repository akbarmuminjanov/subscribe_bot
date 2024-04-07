from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import types
from data.config import CHANNELS
from loader import bot, dp
from keyboards.inline.check import check_button
from utils.check_member import check


# @dp.message_handler(CommandStart())
# async def bot_start(message: types.Message):
#     await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!")





@dp.message_handler(commands=['start'])
async def show_channels(message: types.Message):
    channels_format = str()
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        # logging.info(invite_link)
        channels_format += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"

    await message.answer(f"Quyidagi kanallarga obuna bo'ling: \n"
                         f"{channels_format}", reply_markup=check_button)
    



@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    for channel in CHANNELS:
        status = await check(user_id=call.from_user.id,
                                            channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            result += f" ✅<b>{channel.title}</b> kanaliga obuna bo'lgansiz!\n\n"
        else:
            invite_link = await channel.export_invite_link()
            result += (f"❌<b>{channel.title}</b> kanaliga obuna bo'lmagansiz. "
                        f"<a href='{invite_link}'>Obuna bo'ling</a>\n\n")

    await call.message.answer(result)
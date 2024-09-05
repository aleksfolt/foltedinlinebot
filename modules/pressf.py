import hashlib
import time

from aiogram import types, F
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import bot, dp

f_s = {}
user_clicks = {}

async def inline_f(inline_query: InlineQuery):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Press F", callback_data="f"))

    input_content = InputTextMessageContent(message_text="Press F to pay respect.")
    result_id = hashlib.md5("Press_F".encode()).hexdigest()

    item = InlineQueryResultArticle(
        id=result_id,
        type="article",
        title="Press F",
        input_message_content=input_content,
        thumbnail_url="https://tinypic.host/images/2024/09/01/DALLE-2024-09-01-03.32.12---A-detailed-3D-illustration-of-the-letter-F-on-a-dark-background.-The-letter-should-have-a-metallic-texture-with-a-sleek-and-polished-finish-giving.webp",
        reply_markup=builder.as_markup()
    )

    return item


async def ping_callback_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    current_time = time.time()

    if user_id in user_clicks and current_time - user_clicks[user_id] < 1:
        await callback_query.answer("Too fast...")
        return

    user_clicks[user_id] = current_time

    message_id = callback_query.inline_message_id

    if message_id not in f_s:
        f_s[message_id] = {}
    if user_id not in f_s[message_id]:
        f_s[message_id][user_id] = 1
    else:
        if f_s[message_id][user_id] == 1:
            f_s[message_id][user_id] = 0
        else:
            f_s[message_id][user_id] = 1

    count = sum(f_s[message_id].values())

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=f"{count} F's", callback_data="f"))

    await bot.edit_message_text(
        text=f"Press F to pay respect.",
        inline_message_id=message_id,
        reply_markup=builder.as_markup()
    )

def setup_tools_f(dp, bot):
    dp.callback_query(lambda c: c.data == 'f')(ping_callback_handler)

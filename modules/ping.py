import time
import hashlib
from aiogram import types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def inline_ping(inline_query: InlineQuery, bot):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Ping", callback_data="ping_all"))

    input_content = InputTextMessageContent(message_text="Test Ping")
    result_id = hashlib.md5("Test Ping".encode()).hexdigest()

    item = InlineQueryResultArticle(
        id=result_id,
        type="article",
        title="Test Ping",
        input_message_content=input_content,
        reply_markup=builder.as_markup()
    )

    await inline_query.answer([item])


async def ping_callback_handler(callback_query: types.CallbackQuery, bot):
    ping_start_time = time.time()

    await bot.answer_callback_query(callback_query.id, text="Pinging...")

    ping_end_time = time.time()
    ping_time = round((ping_end_time - ping_start_time) * 1000)
    print(callback_query)
    print(callback_query.message.message_id)

    await bot.edit_message_text(
        text=f"🌕\nPing: {ping_time} ms",
        message_id=callback_query.message.message_id
    )


def setup_tools_ping(dp, bot):
    dp.callback_query(lambda c: c.data == 'ping_all')(ping_callback_handler)

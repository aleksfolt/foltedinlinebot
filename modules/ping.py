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
    await bot.answer_callback_query(callback_query.id, text="Pinging...")

    if callback_query.message:
        ping_start_time = time.time()
        await bot.edit_message_text(
            text=f"🌕",  # Here was the issue
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id
        )
        ping_end_time = time.time()
        ping_time = round((ping_end_time - ping_start_time) * 1000)
        await bot.edit_message_text(
            text=f"Ping: {ping_time} ms",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id
        )
    elif callback_query.inline_message_id:
        ping_start_time = time.time()
        await bot.edit_message_text(
            text=f"🌕",  # Here was the issue
            inline_message_id=callback_query.inline_message_id
        )
        ping_end_time = time.time()
        ping_time = round((ping_end_time - ping_start_time) * 1000)
        await bot.edit_message_text(
            text=f"Ping: {ping_time} ms",
            inline_message_id=callback_query.inline_message_id
        )
    else:
        print("No valid message or inline message reference found.")


def setup_tools_ping(dp, bot):
    dp.callback_query(lambda c: c.data == 'ping_all')(ping_callback_handler)
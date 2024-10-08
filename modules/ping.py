import time
import hashlib
from aiogram import types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import config
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

logger.debug("Starting ping handler")


async def inline_ping(inline_query: InlineQuery):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Click", callback_data="ping_all"))

    input_content = InputTextMessageContent(message_text="⏳ Get InlineBot ping")
    result_id = hashlib.md5("Test Ping".encode()).hexdigest()

    item = InlineQueryResultArticle(
        id=result_id,
        type="article",
        title="Get Ping",
        thumbnail_url="https://tinypic.host/images/2024/09/01/DALLE-2024-09-01-01.16.21---A-detailed-and-artistic-illustration-of-a-moon-emoji-without-facial-features.-The-moon-should-have-a-soft-glowing-texture-with-subtle-craters-and-a-g.webp",
        input_message_content=input_content,
        description="Get inline bot ping",
        reply_markup=builder.as_markup()
    )

    return item


async def ping_callback_handler(callback_query: types.CallbackQuery, bot):
    allowed_user_id = config.AUTHORIZED_USER_ID

    if callback_query.from_user.id not in allowed_user_id:
        await bot.answer_callback_query(callback_query.id, text="You are not authorized to use this button.", show_alert=True)
        return

    await bot.answer_callback_query(callback_query.id, text="Pinging...")

    if callback_query.message:
        ping_start_time = time.time()
        await bot.edit_message_text(
            text=f"🌕",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id
        )
        ping_end_time = time.time()
        ping_time = round((ping_end_time - ping_start_time) * 1000)
        await bot.edit_message_text(
            text=f"🌒 Ping: {ping_time} ms",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id
        )
    elif callback_query.inline_message_id:
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="Click", callback_data="ping_all"))
        ping_start_time = time.time()
        await bot.edit_message_text(
            text=f"🌕", 
            inline_message_id=callback_query.inline_message_id
        )
        ping_end_time = time.time()
        ping_time = round((ping_end_time - ping_start_time) * 1000)
        await bot.edit_message_text(
            text=f"🌒 Ping: {ping_time} ms",
            inline_message_id=callback_query.inline_message_id,
            reply_markup=builder.as_markup()
        )
    else:
        print("No valid message or inline message reference found.")


def setup_tools_ping(dp, bot):
    dp.callback_query(lambda c: c.data == 'ping_all')(ping_callback_handler)
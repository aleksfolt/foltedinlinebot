from aiogram.enums import ParseMode
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import hashlib
from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from aiogram import types
from aiogram.filters import CommandStart, CommandObject

updates_router = Router()

async def inline_updates(inline_query: InlineQuery):
    message_text = "Click on the button below to see the latest update 👇."

    input_content = InputTextMessageContent(message_text=message_text, parse_mode=ParseMode.MARKDOWN)
    result_id = hashlib.md5(message_text.encode()).hexdigest()

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Click here.", url="https://t.me/foltedbot?start=update"))

    item = InlineQueryResultArticle(
        id=result_id,
        cache_time=0,
        title="Get Updates",
        description="Get inline bot updates",
        reply_markup=builder.as_markup(),
        thumbnail_url="https://tinypic.host/images/2024/09/03/DALLE-2024-09-03-04.32.39---A-minimalist-emoji-style-image-representing-an-update.-The-image-should-feature-an-icon-of-an-upward-arrow-combined-with-a-small-gear-symbol.-The-styl.webp",
        input_message_content=input_content,
    )

    return item


@updates_router.message(CommandStart())
async def handler_start_command(msg: Message, command: CommandObject):
    if command.args == "update":
        message_text = (
            "🆕 *Latest Updates:*\n\n"
            "1. *New Command Added:*\n"
            "   • `press f` - _Press F to pay respect_\n\n"
            "2. *Enhancements:*\n"
            "   • Added comments to `cb` command.\n"
            "   • Added images for each inline query result.\n\n"
            "Thanks for using! 😊"
        )
        await msg.answer(message_text, parse_mode=ParseMode.MARKDOWN)
    elif command.args == "help":
        message_text = (
            "*🔓 Available Modules*\n"
            "────────────────────────\n\n"
            "*📁 General Commands*\n"
            "• `help` - _Get help_\n"
            "• `ping` - _Check your ping_\n"
            "• `sysinfo` - _System information_\n"
            "• `calc <2+2>` - _Calculator_\n"
            "• `qr <link>` - _Generate QR code_\n\n"
            "*🔍 Search Commands*\n"
            "• `wiki <query>` - _Search in Wikipedia_\n"
            "• `duck <query>` - _Search in DuckDuckGo_\n"
            "• `wh <city>` - _Weather in city_\n"
            "• `url <url>` - _Shorten URL_\n"
            "• `pic <query>` - _Find an image_\n"
            "• `movie <name>` - _Movie/Film details_\n\n"
            "*🎉 Fun Commands*\n"
            "• `ily` - _TikTok animation_\n"
            "• `cb <asset> <amount>` - _Fake @send check_\n"
            "• `press f` - _Press F to pay respect_\n\n"
            "*🔐 Utility Commands*\n"
            "• `rdr <link>` - _Check link for redirects_\n"
            "• `tr <source lang> <target lang> <query>` - _Translate text_\n"
            "• `yt <video name>` - _Search on YouTube_\n"
            "────────────────────────"
        )
        await msg.answer(message_text, parse_mode=ParseMode.MARKDOWN)

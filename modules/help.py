from aiogram.enums import ParseMode
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import hashlib

async def inline_help(inline_query: InlineQuery):
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

    input_content = InputTextMessageContent(message_text=message_text, parse_mode=ParseMode.MARKDOWN)
    result_id = hashlib.md5("System Information".encode()).hexdigest()

    item = InlineQueryResultArticle(
        id=result_id,
        cache_time=0,
        title="Get Help",
        description="Get inline bot help",
        thumbnail_url="https://tinypic.host/images/2024/09/01/DALLE-2024-09-01-01.19.55---A-highly-detailed-and-realistic-illustration-of-a-dark-metallic-gear-cogwheel-perfectly-centered-on-a-very-dark-blue-almost-black-background.-The-g.webp",
        input_message_content=input_content,
    )

    return item

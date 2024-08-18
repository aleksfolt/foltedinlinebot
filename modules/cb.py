from aiogram import types
from aiogram.types import InlineQueryResultPhoto, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton


async def inline_photo_with_caption_and_button(inline_query, bot):
    photo_url = "https://tinypic.host/images/2024/08/18/IMG_0546.jpeg"
    caption = "🦋 [Чек](https://t.me/CryptoBotRU/23) на *10 USDT ($10)*."
    
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Получить 10 USDT", url="https://t.me/CryptoBotRU/23")
    keyboard.add(button)

    result_id = inline_query.id
    input_content = InputTextMessageContent(message_text=caption, parse_mode="Markdown")

    item = InlineQueryResultPhoto(
        id=result_id,
        photo_url=photo_url,
        thumb_url=photo_url,
        caption=caption,
        reply_markup=keyboard,
        input_message_content=input_content
    )

    await inline_query.answer([item], cache_time=0)
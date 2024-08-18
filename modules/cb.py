from aiogram import types
from aiogram.types import InputFile, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton

async def send_photo_with_caption_and_button(message: types.Message, bot):
    photo_url = "https://tinypic.host/images/2024/08/18/IMG_0546.jpeg"
    caption = "🦋 [Чек](https://t.me/CryptoBotRU/23) на *10 USDT ($10)*."
    
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Получить 10 USDT", url="https://t.me/CryptoBotRU/23")
    keyboard.add(button)

    await message.reply_photo(
        photo=photo_url,
        caption=caption,
        reply_markup=keyboard,
        parse_mode="Markdown",
        cache_time=0
    )

def setup_tools_kb(dp):
    dp.message_handler(commands=['kb'])(send_photo_with_caption_and_button)
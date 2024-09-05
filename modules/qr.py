import asyncio
from aiogram import types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto
import hashlib

async def inline_qr(inline_query: InlineQuery):
    query_text = inline_query.query.strip()

    if query_text.startswith("qr "):
        query_text_after_qr = query_text[3:].strip()
    else:
        query_text_after_qr = query_text

    base_url = f"qr.crypt.bot/?url={query_text_after_qr}"
    
    input_content = InputTextMessageContent(message_text=f"Your QR Code: {base_url}")
    
    result_id = hashlib.md5(base_url.encode()).hexdigest()

    item = InlineQueryResultPhoto(
        id=result_id,
        cache_time=0,
        photo_url=base_url,
        thumbnail_url=base_url,
        title="Qr code generator",
    )
    
    return item
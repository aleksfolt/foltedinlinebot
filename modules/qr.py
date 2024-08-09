import asyncio
from aiogram import types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import hashlib

async def inline_qr(inline_query: InlineQuery):
    query_text = inline_query.query.strip()
    
    if query_text.startswith("qr "):
        query_text_after_qr = query_text[3:].strip()
    else:
        query_text_after_qr = query_text

    base_url = "https://api.qrserver.com/v1/create-qr-code/"
    params = {
        "size": "300x300",
        "data": query_text_after_qr
    }
    qr_code_url = f"{base_url}?size={params['size']}&data={params['data']}"
    
    input_content = InputTextMessageContent(message_text=f"Your QR Code: {qr_code_url}")
    
    result_id = hashlib.md5(qr_code_url.encode()).hexdigest()
    
    item = InlineQueryResultArticle(
        id=result_id,
        type="article",
        title="QR Code Generator",
        input_message_content=input_content
    )
    
    await inline_query.answer([item])
    
def setup_tools_qr(dp):
    dp.inline_query(inline_qr)
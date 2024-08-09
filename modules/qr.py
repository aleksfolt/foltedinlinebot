import asyncio 
from aiogram import types 
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests
import hashlib

async def inline_qr(inline_query: InlineQuery):
     _, query_text = query_text.split(maxsplit=1)
    
    base_url= "https://api.qrserver.com/v1/create-qr-code/"
    params= {
        "size": "300x300",
        "data": query_text
    }
    qr_code_url=f"{base_url}?size={params['size']}&data={params['data']}"
    
    input_content = InputTextMessageContent(message_text=f"Your Qr: {qr_code_url}")
    
    result_id= hashlib.md5(qr_code_url.encode()).hexdigest()
    
    item=InlineQueryResultArticle(
        id=result_id,
        type="article",
        title="QrCode Generator",
        input_message_content=input_content
    )
    
    await inline_query.answer([item])
    
    
def setup_tools_qr(dp):
    dp.inline_query(inline_qr)
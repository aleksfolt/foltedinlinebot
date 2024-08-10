import asyncio
from aiogram import types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import hashlib
import requests

async def inline_tinyurl(inline_query: InlineQuery):
    query_text = inline_query.query.strip()

    long_url = query_text[4:].strip()

    base_url = "http://tinyurl.com/api-create.php"
    params = {
        "url": long_url
    }
    response = requests.get(base_url, params=params)
    short_url = response.text
    input_content = InputTextMessageContent(message_text=f"Your shortened URL: {short_url}")
    result_id = hashlib.md5(short_url.encode()).hexdigest()

    item = InlineQueryResultArticle(
        id=result_id,
        type="article",
        title="URL Shortener (TinyURL)",
        input_message_content=input_content
    )
    await inline_query.answer([item])

def setup_tools_tinyurl(dp):
    dp.inline_query(inline_tinyurl)
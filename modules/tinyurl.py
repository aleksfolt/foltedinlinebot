import asyncio
from aiogram import types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import hashlib
import requests

async def shorten_url_tinyurl(long_url: str) -> str:
    api_url = f"http://tinyurl.com/api-create.php?url={long_url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.text
    else:
        return None

async def inline_tinyurl(inline_query: InlineQuery):
    query_text = inline_query.query.strip()

    long_url = query_text[4:].strip()

    response_text = await shorten_url_tinyurl(long_url)

    if response_text is None:
        response_text = "Error: Unable to shorten the URL"

    input_content = InputTextMessageContent(message_text=f"Your shortened URL: {response_text}")
    result_id = hashlib.md5(response_text.encode()).hexdigest()

    item = InlineQueryResultArticle(
        id=result_id,
        cache_time=0,
        type="article",
        title="URL Shortener (TinyURL)",
        thumbnail_url="https://tinypic.host/images/2024/09/01/DALLE-2024-09-01-03.34.04---A-highly-detailed-and-realistic-illustration-of-a-chain-link-emoji-on-a-dark-background.-The-chain-links-should-be-metallic-with-a-glossy-reflective.webp",
        input_message_content=input_content
    )
    await inline_query.answer([item])


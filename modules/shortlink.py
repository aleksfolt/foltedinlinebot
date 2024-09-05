import asyncio
import hashlib
import aiohttp
from aiogram import types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

async def check_redirect(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, allow_redirects=False) as response:
                if 300 <= response.status < 400:
                    return f"Redirect detected from {url} to {response.headers['Location']}"
                else:
                    return f"No redirect for {url}"
    except aiohttp.ClientError as e:
        return f"Error checking {url}: {e}"

async def inline_redirect(inline_query: InlineQuery):
    query_text = inline_query.query.strip()
    _, search_query = query_text.split(maxsplit=1)

    redirect_info = await check_redirect(search_query)

    input_content = InputTextMessageContent(message_text=redirect_info)
    result_id = hashlib.md5(redirect_info.encode()).hexdigest()

    item = InlineQueryResultArticle(
        id=result_id,
        type="article",
        title=redirect_info,
        thumbnail_url="https://tinypic.host/images/2024/09/01/DALLE-2024-09-01-03.34.04---A-highly-detailed-and-realistic-illustration-of-a-chain-link-emoji-on-a-dark-background.-The-chain-links-should-be-metallic-with-a-glossy-reflective.webp",
        input_message_content=input_content
    )

    return item
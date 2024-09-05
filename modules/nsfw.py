import asyncio
import hashlib
from aiogram import types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import aiohttp

async def check_redirection(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, allow_redirects=False) as response:
            if 300 <= response.status < 400:
                redirect_url = response.headers.get('Location')
                if '/pornstars' in redirect_url:
                    return True
            return False

async def inline_nswf(inline_query: InlineQuery):
    query_text = inline_query.query.strip()
    _, search_query = query_text.split(maxsplit=1)

    search_query = search_query.replace(' ', '-')
    get_model = f"https://rt.pornhub.com/model/{search_query}"

    if await check_redirection(get_model):
        input_content = InputTextMessageContent(message_text="Модель не найдена.")
        result_id = hashlib.md5("not_found".encode()).hexdigest()

        item = InlineQueryResultArticle(
            id=result_id,
            type="article",
            title="Модель не найдена",
            input_message_content=input_content
        )
    else:
        input_content = InputTextMessageContent(message_text=f"Model: {get_model}")
        result_id = hashlib.md5(get_model.encode()).hexdigest()

        item = InlineQueryResultArticle(
            id=result_id,
            cache_time=0,
            type="article",
            title="PornHub Model",
            input_message_content=input_content
        )

    return item


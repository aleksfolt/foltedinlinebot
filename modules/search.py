import hashlib
import logging
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from duckduckgo_search import AsyncDDGS

logging.basicConfig(level=logging.INFO)

async def inline_search(inline_query: InlineQuery):
    query_text = inline_query.query.lower()
    logging.info(f"Received query: {query_text}")

    if ' ' not in query_text:
        logging.warning("No search query provided.")
        await inline_query.answer([], cache_time=0)
        return

    try:
        _, search_query = query_text.split(maxsplit=1)
    except ValueError:
        logging.warning("Failed to split query. No search query provided.")
        await inline_query.answer([], cache_time=0)
        return

    async with AsyncDDGS() as ddgs:
        try:
            results = await ddgs.text(search_query, max_results=15)
        except Exception as e:
            logging.error(f"Error while searching: {e}")
            await inline_query.answer([], cache_time=0)
            return

    articles = []
    for result in results:
        result_id = hashlib.md5(result["title"].encode()).hexdigest()
        item = InlineQueryResultArticle(
            id=result_id,
            type="article",
            title=result["title"],
            input_message_content=InputTextMessageContent(
                message_text=f"{result['title']}\n{result['href']}"
            )
        )
        articles.append(item)

    await inline_query.answer(articles, cache_time=0)

def setup_tools_search(dp):
    pass
import hashlib
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from duckduckgo_search import AsyncDDGS


async def inline_search(inline_query: InlineQuery):
    query_text = inline_query.query.lower()
    _, search_query = query_text.split(maxsplit=1)
    async with AsyncDDGS() as ddgs:
        results = ddgs.text(search_query, max_results=15)

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

    await inline_query.answer(articles)


def setup_tools_search(dp):
    pass

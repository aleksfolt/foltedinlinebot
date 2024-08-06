import hashlib
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='foltuserbot/1.0'
    )


async def inline_wiki(inline_query: InlineQuery):
    query_text = inline_query.query.lower()
    _, search_query = query_text.split(maxsplit=1)
    page = wiki_wiki.page(search_query)

    articles = []
    if page.exists():
        summary = page.summary[:300]
        result_id = hashlib.md5(page.title.encode()).hexdigest()
        item = InlineQueryResultArticle(
            id=result_id,
            type="article",
            title=page.title,
            input_message_content=InputTextMessageContent(
                message_text=f"{page.title}\n\n{summary}\n\nRead more: {page.fullurl}"
            )
        )
        articles.append(item)

    await inline_query.answer(articles)


def setup_tools_wiki(dp):
    dp.inline_query(inline_wiki)

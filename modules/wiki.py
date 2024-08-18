import logging
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import wikipediaapi
import hashlib

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='foltuserbot/1.0'
)

async def inline_wiki(inline_query: InlineQuery):
    query_text = inline_query.query.lower()
    try:
        _, search_query = query_text.split(maxsplit=1)
    except ValueError as e:
        logger.error("Ошибка разбиения запроса: %s", e)
        return  # Останавливаем обработку, если запрос неправильный

    logger.info("Поиск в Википедии по запросу: %s", search_query)
    page = wiki_wiki.page(search_query)

    articles = []
    if page.exists():
        summary = page.summary[:300]
        result_id = hashlib.md5(page.title.encode()).hexdigest()
        item = InlineQueryResultArticle(
            id=result_id,
            title=page.title,
            input_message_content=InputTextMessageContent(
                message_text=f"{page.title}\n\n{summary}\n\nRead more: {page.fullurl}"
            )
        )
        articles.append(item)
        logger.info("Страница найдена: %s", page.title)
    else:
        logger.info("Страница не найдена: %s", search_query)

    await inline_query.answer(articles)
    logger.info("Ответ отправлен пользователю")
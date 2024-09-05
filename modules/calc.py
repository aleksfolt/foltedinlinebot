import logging
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import hashlib
from sympy import sympify
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

operation_pattern = re.compile(r'^[\d+\-*/\(\)]+$')
max_number = 10 ** 6


def is_expression_safe(expression):
    if '**' in expression:
        return False

    numbers = re.findall(r'\d+', expression)
    for number in numbers:
        if int(number) > max_number:
            return False
    return True


async def inline_calculator(inline_query: InlineQuery):
    query_text = inline_query.query.replace(" ", "")
    if not query_text:
        return

    if query_text.startswith("calc"):
        query_text = query_text[4:]

    if not operation_pattern.match(query_text):
        logger.warning("Недопустимая операция: %s", query_text)
        return

    if not is_expression_safe(query_text):
        logger.warning("Небезопасное выражение или слишком большое число: %s", query_text)
        result_text = f"🔢 Запрос: {query_text}\n📊 Результат: Выражение недопустимо или слишком велико для обработки."
        result_id = hashlib.md5(query_text.encode()).hexdigest()

        item = InlineQueryResultArticle(
            id=result_id,
            title="Ошибка: недопустимое выражение",
            input_message_content=InputTextMessageContent(
                message_text=result_text
            )
        )
        return item

    try:
        result = sympify(query_text)
        result_text = f"🔢 Запрос: {query_text}\n📊 Результат: {result}"

        logger.info("Вычислен результат: %s", result_text)

        result_id = hashlib.md5(query_text.encode()).hexdigest()

        item = InlineQueryResultArticle(
            id=result_id,
            title=f"{query_text} = {result}",
            input_message_content=InputTextMessageContent(
                message_text=result_text
            ),
            thumbnail_url="https://tinypic.host/images/2024/09/01/image-removebg-preview.png"
        )

        return item
    except Exception as e:
        logger.error("Ошибка вычисления: %s", e)
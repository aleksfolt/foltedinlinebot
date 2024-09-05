from mtranslate import translate
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import hashlib

async def inline_translate(inline_query: InlineQuery):
    query_text = inline_query.query.strip()

    print(f"Полный текст запроса: {query_text}")

    if not query_text.startswith("tr "):
        await inline_query.answer([
            InlineQueryResultArticle(
                id="error",
                cache_time=0,
                title="Error",
                input_message_content=InputTextMessageContent(
                    message_text="Используйте формат: tr RU EN привет"
                )
            )
        ])
        return

    query_text = query_text[3:].strip().split(maxsplit=2)

    print(f"Разделённый текст запроса: {query_text}")

    if len(query_text) != 3:
        await inline_query.answer([
            InlineQueryResultArticle(
                id="error",
                cache_time=0,
                title="Error",
                input_message_content=InputTextMessageContent(
                    message_text="Пожалуйста, используйте формат: RU EN привет"
                )
            )
        ])
        return

    source_lang, target_lang, text_to_translate = query_text

    try:
        translated_text = translate(text_to_translate, target_lang.lower(), source_lang.lower())
        print(translated_text)
    except Exception as e:
        await inline_query.answer([
            InlineQueryResultArticle(
                id="error",
                cache_time=0,
                title="Error",
                input_message_content=InputTextMessageContent(
                    message_text=f"Ошибка перевода: {str(e)}"
                )
            )
        ])
        return

    result_id = hashlib.md5(text_to_translate.encode()).hexdigest()

    translation_message = (
        f"🔠 *Перевод*\n\n"
        f"Оригинал: {text_to_translate}\n"
        f"Перевод: {translated_text}"
    )

    item = InlineQueryResultArticle(
        id=result_id,
        cache_time=0,
        type="article",
        title=f"Перевод: {source_lang.upper()} ➡️ {target_lang.upper()}",
        input_message_content=InputTextMessageContent(
            message_text=translation_message,
            parse_mode="Markdown"
        ),
        thumbnail_url="https://tinypic.host/images/2024/09/01/DALLE-2024-09-01-03.40.54---An-emoji-style-illustration-of-the-text-EN-RU.-The-text-should-be-bold-and-colorful-with-a-smooth-glossy-finish-to-resemble-a-high-quality-emoji..webp"
    )

    return item
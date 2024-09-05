import asyncio
import requests
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import hashlib

import config

async def inline_movie(inline_query: InlineQuery):
    query_text = inline_query.query.strip()

    if query_text.startswith("movie "):
        movie_name = query_text[6:].strip()
    else:
        movie_name = query_text

    url = f"http://www.omdbapi.com/?s={movie_name}&apikey={config.MOVIE_API}"
    response = requests.get(url)
    movie_data = response.json()

    results = []

    if movie_data.get("Search"):
        for movie in movie_data["Search"][:10]:
            title = movie.get("Title")
            year = movie.get("Year")
            poster = movie.get("Poster", "")
            imdb_id = movie.get("imdbID")

            details_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={config.MOVIE_API}"
            details_response = requests.get(details_url)
            details_data = details_response.json()

            info = details_data.get("Plot")
            genre = details_data.get("Genre")
            language = details_data.get("Language")
            country = details_data.get("Country")
            runtime = details_data.get("Runtime")

            input_content = InputTextMessageContent(
                message_text=(
                    f"🎬 ```Movie\n{title}```\n\n"
                    f"🎞️ *Movie Info*\n{info}\n\n"
                    f"😀️ *Genre:* {genre}\n"
                    f"🗣️ *Language:* {language}\n"
                    f"🌍 *Country:* {country}\n"
                    f"🗓️ *Release Date:* {year}\n"
                    f"⏳️ *Running time:* {runtime}\n"
                    f"©️ *Poster:* [Poster]({poster})"
                ),
                parse_mode=ParseMode.MARKDOWN
            )

            result_id = hashlib.md5(f"{title}{year}".encode()).hexdigest()

            item = InlineQueryResultArticle(
                id=result_id,
                cache_time=0,
                type="article",
                title=f"{title} ({year})",
                thumbnail_url=poster if poster != "N/A" else None,
                input_message_content=input_content
            )

            results.append(item)

    return results
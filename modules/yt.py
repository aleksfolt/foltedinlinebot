import requests
from aiogram import types
from aiogram.types import InlineQuery, InlineQueryResultVideo, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
import hashlib

from aiogram.utils.keyboard import InlineKeyboardBuilder

import config

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"

def format_view_count(view_count):
    view_count = int(view_count)
    if view_count >= 1_000_000_000:
        return f"{view_count / 1_000_000_000:.1f}B"
    elif view_count >= 1_000_000:
        return f"{view_count / 1_000_000:.1f}M"
    elif view_count >= 1_000:
        return f"{view_count / 1_000:.1f}K"
    return str(view_count)

async def inline_youtube_search(inline_query: InlineQuery):
    query_text = inline_query.query.strip()

    print(f"Полный текст запроса: {query_text}")

    if not query_text.startswith("yt "):
        await inline_query.answer([
            InlineQueryResultVideo(
                id="error",
                cache_time=0,
                title="Error",
                input_message_content=InputTextMessageContent(
                    message_text="Используйте формат: yt запрос"
                ),
                video_url="",
                mime_type="text/html",
                thumbnail_url=""
            )
        ])
        return

    search_query = query_text[3:].strip()

    search_params = {
        "part": "snippet",
        "q": search_query,
        "key": config.YOUTUBE_API_KEY,
        "type": "video",
        "maxResults": 10
    }

    try:
        search_response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
        search_response.raise_for_status()
        search_results = search_response.json()

        items = []
        for item in search_results.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            description = item["snippet"]["description"]
            thumbnail_url = item["snippet"]["thumbnails"]["high"]["url"]

            video_params = {
                "part": "statistics",
                "id": video_id,
                "key": config.YOUTUBE_API_KEY
            }
            video_response = requests.get(YOUTUBE_VIDEO_URL, params=video_params)
            video_response.raise_for_status()
            video_data = video_response.json()

            view_count = video_data["items"][0]["statistics"].get("viewCount", "N/A")
            formatted_view_count = format_view_count(view_count)

            result_id = hashlib.md5(video_id.encode()).hexdigest()

            builder = InlineKeyboardBuilder()
            builder.row(InlineKeyboardButton(text="Show Description", callback_data=f"show_desc_{video_id}"))

            item = InlineQueryResultVideo(
                id=result_id,
                cache_time=0,
                title=title,
                input_message_content=InputTextMessageContent(
                    message_text=f"{url}"
                ),
                video_url=url,
                mime_type="text/html",
                thumbnail_url=thumbnail_url,
                description=f"Просмотры: {formatted_view_count}",
                reply_markup=builder.as_markup()
            )
            items.append(item)

        if not items:
            return ([
                InlineQueryResultVideo(
                    id="no_results",
                    cache_time=0,
                    title="No results",
                    input_message_content=InputTextMessageContent(
                        message_text="Не удалось найти видео."
                    ),
                    video_url="",
                    mime_type="text/html",
                    thumbnail_url=""
                )
            ])
        else:
            return items

    except Exception as e:
        return ([
            InlineQueryResultVideo(
                id="error",
                cache_time=0,
                title="Error",
                input_message_content=InputTextMessageContent(
                    message_text=f"Ошибка поиска на YouTube: {str(e)}"
                ),
                video_url="",
                mime_type="text/html",
                thumbnail_url=""
            )
        ])

async def show_description_callback_handler(callback_query: types.CallbackQuery, bot):
    video_id = callback_query.data.split("_")[-1]

    video_params = {
        "part": "snippet",
        "id": video_id,
        "key": config.YOUTUBE_API_KEY
    }
    video_response = requests.get(YOUTUBE_VIDEO_URL, params=video_params)
    video_response.raise_for_status()
    video_data = video_response.json()

    description = video_data["items"][0]["snippet"]["description"]

    if len(description) > 200:
        description = description[:200] + "..."

    await bot.answer_callback_query(callback_query.id, text=description, show_alert=True)

def setup_tools_youtube(dp, bot):
    dp.callback_query(lambda c: c.data.startswith('show_desc_'))(show_description_callback_handler)

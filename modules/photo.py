import hashlib
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import InlineQuery, InlineQueryResultPhoto
import config

def get_images_by_query(query):
    url = 'https://api.unsplash.com/search/photos'
    params = {
        'query': query,
        'client_id': config.UNSPLASH_ACCESS_KEY,
        'per_page': 30,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        return []

async def show_user_images(inline_query: InlineQuery):
    query = inline_query.query.strip()

    if not query:
        return

    images = get_images_by_query(query)
    results = []

    for index, image in enumerate(images):
        photo_url = image['urls']['regular']
        thumb_url = image['urls']['thumb']

        results.append(
            InlineQueryResultPhoto(
                id=str(index),
                cache_time=0,
                photo_url=photo_url,
                thumbnail_url=thumb_url,
                title=image.get('description', 'Image'),
            )
        )

    return results
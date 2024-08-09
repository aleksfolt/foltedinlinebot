import requests
import hashlib
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import config


async def inline_weather(inline_query: InlineQuery):
    query_text = inline_query.query.lower()
    print(".")
    _, city = query_text.split(maxsplit=1)
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.WEATHER_API_KEY}")
    weather_data = response.json()
    weather_desc = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"] - 273.15
    result_id = hashlib.md5(city.encode()).hexdigest()

    item = InlineQueryResultArticle(
        id=result_id,
        type="article",
        title=f"Weather in {city}",
        input_message_content=InputTextMessageContent(
            message_text=f"Weather in {city}: {weather_desc}, {temp:.2f}°C")
    )

    await inline_query.answer([item])


def setup_tools_weather(dp):
    dp.inline_query(inline_weather)

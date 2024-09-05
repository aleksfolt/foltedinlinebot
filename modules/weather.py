import requests
import hashlib
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import config
from datetime import datetime


async def inline_weather(inline_query: InlineQuery):
    query_text = inline_query.query.lower()
    print(".")
    _, city = query_text.split(maxsplit=1)
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.WEATHER_API_KEY}")
    weather_data = response.json()

    if "weather" not in weather_data or len(weather_data["weather"]) == 0:
        await inline_query.answer([
            InlineQueryResultArticle(
                id="error",
                title="Error",
                input_message_content=InputTextMessageContent(
                    message_text="Weather data not available."
                )
            )
        ])
        return

    weather_desc = weather_data["weather"][0]["description"].capitalize()
    temp = weather_data["main"]["temp"] - 273.15
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]

    sunrise_time = datetime.fromtimestamp(weather_data["sys"]["sunrise"]).strftime('%H:%M:%S')
    sunset_time = datetime.fromtimestamp(weather_data["sys"]["sunset"]).strftime('%H:%M:%S')

    result_id = hashlib.md5(city.encode()).hexdigest()

    weather_message = (
        f"🌆 *Weather in {city.capitalize()}*\n\n"
        f"🌡 Temperature: {temp:.2f}°C\n"
        f"🌧 Description: {weather_desc}\n"
        f"💧 Humidity: {humidity}%\n"
        f"💨 Wind speed: {wind_speed} m/s\n"
        f"🌅 Sunrise: {sunrise_time}\n"
        f"🌇 Sunset: {sunset_time}"
    )

    item = InlineQueryResultArticle(
        id=result_id,
        type="article",
        title=f"Weather in {city.capitalize()}",
        input_message_content=InputTextMessageContent(
            message_text=weather_message,
            parse_mode="Markdown"
        ),
        description=f"🌡 Temperature: {temp:.2f}°C",
        thumbnail_url="https://tinypic.host/images/2024/09/01/DALLE-2024-09-01-03.38.06---An-emoji-style-illustration-of-mountains-with-a-lake.-The-mountains-should-have-simple-rounded-shapes-with-a-gradient-of-green-and-brown-and-white-s.webp"
    )

    return item

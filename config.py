import json
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
AUTHORIZED_USER_ID = json.loads(os.getenv('AUTHORIZED_USER_ID', '[]'))
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
MOVIE_API = os.getenv("MOVIE_API")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
EXCHANGE_KEY = os.getenv("EXCHANGE_KEY")

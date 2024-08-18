import psutil
import platform
import requests
from aiogram.enums import ParseMode
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import hashlib


def get_system_info():
    ram = psutil.virtual_memory()
    ram_total = ram.total / (1024 ** 3)
    ram_used = ram.used / (1024 ** 3)
    ram_percent = ram.percent

    system = platform.system()
    release = platform.release()
    version = platform.version()

    return ram_total, ram_used, ram_percent, system, release, version


def get_country():
    try:
        ip_response = requests.get('https://api.ipify.org?format=json')
        ip = ip_response.json().get('ip')

        if ip:
            country_response = requests.get(f'https://ipinfo.io/{ip}/json')
            country = country_response.json().get('country')
            return country
        else:
            return None
    except requests.RequestException as e:
        print(f"Ошибка получения информации: {e}")
        return None


async def inline_system_info(inline_query: InlineQuery):
    ram_total, ram_used, ram_percent, system, release, version = get_system_info()
    country = get_country()

    message_text = (
        f"*System Information*\n"
        f"    RAM: {ram_used:.2f} / {ram_total:.2f} GB ({ram_percent}%)\n"
        f"    System: {system}\n"
        f"    Release: {release}\n"
    )

    if country:
        message_text += f"    Country: {country}\n"
    else:
        message_text += "    Country information could not be retrieved."

    message_text = message_text.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]') \
                               .replace('(', '\\(').replace(')', '\\)').replace('~', '\\~').replace('`', '\\`') \
                               .replace('>', '\\>').replace('#', '\\#').replace('+', '\\+').replace('-', '\\-') \
                               .replace('=', '\\=').replace('|', '\\|').replace('{', '\\{').replace('}', '\\}') \
                               .replace('.', '\\.').replace('!', '\\!')

    input_content = InputTextMessageContent(message_text=message_text, parse_mode=ParseMode.MARKDOWN_V2)
    result_id = hashlib.md5("System Information".encode()).hexdigest()

    item = InlineQueryResultArticle(
        id=result_id,
        cache_time=0,
        title="System Information",
        input_message_content=input_content
    )

    await inline_query.answer([item])
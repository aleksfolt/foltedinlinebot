import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from modules.sysinfo import inline_system_info
from modules.ilyy import inline_ily, heart_animation
from modules.search import inline_search, setup_tools_search
from modules.weather import inline_weather, setup_tools_weather
from modules.wiki import inline_wiki, setup_tools_wiki
from modules.ping import inline_ping, setup_tools_ping

API_TOKEN = '7444946939:AAGzQG_Qega-XtJRcr50y4r2ndMhzbXen3Q'
AUTHORIZED_USER_ID = 6184515646

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.inline_query()
async def inline_handler(inline_query: types.InlineQuery):
    user_id = inline_query.from_user.id
    if user_id != AUTHORIZED_USER_ID:
        await inline_query.answer(
            results=[],
            cache_time=0,
            switch_pm_text="Unauthorized user",
            switch_pm_parameter="start"
        )
        return

    query_text = inline_query.query.lower()
    print(query_text)

    if query_text.startswith("wh"):
        await inline_weather(inline_query)
    elif query_text.startswith("duck"):
        await inline_search(inline_query)
    elif query_text.startswith("wiki"):
        await inline_wiki(inline_query)
    elif query_text.startswith("ping"):
        await inline_ping(inline_query, bot)
    elif query_text == "ily":
        await inline_ily(inline_query)
    elif query_text.startswith("sysinfo"):
        await inline_system_info(inline_query)


@dp.chosen_inline_result()
async def chosen_inline_result_handler(chosen_inline_result: types.ChosenInlineResult):
    inline_message_id = chosen_inline_result.inline_message_id
    query = chosen_inline_result.query.lower()

    if query == "ily":
        await heart_animation(bot, inline_message_id)


if __name__ == "__main__":
    setup_tools_weather(dp)
    setup_tools_search(dp)
    setup_tools_wiki(dp)
    setup_tools_ping(dp, bot)
    dp.run_polling(bot)

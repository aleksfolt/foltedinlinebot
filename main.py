import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from modules.calc import inline_calculator
from modules.help import inline_help
from modules.movie import inline_movie
from modules.nsfw import inline_nswf
from modules.pressf import inline_f, setup_tools_f
from modules.sysinfo import inline_system_info
from modules.ilyy import inline_ily, heart_animation
from modules.search import inline_search
from modules.translator import inline_translate
from modules.weather import inline_weather
from modules.wiki import inline_wiki
from modules.ping import inline_ping, setup_tools_ping
from modules.qr import inline_qr
from modules.tinyurl import inline_tinyurl
from modules.cb import inline_photo_with_caption_and_button, cb_animation
from modules.shortlink import inline_redirect
from modules.photo import show_user_images
from modules.updates import inline_updates, updates_router
import config
from modules.yt import inline_youtube_search, setup_tools_youtube

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.inline_query()
async def inline_handler(inline_query: types.InlineQuery):
    global item
    user_id = inline_query.from_user.id
    if user_id not in config.AUTHORIZED_USER_ID:
        await inline_query.answer(
            results=[],
            cache_time=0,
            switch_pm_text="Unauthorized user",
            switch_pm_parameter="start"
        )
        return

    query_text = inline_query.query.lower()
    print(query_text)

    if query_text == "":
        results = []
        results.append(await inline_ping(inline_query))
        results.append(await inline_help(inline_query))
        results.append(await inline_updates(inline_query))

        await inline_query.answer(results, cache_time=0)
        return

    if query_text.startswith("wh"):
        item = await inline_weather(inline_query)
    elif query_text.startswith("duck"):
        item = await inline_search(inline_query)
    elif query_text.startswith("wiki"):
        item = await inline_wiki(inline_query)
    elif query_text == "ping":
        item = await inline_ping(inline_query)
    elif query_text == "ily":
        item = await inline_ily(inline_query)
    elif query_text == "sysinfo":
        item = await inline_system_info(inline_query)
    elif query_text.startswith("qr"):
        item = await inline_qr(inline_query)
    elif query_text.startswith("url"):
        item = await inline_tinyurl(inline_query)
    elif query_text == "help":
        item = await inline_help(inline_query)
    elif query_text.startswith("porn"):
        item = await inline_nswf(inline_query)
    elif query_text.startswith("movie"):
        item = await inline_movie(inline_query)
    elif query_text.startswith("cb"):
        item = await inline_photo_with_caption_and_button(inline_query, bot)
    elif query_text.startswith("pic"):
        item = await show_user_images(inline_query)
    elif query_text.startswith("rdr"):
        item = await inline_redirect(inline_query)
    elif query_text.startswith("tr"):
        item = await inline_translate(inline_query)
    elif query_text.startswith("yt"):
        item = await inline_youtube_search(inline_query)
    elif query_text.startswith("calc"):
        item = await inline_calculator(inline_query)
    elif query_text == "press f":
        item = await inline_f(inline_query)
    elif query_text == "update":
        item = await inline_updates(inline_query)
    else:
        await inline_query.answer(
            results=[],
            cache_time=0,
            switch_pm_text="Command not found",
            switch_pm_parameter="help"
        )
        return

    try:
        await inline_query.answer(item, cache_time=0)
    except Exception:
        await inline_query.answer([item], cache_time=0)


@dp.chosen_inline_result()
async def chosen_inline_result_handler(chosen_inline_result: types.ChosenInlineResult):
    inline_message_id = chosen_inline_result.inline_message_id
    query = chosen_inline_result.query.lower()

    if query == "ily":
        await heart_animation(bot, inline_message_id)
    elif query.startswith("cb"):
        parts = chosen_inline_result.result_id.split("_")
        asset = parts[1]
        amount_str = parts[2]

        try:
            amount = float(amount_str)
            if amount.is_integer():
                amount = int(amount)
        except ValueError:
            amount = amount_str

        extra_text = "_".join(parts[3:]) if len(parts) > 3 else None
        if extra_text:
            extra_text = extra_text.replace("_", " ")
            extra_text = extra_text.replace("%20", " ")
        if extra_text:
            await cb_animation(bot, inline_message_id, asset, amount, extra_text)
        else:
            await cb_animation(bot, inline_message_id, asset, amount)


if __name__ == "__main__":
    setup_tools_ping(dp, bot)
    setup_tools_youtube(dp, bot)
    setup_tools_f(dp, bot)
    dp.include_router(updates_router)
    dp.run_polling(bot)

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from modules.calc import inline_calculator
from modules.gemini import gemini_questions, gemini_question, setup_tools_gemini
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


async def handle_empty_query(inline_query: types.InlineQuery):
    results = [
        await inline_ping(inline_query),
        await inline_help(inline_query),
        await inline_updates(inline_query)
    ]
    await inline_query.answer(results, cache_time=0)


async def handle_specific_query(query_text, inline_query, bot):
    inline_actions = {
        "ping": inline_ping,
        "ily": inline_ily,
        "sysinfo": inline_system_info,
        "qr": inline_qr,
        "url": inline_tinyurl,
        "help": inline_help,
        "porn": inline_nswf,
        "movie": inline_movie,
        "cb": lambda iq: inline_photo_with_caption_and_button(iq, bot),
        "pic": show_user_images,
        "rdr": inline_redirect,
        "tr": inline_translate,
        "yt": inline_youtube_search,
        "calc": inline_calculator,
        "press": inline_f,
        "update": inline_updates,
        "wh": inline_weather,
        "wiki": inline_wiki,
        "duck": inline_search,
        "gemini": gemini_questions
    }

    query_action = query_text.split()[0]
    if query_action in inline_actions:
        return await inline_actions[query_action](inline_query)
    return None


@dp.inline_query()
async def inline_handler(inline_query: types.InlineQuery):
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

    if query_text == "":
        await handle_empty_query(inline_query)
        return

    item = await handle_specific_query(query_text, inline_query, bot)

    if item is None:
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
    user_id = chosen_inline_result.from_user.id  # Получаем user_id

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
    elif query.startswith("gemini"):
        model = chosen_inline_result.result_id.split("_")[1]
        query_text = query[len("gemini"):].strip()
        await gemini_question(bot, inline_message_id, model, query_text, user_id)


async def main():
    setup_tools_ping(dp, bot)
    setup_tools_youtube(dp, bot)
    setup_tools_f(dp, bot)
    setup_tools_gemini(dp, bot)
    dp.include_router(updates_router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())

import aiohttp
from aiogram import types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, \
    LinkPreviewOptions
from html import escape
import config
from loader import dp, bot

async def inline_photo_with_caption_and_button(inline_query, bot):
    query_text = inline_query.query.split()
    if len(query_text) < 3 or query_text[0].lower() != 'cb':
        await inline_query.answer([], cache_time=0, switch_pm_text="Неверный формат запроса", switch_pm_parameter="error")
        return

    main_asset = query_text[1]
    main_amount = query_text[2]

    if not main_asset.isalpha():
        await inline_query.answer([], cache_time=0, switch_pm_text="Неверный формат: введите валюту и количество", switch_pm_parameter="error")
        return

    main_asset_2 = escape(main_asset.upper())
    main_amount_2 = escape(main_amount)

    extra_text = " ".join(query_text[3:]) if len(query_text) > 3 else ""
    extra_text = extra_text.replace(" ", "%20")
    result_id = f"cb_{main_asset_2}_{main_amount_2}"
    if extra_text:
        result_id += f"_{extra_text}"

    initial_message_text = f"🕒 Создание <a href='http://t.me/CryptoBotRU/23'>чека</a> на 🪙 <b>{main_amount_2} {main_asset_2}</b>…"
    initial_button = InlineKeyboardButton(text="...", callback_data="none")
    initial_keyboard = InlineKeyboardMarkup(inline_keyboard=[[initial_button]])

    input_content = InputTextMessageContent(message_text=initial_message_text, parse_mode="HTML", disable_web_page_preview=True)

    link = f"https://imggen.send.tg/checks/image?asset={main_asset_2}&asset_amount={main_amount_2}"

    item = InlineQueryResultArticle(
        id=result_id,
        title=f"Отправить {main_amount_2} {main_asset_2}",
        input_message_content=input_content,
        thumbnail_url=link,
        description=f"Отправить {main_amount_2} {main_asset_2}",
        reply_markup=initial_keyboard
    )

    return item


async def cb_animation(bot, inline_message_id, main_asset, main_amount, comment=None):
    main_asset_2 = escape(main_asset.upper())
    main_amount_2 = escape(str(main_amount))

    if comment:
        comment = comment.replace("%20", " ")

    caption = f"🦋 <a href='https://t.me/CryptoBotRU/23'>Чек</a> на <b>{main_amount_2} {main_asset_2}</b>."

    try:
        main_amount_float = float(main_amount)
        if main_amount_float.is_integer():
            main_amount_float = int(main_amount_float)
    except ValueError:
        main_amount_float = None

    if main_amount_float is not None:
        headers = {
            'authorization': config.EXCHANGE_KEY
        }
        params = {
            'fsym': main_asset,
            'tsyms': 'USD'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get("https://min-api.cryptocompare.com/data/price", headers=headers,
                                   params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'USD' in data:
                        fiat_amount = data['USD'] * main_amount_float
                        fiat_amount_str = f"{fiat_amount:.10f}".rstrip('0').rstrip('.')

                        if fiat_amount_str.endswith(".0"):
                            fiat_amount_str = fiat_amount_str[:-2]

                        caption += f" <b>({fiat_amount_str} USD)</b>"
                        link = f"https://imggen.send.tg/checks/image?asset={main_asset}&asset_amount={main_amount_float}&fiat=USD&fiat_amount={fiat_amount_str}&main=asset"
                    else:
                        link = f"https://imggen.send.tg/checks/image?asset={main_asset}&asset_amount={main_amount_float}"
                else:
                    link = f"https://imggen.send.tg/checks/image?asset={main_asset}&asset_amount={main_amount_float}"
    else:
        link = f"https://imggen.send.tg/checks/image?asset={main_asset}&asset_amount={main_amount}"

    if comment:
        caption += escape(f"\n\n💬 {comment}")

    options = LinkPreviewOptions(
        url=link,
        show_above_text=True,
    )
    final_button = InlineKeyboardButton(text=f"Получить {main_amount_2} {main_asset_2}", url="t.me/jdidoxswat")
    final_keyboard = InlineKeyboardMarkup(inline_keyboard=[[final_button]])

    await bot.edit_message_text(
        inline_message_id=inline_message_id,
        text=caption,
        reply_markup=final_keyboard,
        parse_mode="HTML",
        link_preview_options=options
    )


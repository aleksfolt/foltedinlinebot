import asyncio
import hashlib
import random
from aiogram import types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

arr = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "💖"]
h = "🤍"


async def heart_animation(bot, inline_message_id):
    first_block = ""
    for i in "".join(
            [
                h * 9,
                "\n",
                h * 2,
                arr[0] * 2,
                h,
                arr[0] * 2,
                h * 2,
                "\n",
                h,
                arr[0] * 7,
                h,
                "\n",
                h,
                arr[0] * 7,
                h,
                "\n",
                h,
                arr[0] * 7,
                h,
                "\n",
                h * 2,
                arr[0] * 5,
                h * 2,
                "\n",
                h * 3,
                arr[0] * 3,
                h * 3,
                "\n",
                h * 4,
                arr[0],
                h * 4,
            ]
    ).split("\n"):
        first_block += i + "\n"
        await bot.edit_message_text(first_block, inline_message_id=inline_message_id)
        await asyncio.sleep(0.3)
    for i in arr:
        await bot.edit_message_text(
            "".join(
                [
                    h * 9,
                    "\n",
                    h * 2,
                    i * 2,
                    h,
                    i * 2,
                    h * 2,
                    "\n",
                    h,
                    i * 7,
                    h,
                    "\n",
                    h,
                    i * 7,
                    h,
                    "\n",
                    h,
                    i * 7,
                    h,
                    "\n",
                    h * 2,
                    i * 5,
                    h * 2,
                    "\n",
                    h * 3,
                    i * 3,
                    h * 3,
                    "\n",
                    h * 4,
                    i,
                    h * 4,
                    "\n",
                    h * 9,
                ]
            ),
            inline_message_id=inline_message_id
        )
        await asyncio.sleep(0.4)
    for _ in range(8):
        rand = random.choices(arr, k=34)
        await bot.edit_message_text(
            "".join(
                [
                    h * 9,
                    "\n",
                    h * 2,
                    rand[0],
                    rand[1],
                    h,
                    rand[2],
                    rand[3],
                    h * 2,
                    "\n",
                    h,
                    rand[4],
                    rand[5],
                    rand[6],
                    rand[7],
                    rand[8],
                    rand[9],
                    rand[10],
                    h,
                    "\n",
                    h,
                    rand[11],
                    rand[12],
                    rand[13],
                    rand[14],
                    rand[15],
                    rand[16],
                    rand[17],
                    h,
                    "\n",
                    h,
                    rand[18],
                    rand[19],
                    rand[20],
                    rand[21],
                    rand[22],
                    rand[23],
                    rand[24],
                    h,
                    "\n",
                    h * 2,
                    rand[25],
                    rand[26],
                    rand[27],
                    rand[28],
                    rand[29],
                    h * 2,
                    "\n",
                    h * 3,
                    rand[30],
                    rand[31],
                    rand[32],
                    h * 3,
                    "\n",
                    h * 4,
                    rand[33],
                    h * 4,
                    "\n",
                    h * 9,
                ]
            ),
            inline_message_id=inline_message_id
        )
        await asyncio.sleep(0.4)
    fourth = "".join(
        [
            h * 9,
            "\n",
            h * 2,
            arr[0] * 2,
            h,
            arr[0] * 2,
            h * 2,
            "\n",
            h,
            arr[0] * 7,
            h,
            "\n",
            h,
            arr[0] * 7,
            h,
            "\n",
            h,
            arr[0] * 7,
            h,
            "\n",
            h * 2,
            arr[0] * 5,
            h * 2,
            "\n",
            h * 3,
            arr[0] * 3,
            h * 3,
            "\n",
            h * 4,
            arr[0],
            h * 4,
            "\n",
            h * 9,
        ]
    )
    await bot.edit_message_text(fourth, inline_message_id=inline_message_id)
    for _ in range(47):
        fourth = fourth.replace("🤍", "❤️", 1)
        await bot.edit_message_text(fourth, inline_message_id=inline_message_id)
        await asyncio.sleep(0.07)
    for i in range(8):
        await bot.edit_message_text((arr[0] * (8 - i) + "\n") * (8 - i), inline_message_id=inline_message_id)
        await asyncio.sleep(0.3)
    for i in ["I", "I ❤️", "I ❤️ U", "I ❤️ U!"]:
        await bot.edit_message_text(f"<b>{i}</b>", inline_message_id=inline_message_id, parse_mode="HTML")
        await asyncio.sleep(0.2)


async def inline_ily(inline_query: InlineQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Ily", callback_data="hello")
    )

    input_content = InputTextMessageContent(message_text="Привет")
    result_id = hashlib.md5("Привет".encode()).hexdigest()

    item = InlineQueryResultArticle(
        id=result_id,
        type="article",
        title="Ily Animation",
        thumbnail_url="https://tinypic.host/images/2024/09/01/DALLE-2024-09-01-03.24.22---A-detailed-illustration-of-a-heart-emoji-on-a-dark-blue-background.-The-heart-should-be-vibrant-red-with-a-smooth-glossy-texture-and-a-slight-shine.webp",
        input_message_content=input_content,
        reply_markup=builder.as_markup()
    )

    return item


def setup_tools_ily(dp, bot):
    dp.chosen_inline_result(chosen_inline_result_handler)


async def chosen_inline_result_handler(chosen_inline_result: types.ChosenInlineResult):
    inline_message_id = chosen_inline_result.inline_message_id
    await heart_animation(chosen_inline_result.bot, inline_message_id)



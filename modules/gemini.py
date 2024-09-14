from aiogram import types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
import config
from aiogram.utils.keyboard import InlineKeyboardBuilder
import google.generativeai as genai

chat_histories = {}
genai.configure(api_key=config.GEMINI_KEY)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

async def get_model(model):
    model = genai.GenerativeModel(
        model_name=model,
        generation_config=generation_config,
        system_instruction="Отвечай как можно короче."
    )
    return model


async def gemini_questions(inline_query):
    query_text = inline_query.query.split()
    results = []
    models = ["gemini-1.5-pro", "gemini-1.0-pro", "gemini-1.5-pro-exp-0827",
              "gemini-1.5-flash", "gemini-1.5-flash-exp-0827", "gemini-1.5-flash-8b-exp-0827"]
    initial_button = InlineKeyboardButton(text="⏳", callback_data="none")
    initial_keyboard = InlineKeyboardMarkup(inline_keyboard=[[initial_button]])
    for model in models:
        input_content = InputTextMessageContent(message_text=f"Generating answer\nModel: {model}", parse_mode="HTML",
                                                disable_web_page_preview=True)
        item = InlineQueryResultArticle(
            id=f"gemini_{model}",
            title=model,
            input_message_content=input_content,
            description=f"Ask a question to {model}",
            reply_markup=initial_keyboard
        )
        results.append(item)
    return results


async def gemini_question(bot, inline_message_id, modell, query_text, user_id):
    if user_id not in chat_histories:
        chat_histories[user_id] = []

    model = await get_model(modell)


    chat_histories[user_id].append({
        "role": "user",
        "parts": [query_text],
    })

    chat_session = model.start_chat(
        history=chat_histories[user_id]
    )

    response = chat_session.send_message(query_text)

    chat_histories[user_id].append({
        "role": "model",
        "parts": [response.text],
    })

    answer = f"User: {query_text}\n\n{modell}: {response.text}"

    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Clear chat history", callback_data=f"clear_chat:{user_id}"))

    try:
        await bot.edit_message_text(
            inline_message_id=inline_message_id,
            text=answer,
            parse_mode="MARKDOWN",
            reply_markup=keyboard.as_markup()
        )
    except Exception:
        await bot.edit_message_text(
            inline_message_id=inline_message_id,
            text=answer,
            reply_markup=keyboard.as_markup()
        )


async def clear_chat_handler(callback_query: types.CallbackQuery, bot):
    callback_data = callback_query.data
    _, user_id = callback_data.split(":")

    user_id = int(user_id)

    if callback_query.from_user.id != user_id:
        await bot.answer_callback_query(
            callback_query.id,
            text="You are not authorized to use this button.",
            show_alert=True
        )
        return

    if user_id in chat_histories:
        del chat_histories[user_id]

    await bot.answer_callback_query(
        callback_query.id,
        text="Chat history cleared!"
    )



def setup_tools_gemini(dp, bot):
    dp.callback_query(lambda c: c.data.startswith('clear_chat'))(clear_chat_handler)


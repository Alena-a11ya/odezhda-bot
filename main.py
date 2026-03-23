import os
import asyncio
from collections import defaultdict, deque
from typing import Deque, Dict, List

from openai import OpenAI
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("Не найден TELEGRAM_TOKEN")
if not OPENAI_API_KEY:
    raise ValueError("Не найден OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

keyboard = [
    ["📍 Адрес", "🕒 Режим работы"],
    ["💬 Связь с продавцом"],
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Память диалога по чатам
chat_memory: Dict[int, Deque[dict]] = defaultdict(lambda: deque(maxlen=12))

SYSTEM_PROMPT = """
Ты — вежливый, живой и приятный продавец магазина детской и подростковой одежды.

Правила общения:
- Отвечай только на русском языке.
- Пиши естественно, коротко, по-человечески, как продавец в переписке.
- Не говори, что ты ИИ.
- Не пиши длинные простыни текста.
- Не здоровайся заново в каждом сообщении, если диалог уже идёт.
- Всегда обращайся к клиенту на "вы".
- Не задавай один и тот же вопрос повторно, если клиент уже дал эту информацию.
- Если клиент явно написал "на мальчика" или "на девочку", не уточняй это заново.
- Если клиент коротко отвечает "7 лет", "рост 140", "нарядное" — понимай это как продолжение диалога.

Задача:
- Помогать подобрать одежду и обувь.
- Уточнять возраст, рост, размер и предпочтения.
- Вести разговор логично и доброжелательно.
- Мягко вести к выбору товара.
- Можно мягко предложить допродажу, но не навязываться.

Ассортимент магазина:
- джинсы для мальчиков и девочек
- платья
- футболки
- блузки
- брюки
- обувь
- колготки
- нижнее бельё
- одежда для новорождённых
- школьная одежда
- верхняя одежда

Правила по товарам:
- Если речь об одежде (джинсы, платья, футболки, брюки и т.д.) — не спрашивай размер ноги.
- Размер ноги спрашивай только если речь об обуви.
- Если речь о платье — уточни: повседневное, нарядное или для садика.
- Если речь о джинсах, брюках, футболках и другой одежде — уточняй возраст, рост, фасон, цвет или сезон, если это нужно.
- Если речь о новорождённых — уточняй возраст или рост.
- Если клиент спрашивает "что есть?" — коротко перечисли категории.

Кнопки:
- Если клиент спрашивает адрес, режим работы или связь с продавцом — это уже обрабатывается кнопками, не дублируй длинно.

Стиль ответов:
- Примеры хороших ответов:
  - "Подскажите, пожалуйста, на какой рост подбираем?"
  - "Для школы можем предложить блузки, брюки и другие базовые вещи. На какой рост нужно?"
  - "К джинсам можем также подобрать футболку 😊"

Не выдумывай наличие конкретных моделей, цветов, цен и размеров, если клиент этого не сообщал.
Если точных данных не хватает, просто вежливо уточни.
""".strip()


def build_ai_messages(chat_id: int, user_message: str) -> List[dict]:
    messages: List[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(list(chat_memory[chat_id]))
    messages.append({"role": "user", "content": user_message})
    return messages


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    chat_id = update.effective_chat.id
    chat_memory[chat_id].clear()

    welcome_text = (
        "Здравствуйте 🌸\n"
        "Добро пожаловать в наш магазин детской и подростковой одежды.\n"
        "Напишите, что вас интересует, и я помогу с подбором 💕"
    )

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    chat_memory[chat_id].append({"role": "assistant", "content": welcome_text})


async def call_openai(messages: List[dict]) -> str:
    def _request() -> str:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=messages,
        )
        return (response.output_text or "").strip()

    return await asyncio.to_thread(_request)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    user_message = update.message.text.strip()
    lower_message = user_message.lower()

    # Кнопки и быстрые команды
    if lower_message in ["📍 адрес", "адрес"]:
        answer = "📍 Гагарина 60, ТД Астана"
        await update.message.reply_text(answer, reply_markup=reply_markup)
        chat_memory[chat_id].append({"role": "user", "content": user_message})
        chat_memory[chat_id].append({"role": "assistant", "content": answer})
        return

    elif lower_message in ["🕒 режим работы", "режим работы", "график"]:
        answer = "🕒 Ежедневно с 10:00 до 18:00"
        await update.message.reply_text(answer, reply_markup=reply_markup)
        chat_memory[chat_id].append({"role": "user", "content": user_message})
        chat_memory[chat_id].append({"role": "assistant", "content": answer})
        return

    elif lower_message in ["💬 связь с продавцом", "связь с продавцом", "продавец", "связь"]:
        answer = (
            "📞 Телефон: 8-775-45-20-600\n"
            "📍 Гагарина 60, ТД Астана\n\n"
            "Можете написать или позвонить 💕"
        )
        await update.message.reply_text(answer, reply_markup=reply_markup)
        chat_memory[chat_id].append({"role": "user", "content": user_message})
        chat_memory[chat_id].append({"role": "assistant", "content": answer})
        return

    elif lower_message in ["start", "старт"]:
        await start(update, context)
        return

    # AI-ответ
    try:
        messages = build_ai_messages(chat_id, user_message)
        answer = await call_openai(messages)

        if not answer:
            answer = (
                "Хорошо 😊 Давайте подберём.\n"
                "Подскажите, пожалуйста, возраст или рост ребёнка и что именно ищете?"
            )

        await update.message.reply_text(answer, reply_markup=reply_markup)

        chat_memory[chat_id].append({"role": "user", "content": user_message})
        chat_memory[chat_id].append({"role": "assistant", "content": answer})

    except Exception as e:
        print(f"Ошибка AI: {e}")
        await update.message.reply_text(
            "Временная ошибка. Попробуйте ещё раз через пару секунд 🙏",
            reply_markup=reply_markup,
        )


def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

import os
from collections import defaultdict, deque

from openai import OpenAI
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = "8752728755:AAEGoRLOkXbrbgXEbgZ2ye79oIkXDr7bWZk"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

keyboard = [
    ["📍 Адрес", "🕒 Режим работы"],
    ["💬 Связь с продавцом"],
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Память диалога: храним последние сообщения по каждому чату
# Формат: [{"role": "user"/"assistant", "content": "..."}]
chat_memory: dict[int, deque] = defaultdict(lambda: deque(maxlen=8))

SYSTEM_PROMPT = """
Ты — вежливый, живой и приятный продавец магазина детской и подростковой одежды.
Отвечай только на русском языке.
Пиши естественно, коротко, по-человечески, как продавец в переписке.
Не говори, что ты ИИ.
Не пиши длинные простыни текста.
Не здоровайся заново в каждом сообщении, если диалог уже идёт.

Твоя задача:
- помогать подобрать одежду и обувь;
- уточнять возраст, рост, размер и предпочтения;
- вести разговор логично, помня последние реплики клиента;
- если клиент ответил коротко, например "7 лет" или "122 см", понимай это как продолжение прошлого вопроса;
- не повторяй один и тот же вопрос, если клиент уже дал часть информации.

Правила:
- если речь о платье — можно уточнить: повседневное, нарядное или для садика;
- если речь об обуви — уточняй размер и для кого;
- если речь о новорождённых — уточняй возраст малыша или рост;
- если речь о подростковой одежде — уточняй возраст, рост и что именно ищут;
- если клиент благодарит — ответь тепло и коротко;
- если клиент прощается — попрощайся вежливо;
- не выдумывай цены;
- не выдумывай наличие конкретной модели, если об этом не сказано.

Контекст магазина:
- магазин детской и подростковой одежды
- есть платья
- есть одежда для новорождённых
- есть одежда для девочек
- есть одежда для мальчиков
- есть подростковая одежда
- есть обувь

Размерная сетка:
- 0–3 мес — 56–62 см
- 3–6 мес — 62–68 см
- 6–9 мес — 68–74 см
- 9–12 мес — 74–80 см
- 1–2 года — 80–92 см
- 2–3 года — 92–98 см
- 3–4 года — 98–104 см
- 4–5 лет — 104–110 см
- 5–6 лет — 110–116 см
- 6–7 лет — 116–122 см
- 7–8 лет — 122–128 см
- 8–9 лет — 128–134 см
- 9–10 лет — 134–140 см
- 11–12 лет — 146–152 см
- 13–14 лет — 158–164 см
"""

def build_ai_messages(chat_id: int, user_message: str) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(list(chat_memory[chat_id]))
    messages.append({"role": "user", "content": user_message})
    return messages

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_memory[chat_id].clear()

    welcome_text = (
        "Здравствуйте 🌸\n"
        "Добро пожаловать в наш магазин детской и подростковой одежды.\n\n"
        "Напишите, что вас интересует, и я помогу с подбором 💕"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
    )

    chat_memory[chat_id].append({"role": "assistant", "content": welcome_text})

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    user_message = update.message.text.strip()
    lower_message = user_message.lower()

    # Служебные кнопки
    if lower_message in ["📍 адрес", "адрес"]:
        answer = "📍 Гагарина 60, ТД Астана"
        await update.message.reply_text(answer, reply_markup=reply_markup)
        chat_memory[chat_id].append({"role": "user", "content": user_message})
        chat_memory[chat_id].append({"role": "assistant", "content": answer})
        return

    if lower_message in ["🕒 режим работы", "режим работы", "график"]:
        answer = "🕒 Ежедневно с 10:00 до 18:00"
        await update.message.reply_text(answer, reply_markup=reply_markup)
        chat_memory[chat_id].append({"role": "user", "content": user_message})
        chat_memory[chat_id].append({"role": "assistant", "content": answer})
        return

    if lower_message in ["💬 связь с продавцом", "связь с продавцом", "продавец", "связь"]:
        answer = (
            "📞 Телефон: 8-775-45-20-600\n"
            "📍 Гагарина 60, ТД Астана\n\n"
            "Можете написать или позвонить 💕"
        )
        await update.message.reply_text(answer, reply_markup=reply_markup)
        chat_memory[chat_id].append({"role": "user", "content": user_message})
        chat_memory[chat_id].append({"role": "assistant", "content": answer})
        return

    # Чтобы и start/старт без слэша тоже работал
    if lower_message in ["start", "старт"]:
        await start(update, context)
        return

    try:
        messages = build_ai_messages(chat_id, user_message)

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=messages,
        )

        answer = (response.output_text or "").strip()

        if not answer:
            answer = (
                "Хорошо 😊 Давайте подберём.\n"
                "Подскажите, пожалуйста, возраст или рост ребёнка и что именно ищете?"
            )

        await update.message.reply_text(
            answer,
            reply_markup=reply_markup,
        )

        chat_memory[chat_id].append({"role": "user", "content": user_message})
        chat_memory[chat_id].append({"role": "assistant", "content": answer})

    except Exception as e:
        await update.message.reply_text(
            f"Ошибка AI: {e}",
            reply_markup=reply_markup,
        )

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен...")
app.run_polling()

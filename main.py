import os

from openai import OpenAI
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = "8752728755:AAEGoRLOkXbrbgXEbgZ2ye79oIkXDr7bWZk"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

keyboard = [
    ["📍 Адрес", "🕒 Режим работы"],
    ["💬 Связь с продавцом", "🆕 Новинки"],
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

SYSTEM_PROMPT = """
Ты — вежливый, живой и приятный продавец магазина детской и подростковой одежды.
Отвечай на русском языке.
Пиши естественно, как человек в переписке с клиентом.
Не отвечай сухо и шаблонно.
Не пиши слишком длинно.
Если клиент спрашивает про товар — помогай подобрать и уточняй возраст, рост, размер или предпочтения.
Если клиент спрашивает про платье — можешь уточнить: повседневное, нарядное или для садика.
Если клиент спрашивает про обувь — уточняй размер и для кого.
Если клиент спрашивает про новорождённых — уточняй возраст малыша или рост.
Если клиент спрашивает про подростковую одежду — уточняй возраст, рост и что именно ищут.
Если клиент здоровается — поздоровайся красиво и предложи помощь.
Если клиент благодарит — ответь тепло и коротко.
Если клиент прощается — попрощайся вежливо.
Не выдумывай цены, которых тебе не сообщали.
Не выдумывай наличие конкретной модели, если этого нет в сообщении клиента.
Не говори, что ты ИИ.
Не здоровайся заново в каждом сообщении, если уже диалог идёт.

Контекст магазина:
- магазин детской и подростковой одежды
- есть платья
- есть одежда для новорождённых
- есть одежда для девочек
- есть одежда для мальчиков
- есть подростковая одежда
- есть обувь
- есть новинки

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте 🌸\n"
        "Добро пожаловать в наш магазин детской и подростковой одежды.\n\n"
        "Напишите, что вас интересует, или выберите раздел ниже 👇",
        reply_markup=reply_markup,
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()
    lower_message = user_message.lower()

    # Кнопки и служебные ответы — вручную
    if lower_message in ["📍 адрес", "адрес"]:
        await update.message.reply_text(
            "📍 Гагарина 60, ТД Астана",
            reply_markup=reply_markup,
        )
        return

    if lower_message in ["🕒 режим работы", "режим работы", "график"]:
        await update.message.reply_text(
            "🕒 Ежедневно с 10:00 до 18:00",
            reply_markup=reply_markup,
        )
        return

    if lower_message in ["💬 связь с продавцом", "связь с продавцом", "продавец", "связь"]:
        await update.message.reply_text(
            "📞 Телефон: 8-775-45-20-600\n"
            "📍 Гагарина 60, ТД Астана\n\n"
            "Можете написать или позвонить 💕",
            reply_markup=reply_markup,
        )
        return

    if lower_message in ["🆕 новинки", "новинки", "новое поступление"]:
        await update.message.reply_text(
            "🆕 Новинки скоро добавим сюда 💕\n"
            "Можете написать, что именно вас интересует, и я помогу с подбором.",
            reply_markup=reply_markup,
        )
        return

    # Обычное слово start тоже отправляем в старт
    if lower_message in ["start", "старт"]:
        await start(update, context)
        return

    # Всё остальное отдаём AI
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )

        answer = (response.output_text or "").strip()

        if not answer:
            answer = (
                "Да, конечно 😊 Подскажите, пожалуйста, что именно вас интересует — "
                "платья, обувь, новорождённые или подростковая одежда?"
            )

        await update.message.reply_text(
            answer,
            reply_markup=reply_markup,
        )

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

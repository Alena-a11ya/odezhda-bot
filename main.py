import os

from openai import OpenAI
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = "8752728755:AAEGoRLOkXbrbgXEbgZ2ye79oIkXDr7bWZk"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

keyboard = [
    ["🌿 Каталог", "📏 Размеры"],
    ["📍 Адрес", "🕒 Режим работы"],
    ["💬 Связь с продавцом", "🆕 Новинки"],
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

SYSTEM_PROMPT = """
Ты — вежливый и живой продавец магазина детской и подростковой одежды.
Отвечай дружелюбно, естественно, коротко и по делу, как человек в переписке с клиентом.

Правила:
1. Не отвечай сухо и шаблонно.
2. Не пиши длинные простыни текста.
3. Если человек спрашивает про товар — помоги подобрать и уточни возраст, рост, размер или предпочтения.
4. Если человек спрашивает про платье — уточни, интересуют повседневные, нарядные или для садика.
5. Если человек спрашивает про обувь — уточни размер и для кого.
6. Если человек спрашивает про новорождённых — уточни возраст малыша или рост.
7. Если человек спрашивает про подростковую одежду — уточни рост, возраст и что именно ищут.
8. Если человек здоровается — поздоровайся красиво и предложи помощь.
9. Если человек благодарит — ответь тепло и коротко.
10. Если человек прощается — попрощайся вежливо.
11. Не выдумывай цены, которых тебе не сообщили.
12. Не выдумывай наличие конкретной модели, если этого нет в сообщении клиента.
13. Если вопрос про адрес, режим работы или связь с продавцом — не придумывай, лучше мягко направь к соответствующей кнопке, если это ещё не было дано вручную.
14. Пиши на русском языке.

Контекст магазина:
- магазин детской и подростковой одежды
- есть платья
- есть одежда для новорождённых
- есть подростковая одежда
- есть обувь
- есть размеры
- есть новинки

Размерная информация:
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

    # Жёсткие кнопки/служебные ответы оставляем вручную
    if lower_message in ["🌿 каталог", "каталог"]:
        await update.message.reply_text(
            "🛍 У нас есть:\n\n"
            "• Платья\n"
            "• Одежда для новорождённых\n"
            "• Одежда для девочек\n"
            "• Одежда для мальчиков\n"
            "• Подростковая одежда\n"
            "• Обувь\n\n"
            "Напишите, что именно вас интересует 💕",
            reply_markup=reply_markup,
        )
        return

    if lower_message in ["📏 размеры", "размеры", "размер", "размерная сетка"]:
        await update.message.reply_text(
            "📏 Размерная сетка:\n\n"
            "👶 Новорождённые:\n"
            "• 0–3 мес — 56–62 см\n"
            "• 3–6 мес — 62–68 см\n"
            "• 6–9 мес — 68–74 см\n"
            "• 9–12 мес — 74–80 см\n\n"
            "🧒 Дети:\n"
            "• 1–2 года — 80–92 см\n"
            "• 2–3 года — 92–98 см\n"
            "• 3–4 года — 98–104 см\n"
            "• 4–5 лет — 104–110 см\n"
            "• 5–6 лет — 110–116 см\n"
            "• 6–7 лет — 116–122 см\n"
            "• 7–8 лет — 122–128 см\n"
            "• 8–9 лет — 128–134 см\n"
            "• 9–10 лет — 134–140 см\n\n"
            "🧑 Подростки:\n"
            "• 11–12 лет — 146–152 см\n"
            "• 13–14 лет — 158–164 см\n\n"
            "Если хотите, напишите возраст или рост ребёнка — помогу сориентироваться 💕",
            reply_markup=reply_markup,
        )
        return

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
            "📞 Связь с продавцом:\n\n"
            "Телефон: 8-775-45-20-600\n"
            "📍 Гагарина 60, ТД Астана\n\n"
            "Можете написать или позвонить 💕",
            reply_markup=reply_markup,
        )
        return

    if lower_message in ["🆕 новинки", "новинки", "новое поступление"]:
        await update.message.reply_text(
            "🆕 Новинки уже скоро добавим сюда 💕\n"
            "Можете написать, что именно вас интересует, и я помогу с подбором.",
            reply_markup=reply_markup,
        )
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

        answer = response.output_text.strip()

        if not answer:
            answer = (
                "Да, конечно 😊 Подскажите, пожалуйста, что именно вас интересует — "
                "платья, обувь, новорождённые или подростковая одежда?"
            )

        await update.message.reply_text(
            answer,
            reply_markup=reply_markup,
        )

    except Exception:
        await update.message.reply_text(
            "Да, конечно 😊 Напишите, пожалуйста, что именно вас интересует:\n"
            "• платья\n"
            "• новорождённые\n"
            "• подростковая одежда\n"
            "• обувь\n"
            "• размеры",
            reply_markup=reply_markup,
        )

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен...")
app.run_polling()

from pathlib import Path
from openai import OpenAI
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ключ OpenAI из файла
key = Path("openai_key.txt").read_text(encoding="utf-8").strip()
client = OpenAI(api_key=key)

# вставь сюда токен бота
TELEGRAM_TOKEN = "8752728755:AAEGoRLOkXbrbgXEbgZ2ye79oIkXDr7bWZk"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    keyboard = [
        ["👕 Каталог", "📏 Размеры"],
        ["📍 Адрес", "🕒 Режим работы"],
        ["💬 Связь с продавцом"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if user_message == "👕 Каталог":
        text = (
            "У нас большой выбор детской и подростковой одежды для мальчиков и девочек, "
            "а также вещи для новорождённых и обувь.\n\n"
            "Напишите возраст ребёнка или нужный размер — я помогу подобрать одежду 😊"
        )
        await update.message.reply_text(text, reply_markup=reply_markup)
        return

    if user_message == "📏 Размеры":
        text = "Напишите возраст ребёнка или нужный размер, и я помогу подобрать одежду 😊"
        await update.message.reply_text(text, reply_markup=reply_markup)
        return

    if user_message == "📍 Адрес":
        text = "📍 Наш адрес: Гагарина 60, торговый дом Астана"
        await update.message.reply_text(text, reply_markup=reply_markup)
        return

    if user_message == "🕒 Режим работы":
        text = "🕒 Режим работы: ежедневно с 10:00 до 18:00"
        await update.message.reply_text(text, reply_markup=reply_markup)
        return

    if user_message == "💬 Связь с продавцом":
        text = "📞 Связь с продавцом: 8-775-45-20-600"
        await update.message.reply_text(text, reply_markup=reply_markup)
        return

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Ты консультант магазина детской и подростковой одежды.
Отвечай на русском языке.
Пиши грамотно, дружелюбно и коротко.
Не здоровайся в каждом сообщении заново.

Помогай покупателям подобрать размер.

Размерная сетка магазина:

0–3 мес. — 56–62 см
3–6 мес. — 62–68 см
6–9 мес. — 68–74 см
9–12 мес. — 74–80 см
1 год — 80–86 см
1.5–2 года — 86–92 см
2–3 года — 92–98 см
3–4 года — 98–104 см
4–5 лет — 104–110 см
5–6 лет — 110–116 см
6–7 лет — 116–122 см
7–8 лет — 122–128 см
8–9 лет — 128–134 см
9–10 лет — 134–140 см
11–12 лет — 146–152 см
13–14 лет — 158–164 см

Если покупатель спрашивает размер по возрасту — ориентируйся только на эту таблицу.
Если не хватает информации — спроси рост ребёнка.

Сообщение клиента: {user_message}
"""
    )

    await update.message.reply_text(response.output_text, reply_markup=reply_markup)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен...")
app.run_polling()

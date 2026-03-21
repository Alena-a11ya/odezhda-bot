import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = "8752728755:AAEGoRLOkXbrbgXEbgZ2ye79oIkXDr7bWZk"

keyboard = [
    ["📍 Адрес", "🕒 Режим работы"],
    ["💬 Связь с продавцом"],
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте 🌸\n"
        "Напишите, что вас интересует, я помогу с подбором 💕",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "адрес" in text:
        await update.message.reply_text("📍 Гагарина 60, ТД Астана")
        return

    if "режим" in text:
        await update.message.reply_text("🕒 С 10:00 до 18:00")
        return

    if "связь" in text or "продав" in text:
        await update.message.reply_text(
            "📞 8-775-45-20-600\n📍 Гагарина 60"
        )
        return

    # нормальный ответ вместо тупого шаблона
    await update.message.reply_text(
        "Хорошо 😊 Давайте подберём.\n"
        "Подскажите возраст или рост ребёнка и что именно ищете?"
    )

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен...")
app.run_polling()

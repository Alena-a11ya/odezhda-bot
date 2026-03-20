
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN ="8752728755:AAEGoRLOkXbrbgXEbgZ2ye79oIkXDr7bWZk"

# кнопки
reply_markup = ReplyKeyboardMarkup(
    [
        ["Платья", "Обувь"],
        ["Новорожденные", "Подростковая одежда"],
        ["Размеры", "Новинки"],
        ["Адрес", "Связь с продавцом"],
    ],
    resize_keyboard=True,
)

# старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать 🌸\n"
        "В наш магазин детской и подростковой одежды\n\n"
        "Выберите раздел ниже 👇",
        reply_markup=reply_markup,
    )

# ответы
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    # платья
    if "плать" in user_message:
        await update.message.reply_text(
            "Отлично 👗\n\n"
            "Напишите, пожалуйста:\n"
            "• возраст ребёнка\n"
            "• рост\n"
            "• какие модели интересуют:\n"
            "  — повседневные\n"
            "  — нарядные",
            reply_markup=reply_markup,
        )
        return

    # обувь
    if "обув" in user_message:
        await update.message.reply_text(
            "Хорошо 👟\n\n"
            "Напишите:\n"
            "• размер\n"
            "• для девочки или мальчика",
            reply_markup=reply_markup,
        )
        return

    # новорожденные
    if "новорож" in user_message:
        await update.message.reply_text(
            "Для новорожденных 👶\n\n"
            "Напишите:\n"
            "• возраст\n"
            "• что именно ищете",
            reply_markup=reply_markup,
        )
        return

    # подростки
    if "подрост" in user_message:
        await update.message.reply_text(
            "Подростковая одежда 👕\n\n"
            "Напишите:\n"
            "• возраст\n"
            "• размер\n"
            "• что ищете",
            reply_markup=reply_markup,
        )
        return

    # размеры
    if "размер" in user_message:
        await update.message.reply_text(
            "📏 Размерная сетка:\n\n"
            "80–86 — 1–1.5 года\n"
            "92–98 — 2–3 года\n"
            "104–110 — 4–5 лет\n"
            "116–122 — 6–7 лет\n"
            "128–134 — 8–9 лет\n"
            "140–146 — 10–11 лет\n"
            "152–158 — 12–13 лет\n"
            "164 — подростки",
            reply_markup=reply_markup,
        )
        return

    # новинки
    if "новин" in user_message:
        await update.message.reply_text(
            "Скоро добавим новинки ❤️",
            reply_markup=reply_markup,
        )
        return

    # адрес
    if "адрес" in user_message:
        await update.message.reply_text(
            "📍 Гагарина 60, ТД Астана",
            reply_markup=reply_markup,
        )
        return

    # связь
    if "связ" in user_message or "продав" in user_message:
        await update.message.reply_text(
            "📞 Телефон: 8-775-45-20-600\n"
            "📍 Гагарина 60, ТД Астана",
            reply_markup=reply_markup,
        )
        return

    # если не понял
    await update.message.reply_text(
        "Уточните, пожалуйста, что именно ищете 😊\n\n"
        "Например:\n"
        "• платье на девочку 6 лет\n"
        "• обувь 28 размер\n"
        "• одежда для новорожденного",
        reply_markup=reply_markup,
    )


# запуск
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен...")
app.run_polling()

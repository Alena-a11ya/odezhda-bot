from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN ="8752728755:AAEGoRLOkXbrbgXEbgZ2ye79oIkXDr7bWZk"

keyboard = [
    ["🌿 Каталог", "📏 Размеры"],
    ["📍 Адрес", "🕒 Режим работы"],
    ["💬 Связь с продавцом", "🆕 Новинки"],
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте 🌸\n"
        "Добро пожаловать в наш магазин детской и подростковой одежды 👗\n\n"
        "Выберите раздел ниже 👇",
        reply_markup=reply_markup,
       )
       return

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip().lower()

    # приветствие
    if "привет" in user_message or "здрав" in user_message:
        await update.message.reply_text(
            "Здравствуйте 🌸\nЧем могу помочь?",
            reply_markup=reply_markup,
        )
        return

    # прощание
    if "пока" in user_message or "свид" in user_message:
        await update.message.reply_text(
            "До свидания 🌷 Будем рады видеть вас снова ❤️",
            reply_markup=reply_markup,
        )
        return

    # каталог
    if "каталог" in user_message:
        await update.message.reply_text(
            "У нас есть:\n\n"
            "• Платья\n"
            "• Одежда для новорождённых\n"
            "• Подростковая одежда\n"
            "• Обувь",
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

    # продавец
    if "продав" in user_message or "связ" in user_message:
        await update.message.reply_text(
            "📞 Телефон: 8-775-45-20-600\n"
            "📍 Гагарина 60, ТД Астана",
            reply_markup=reply_markup,
        )
        return

    # новинки
    if "новин" in user_message:
        await update.message.reply_text(
            "🆕 Скоро добавим новинки 💕",
            reply_markup=reply_markup,
        )
        return

    # режим работы
    if "режим" in user_message:
        await update.message.reply_text(
            "🕒 Ежедневно с 10:00 до 18:00",
            reply_markup=reply_markup,
        )
        return

    # платья
    if "плать" in user_message:
        await update.message.reply_text(
            "Да, конечно 😊 Сейчас подберём платья.\n\n"
            "Подскажите:\n"
            "• возраст\n"
            "• рост ребёнка\n\n"
            "Какие модели интересуют:\n"
            "• повседневные\n"
            "• нарядные",
            reply_markup=reply_markup,
        )
        return

        # если не понял
        await update.message.reply_text(
        "Уточните, пожалуйста, что именно ищете 😊\n\n"
        "Например:\n"
        "• платье на девочку 6 лет\n"
        "• обувь 28 размер\n"
        "• одежда для новорождённого",
        reply_markup=reply_markup,
    )
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен...")
app.run_polling()



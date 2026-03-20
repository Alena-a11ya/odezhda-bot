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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip().lower()

    # приветствие
    if "здрав" in user_message or "привет" in user_message or "добрый" in user_message:
        await update.message.reply_text(
            "Здравствуйте 🌸\n"
            "Чем могу помочь? 😊",
            reply_markup=reply_markup,
        )
        return

    # прощание
    if "пока" in user_message or "свид" in user_message:
        await update.message.reply_text(
            "До свидания 🌷\nБудем рады видеть вас снова 💕",
            reply_markup=reply_markup,
        )
        return

    # каталог
    if "каталог" in user_message:
        await update.message.reply_text(
            "🛍 У нас есть:\n\n"
            "• Платья\n"
            "• Одежда для новорождённых\n"
            "• Одежда для девочек\n"
            "• Одежда для мальчиков\n"
            "• Подростковая одежда\n"
            "• Обувь",
            reply_markup=reply_markup,
        )
        return

    # размеры
    if "размер" in user_message:
        await update.message.reply_text(
            "📏 Напишите возраст или рост ребёнка — помогу подобрать 💕",
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
    if user_message in ["🕒 режим работы", "режим работы", "график"]:
        await update.message.reply_text(
            "🕒 Режим работы:\nЕжедневно с 10:00 до 18:00",
            reply_markup=reply_markup,
        )
        return

    # связь с продавцом
    if user_message in ["💬 связь с продавцом", "связь с продавцом", "продавец", "связь"]:
        await update.message.reply_text(
            "📞 Связь с продавцом:\n\n"
            "Телефон: 8-775-45-20-600\n"
            "📍 Адрес: Гагарина 60, ТД Астана\n\n"
            "Можете написать или позвонить 💕",
            reply_markup=reply_markup,
        )
        return
    # общий ответ
    await update.message.reply_text(
        "Я помогу вам с выбором 🌸\n\n"
        "Напишите:\n"
        "• платья\n"
        "• новорождённые\n"
        "• подростковая одежда\n"
        "• обувь\n"
        "• размеры\n"
        "• новинки",
        reply_markup=reply_markup,
    )


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен...")
app.run_polling()



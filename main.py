from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = "8752728755:AAEGoRLOkXbrbgXEbgZ2ye79oIkXDr7bWZk"

keyboard = [
    ["🌿 Каталог", "📏 Размеры"],
    ["📍 Адрес", "🕒 Режим работы"],
    ["💬 Связь с продавцом", "🆕 Новинки"],
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте 🌸\n"
        "Добро пожаловать в магазин детской и подростковой одежды.\n\n"
        "Выберите раздел ниже 👇",
        reply_markup=reply_markup,
    )
 return

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip().lower()
if any(word in user_message for word in ["здравствуйте", "привет", "добрый день", "салам"]):
    await update.message.reply_text(
        "Здравствуйте 🌸\n"
        "Добро пожаловать в наш магазин детской и подростковой одежды 👗\n\n"
        "Напишите, что вас интересует:\n"
        "• платья\n"
        "• новорождённые\n"
        "• подростковая одежда\n"
        "• обувь\n"
        "• размеры\n"
        "• новинки",
        reply_markup=reply_markup
    )
    return
    if user_message in ["🌿 каталог", "каталог"]:
        await update.message.reply_text(
            "🛍 У нас есть:\n\n"
            "• Платья\n"
            "• Одежда для новорождённых\n"
            "• Одежда для девочек\n"
            "• Одежда для мальчиков\n"
            "• Подростковая одежда\n"
            "• Обувь\n\n"
            "Напишите, что именно ищете 💕",
            reply_markup=reply_markup,
        )
        return

    # ✅ ВОТ ТУТ РАЗМЕРНАЯ СЕТКА
    if user_message in ["📏 размеры", "размеры", "размер", "размерная сетка"]:
        await update.message.reply_text(
            "📏 Размерная сетка:\n\n"
            "👶 Новорожденные:\n"
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
            "🧑‍🎤 Подростки:\n"
            "• 11–12 лет — 146–152 см\n"
            "• 13–14 лет — 158–164 см\n\n"
            "Напишите возраст или рост ребёнка — помогу подобрать 💕",
            reply_markup=reply_markup,
        )
        return

    if user_message in ["📍 адрес", "адрес"]:
        await update.message.reply_text(
            "📍 Гагарина 60, ТД Астана",
            reply_markup=reply_markup,
        )
        return

    if user_message in ["🕒 режим работы", "режим работы"]:
        await update.message.reply_text(
            "🕒 Ежедневно с 10:00 до 18:00",
            reply_markup=reply_markup,
        )
        return

if user_message in ["💬 связь с продавцом", "связь с продавцом"]:
    await update.message.reply_text(
        "📞 Связь с продавцом:\n\n"
        "Телефон: 8-775-45-20-600\n"
        "📍 Адрес: Гагарина 60, ТД Астана\n\n"
        "Можете написать или позвонить 💕",
        reply_markup=reply_markup,
    )
    return
        )
        return

    if user_message in ["🆕 новинки", "новинки"]:
        await update.message.reply_text(
            "🆕 Новинки скоро добавим 💕",
            reply_markup=reply_markup,
        )
        return
if any(word in user_message for word in ["пока", "до свидания", "всего доброго"]):
    await update.message.reply_text(
        "До свидания 🌷\nБудем рады видеть вас снова 💕",
        reply_markup=reply_markup
    )
    return
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




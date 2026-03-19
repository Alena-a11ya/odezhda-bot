from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = "ВСТАВЬ_СЮДА_СВОЙ_ТЕЛЕГРАМ_ТОКЕН"

keyboard = [
    ["🌿 Каталог", "📏 Размеры"],
    ["📍 Адрес", "🕒 Режим работы"],
    ["💬 Связь с продавцом", "🆕 Новинки"],
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


SIZE_TEXT = (
    "📏 Размерная сетка магазина:\n\n"
    "Новорождённые и малыши:\n"
    "• 0–3 мес — 56–62 см\n"
    "• 3–6 мес — 62–68 см\n"
    "• 6–9 мес — 68–74 см\n"
    "• 9–12 мес — 74–80 см\n\n"
    "Дети:\n"
    "• 1 год — 80–86 см\n"
    "• 1.5–2 года — 86–92 см\n"
    "• 2–3 года — 92–98 см\n"
    "• 3–4 года — 98–104 см\n"
    "• 4–5 лет — 104–110 см\n"
    "• 5–6 лет — 110–116 см\n"
    "• 6–7 лет — 116–122 см\n"
    "• 7–8 лет — 122–128 см\n"
    "• 8–9 лет — 128–134 см\n"
    "• 9–10 лет — 134–140 см\n"
    "• 11–12 лет — 146–152 см\n"
    "• 13–14 лет — 158–164 см\n\n"
    "Если не уверены, напишите возраст или рост ребёнка — поможем подобрать 💕"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте 🌸 Добро пожаловать в магазин детской одежды.\n\n"
        "Выберите раздел ниже 👇",
        reply_markup=reply_markup,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip().lower()

    if user_message in ["/start", "start"]:
        await start(update, context)
        return

    if user_message in ["🌿 каталог", "каталог"]:
        await update.message.reply_text(
            "🛍 У нас есть:\n\n"
            "• Платья\n"
            "• Одежда для новорождённых\n"
            "• Одежда для девочек\n"
            "• Одежда для мальчиков\n"
            "• Обувь\n\n"
            "Напишите, что именно ищете, и я помогу 💕",
            reply_markup=reply_markup,
        )
        return

    if user_message in ["📏 размеры", "размеры", "размер", "размерная сетка"]:
        await update.message.reply_text(
            SIZE_TEXT,
            reply_markup=reply_markup,
        )
        return

    if user_message in ["новорождённые", "новорожденные", "для новорождённых", "для новорожденных", "малыши", "для малышей"]:
        await update.message.reply_text(
            "👶 У нас есть одежда для новорождённых и малышей 💕\n\n"
            "Размеры:\n"
            "• 56–62 см\n"
            "• 62–68 см\n"
            "• 68–74 см\n"
            "• 74–80 см\n\n"
            "Напишите:\n"
            "• возраст малыша\n"
            "или\n"
            "• рост\n\n"
            "И я помогу подобрать нужный размер 👌",
            reply_markup=reply_markup,
        )
        return

    if user_message in ["платье", "платья", "платье в садик", "платье для садика", "плать"]:
        await update.message.reply_text(
            "👗 У нас красивые платья для девочек 💕\n\n"
            "• Повседневные\n"
            "• Нарядные\n"
            "• Для садика\n\n"
            "Напишите:\n"
            "• рост ребёнка\n"
            "• возраст\n\n"
            "И я подберу варианты 📸",
            reply_markup=reply_markup,
        )
        return

    if user_message in ["обувь", "ботинки", "кроссовки", "туфли", "сандалии"]:
        await update.message.reply_text(
            "👟 У нас есть детская обувь.\n\n"
            "Напишите:\n"
            "• размер ноги\n"
            "или\n"
            "• возраст ребёнка\n\n"
            "И я помогу подобрать варианты 💕",
            reply_markup=reply_markup,
        )
        return

    if user_message in ["девочки", "для девочек", "одежда для девочек"]:
        await update.message.reply_text(
            "🎀 Для девочек у нас есть:\n"
            "• платья\n"
            "• костюмы\n"
            "• повседневная одежда\n"
            "• нарядные вещи\n\n"
            "Напишите, что именно хотите посмотреть 💕",
            reply_markup=reply_markup,
        )
        return

    if user_message in ["мальчики", "для мальчиков", "одежда для мальчиков"]:
        await update.message.reply_text(
            "🧒 Для мальчиков у нас есть:\n"
            "• костюмы\n"
            "• повседневная одежда\n"
            "• верхняя одежда\n"
            "• обувь\n\n"
            "Напишите, что именно ищете 👌",
            reply_markup=reply_markup,
        )
        return

    if user_message in ["📍 адрес", "адрес"]:
        await update.message.reply_text(
            "📍 Наш адрес: Гагарина 60, торговый дом «Астана».",
            reply_markup=reply_markup,
        )
        return

    if user_message in ["🕒 режим работы", "режим работы", "график"]:
        await update.message.reply_text(
            "🕒 Режим работы:\nЕжедневно с 10:00 до 20:00.",
            reply_markup=reply_markup,
        )
        return

    if user_message in ["💬 связь с продавцом", "связь с продавцом", "продавец", "связаться"]:
        await update.message.reply_text(
            "💬 Напишите ваш вопрос, и мы поможем с выбором.\n\n"
            "Можно сразу указать:\n"
            "• возраст ребёнка\n"
            "• рост\n"
            "• что именно ищете",
            reply_markup=reply_markup,
        )
        return

    if user_message in ["🆕 новинки", "новинки", "новое поступление"]:
        await update.message.reply_text(
            "🆕 Здесь будут новинки магазина.\n\n"
            "Позже добавим сюда фото и свежие поступления 💕",
            reply_markup=reply_markup,
        )
        return

    if any(word in user_message for word in ["рост", "см", "год", "лет", "месяц", "мес"]):
        await update.message.reply_text(
            "Спасибо 💕 Напишите ещё, пожалуйста, что именно ищете:\n"
            "• платье\n"
            "• одежду для новорождённого\n"
            "• обувь\n"
            "• одежду для девочки\n"
            "• одежду для мальчика\n\n"
            "И я помогу подобрать вариант.",
            reply_markup=reply_markup,
        )
        return

    await update.message.reply_text(
        "Я вас поняла 🌸\n\n"
        "Напишите, что именно ищете:\n"
        "• платье\n"
        "• новорождённому\n"
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





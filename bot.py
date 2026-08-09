from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8823889266:AAHiXR8OsTKeIIugSdopAbXILr6Owkl-dl4"

main_menu = [
    ["📈 Add Alert", "📋 My Alerts"],
    ["🏦 Broker Settings", "🗑 Remove Alert"],
    ["ℹ️ Status"]
]

market_menu = [
    ["💱 Forex", "🪙 Crypto"],
    ["🥇 Commodities", "📊 Indices"],
    ["📈 US Stocks"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Universal Trading Alert Platform",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📈 Add Alert":
        await update.message.reply_text(
            "🌍 Select Market",
            reply_markup=ReplyKeyboardMarkup(market_menu, resize_keyboard=True)
        )

    elif text == "💱 Forex":
        await update.message.reply_text(
            "💱 Forex Menu\n\nEURUSD\nGBPUSD\nUSDJPY\nGBPJPY"
        )

    elif text == "🪙 Crypto":
        await update.message.reply_text(
            "🪙 Crypto Menu\n\nBTCUSDT\nETHUSDT"
        )

    elif text == "🥇 Commodities":
        await update.message.reply_text(
            "🥇 Commodities Menu\n\nXAUUSD\nXAGUSD\nUSOIL"
        )

    elif text == "📊 Indices":
        await update.message.reply_text(
            "📊 Indices Menu\n\nNAS100\nUS30\nSPX500"
        )

    elif text == "📈 US Stocks":
        await update.message.reply_text(
            "📈 US Stocks Menu\n\nAAPL\nNVDA\nAMZN"
        )

    elif text == "📋 My Alerts":
        await update.message.reply_text("📋 No alerts yet.")

    elif text == "🏦 Broker Settings":
        await update.message.reply_text("🏦 Broker settings will be added next.")

    elif text == "🗑 Remove Alert":
        await update.message.reply_text("🗑 Remove alert feature coming next.")

    elif text == "ℹ️ Status":
        await update.message.reply_text("🟢 Server Online")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
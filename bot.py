
import os

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")


# ============================================================
# MENUS
# ============================================================

main_menu = [
    ["📈 Add Alert", "📋 My Alerts"],
    ["🏦 Broker Settings", "🗑 Remove Alert"],
    ["ℹ️ Status"]
]

market_menu = [
    ["💱 Forex", "🪙 Crypto"],
    ["🥇 Commodities", "📊 Indices"]
]


# ============================================================
# /START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Universal Trading Alert Platform",
        reply_markup=ReplyKeyboardMarkup(
            main_menu,
            resize_keyboard=True
        )
    )


# ============================================================
# MENU HANDLER
# ============================================================

async def menu_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    text = update.message.text

    # -------------------------
    # ADD ALERT
    # -------------------------

    if text == "📈 Add Alert":
        await update.message.reply_text(
            "🌍 Select Market",
            reply_markup=ReplyKeyboardMarkup(
                market_menu,
                resize_keyboard=True
            )
        )

    # -------------------------
    # FOREX
    # -------------------------

    elif text == "💱 Forex":
        await update.message.reply_text(
            "💱 Forex Menu\n\n"
            "EURUSD\n"
            "GBPUSD\n"
            "USDJPY\n"
            "GBPJPY"
        )

    # -------------------------
    # CRYPTO
    # -------------------------

    elif text == "🪙 Crypto":
        await update.message.reply_text(
            "🪙 Crypto Menu\n\n"
            "BTCUSDT\n"
            "ETHUSDT"
        )

    # -------------------------
    # COMMODITIES
    # -------------------------

    elif text == "🥇 Commodities":
        await update.message.reply_text(
            "🥇 Commodities Menu\n\n"
            "XAUUSD\n"
            "XAGUSD\n"
            "USOIL"
        )

    # -------------------------
    # INDICES
    # -------------------------

    elif text == "📊 Indices":
        await update.message.reply_text(
            "📊 Indices Menu\n\n"
            "NAS100\n"
            "US30\n"
            "SPX500"
        )

    # -------------------------
    # MY ALERTS
    # -------------------------

    elif text == "📋 My Alerts":
        await update.message.reply_text(
            "📋 No alerts yet."
        )

    # -------------------------
    # BROKER SETTINGS
    # -------------------------

    elif text == "🏦 Broker Settings":
        await update.message.reply_text(
            "🏦 Broker Settings\n\n"
            "FXCM: Demo account\n"
            "Crypto: Binance\n\n"
            "Connection setup will be added next."
        )

    # -------------------------
    # REMOVE ALERT
    # -------------------------

    elif text == "🗑 Remove Alert":
        await update.message.reply_text(
            "🗑 Remove Alert\n\n"
            "No alerts available."
        )

    # -------------------------
    # STATUS
    # -------------------------

    elif text == "ℹ️ Status":

        fxcm_status = (
            "🟢 FXCM credentials configured"
            if FXCM_USERNAME and FXCM_PASSWORD
            else "🔴 FXCM credentials missing"
        )

        await update.message.reply_text(
            "🟢 Server Online\n\n"
            f"{fxcm_status}\n"
            "🟡 FXCM API connection: Not tested yet"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing from Railway Variables."
        )

    if not FXCM_USERNAME:
        print("⚠️ FXCM_USERNAME is missing.")

    if not FXCM_PASSWORD:
        print("⚠️ FXCM_PASSWORD is missing.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu_handler
        )
    )

    print("🚀 Bot started...")

    app.run_polling()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    main()

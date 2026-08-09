import os
import requests

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)


BOT_TOKEN = os.getenv("BOT_TOKEN")
FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")

FXCM_BASE = "https://endpoints-demo.fxcm.com"


main_menu = [
    ["📈 Add Alert", "📋 My Alerts"],
    ["🏦 Broker Settings", "🗑 Remove Alert"],
    ["ℹ️ Status"]
]


market_menu = [
    ["💱 Forex", "🪙 Crypto"],
    ["🥇 Commodities", "📊 Indices"]
]


forex_menu = [
    ["EURUSD", "GBPUSD"],
    ["USDJPY", "GBPJPY"],
    ["⬅️ Back"]
]



def fxcm_login():

    session = requests.Session()

    response = session.get(
        f"{FXCM_BASE}/iam/trading-systems/{FXCM_USERNAME}",
        headers={
            "X-COOKIE-DOMAIN": "fxcm.com"
        },
        timeout=20
    )

    response.raise_for_status()

    systems = response.json()

    if not systems:
        raise Exception("No FXCM trading system found")


    trading_session_id = systems[0]["tradingSessionId"]
    trading_session_sub_id = systems[0]["tradingSessionSubId"]


    xsrf = session.cookies.get("XSRF-TOKEN")

    if not xsrf:
        raise Exception("Missing XSRF token")


    auth = session.post(

        f"{FXCM_BASE}/iam/authenticate",

        json={
            "loginId": FXCM_USERNAME,
            "password": FXCM_PASSWORD,
            "tradingSessionId": trading_session_id,
            "tradingSessionSubId": trading_session_sub_id,
            "appName": "TelegramTradingAlertBot"
        },

        headers={
            "X-COOKIE-DOMAIN": "fxcm.com",
            "X-XSRF-TOKEN": xsrf
        },

        timeout=20
    )


    auth.raise_for_status()

    data = auth.json()

    token = data.get("accessToken")


    if not token:
        raise Exception("FXCM token missing")


    return token



def fxcm_connection_test():

    fxcm_login()

    return True



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "🚀 Universal Trading Alert Platform",

        reply_markup=ReplyKeyboardMarkup(
            main_menu,
            resize_keyboard=True
        )
    )



async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if text == "📈 Add Alert":

        await update.message.reply_text(

            "🌍 Select Market",

            reply_markup=ReplyKeyboardMarkup(
                market_menu,
                resize_keyboard=True
            )
        )


    elif text == "💱 Forex":

        await update.message.reply_text(

            "💱 Select Forex Pair",

            reply_markup=ReplyKeyboardMarkup(
                forex_menu,
                resize_keyboard=True
            )
        )


    elif text in [
        "EURUSD",
        "GBPUSD",
        "USDJPY",
        "GBPJPY"
    ]:

        context.user_data["symbol"] = text

        await update.message.reply_text(

            f"📊 {text} Selected\n\n"
            "Enter alert price:"
        )


    elif text == "⬅️ Back":

        await update.message.reply_text(

            "🌍 Select Market",

            reply_markup=ReplyKeyboardMarkup(
                market_menu,
                resize_keyboard=True
            )
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


    elif text == "📋 My Alerts":

        await update.message.reply_text(
            "📋 No alerts created."
        )


    elif text == "🏦 Broker Settings":

        await update.message.reply_text(

            "🏦 Broker Settings\n\n"
            "FXCM Demo: 🟢 Connected\n"
            "Crypto: Binance"
        )


    elif text == "🗑 Remove Alert":

        await update.message.reply_text(
            "🗑 No alerts available."
        )


    elif text == "ℹ️ Status":

        try:

            fxcm_connection_test()

            await update.message.reply_text(

                "🟢 Server Online\n\n"
                "🟢 FXCM Credentials OK\n"
                "🟢 FXCM Authentication OK\n\n"
                "Ready for market data connection."
            )


        except Exception as e:

            await update.message.reply_text(

                "🔴 FXCM Connection Failed\n\n"
                f"{str(e)}"
            )


    else:

        if "symbol" in context.user_data:

            symbol = context.user_data["symbol"]

            context.user_data["alert_price"] = text

            await update.message.reply_text(

                "✅ Alert Saved\n\n"
                f"Pair: {symbol}\n"
                f"Price: {text}\n\n"
                "Monitoring will start soon."
            )



def main():

    if not BOT_TOKEN:
        raise Exception("BOT_TOKEN missing")

    if not FXCM_USERNAME:
        raise Exception("FXCM_USERNAME missing")

    if not FXCM_PASSWORD:
        raise Exception("FXCM_PASSWORD missing")


    app = Application.builder().token(BOT_TOKEN).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu_handler
        )
    )


    print("🚀 Bot started...")

    app.run_polling()



if __name__ == "__main__":
    main()

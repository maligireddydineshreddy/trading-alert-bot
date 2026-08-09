import os
import requests

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


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
        raise Exception("Missing FXCM security token")

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
        raise Exception("No FXCM access token received")

    return token


def get_fxcm_price():

    token = fxcm_login()

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # FXCM API test endpoint
    url = "https://api-demo.fxcm.com:443"

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    return response.text



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
            "💱 Forex Menu\n\n"
            "EURUSD\n"
            "GBPUSD\n"
            "USDJPY\n"
            "GBPJPY"
        )


    elif text == "🪙 Crypto":

        await update.message.reply_text(
            "🪙 Crypto Menu\n\n"
            "BTCUSDT\n"
            "ETHUSDT"
        )


    elif text == "🥇 Commodities":

        await update.message.reply_text(
            "🥇 Commodities Menu\n\n"
            "XAUUSD\n"
            "XAGUSD\n"
            "USOIL"
        )


    elif text == "📊 Indices":

        await update.message.reply_text(
            "📊 Indices Menu\n\n"
            "NAS100\n"
            "US30\n"
            "SPX500"
        )


    elif text == "📋 My Alerts":

        await update.message.reply_text(
            "📋 No alerts yet."
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

            fxcm_login()

            price = get_fxcm_price()

            await update.message.reply_text(
                "🟢 Server Online\n\n"
                "🟢 FXCM API connected\n\n"
                "📊 FXCM Market Test:\n"
                f"{price[:500]}"
            )


        except Exception as e:

            await update.message.reply_text(
                "🟢 Server Online\n\n"
                "🔴 FXCM test failed\n\n"
                f"{str(e)}"
            )



def main():

    if not BOT_TOKEN:
        raise Exception("Missing BOT_TOKEN")

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



if __name__ == "__main__":
    main()

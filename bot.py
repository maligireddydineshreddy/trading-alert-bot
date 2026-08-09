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


def test_fxcm():
    if not FXCM_USERNAME or not FXCM_PASSWORD:
        return False, "FXCM credentials missing"

    session = requests.Session()

    try:
        # Step 1: Get FXCM trading session information
        url = f"{FXCM_BASE}/iam/trading-systems/{FXCM_USERNAME}"

        response = session.get(
            url,
            headers={
                "X-COOKIE-DOMAIN": "fxcm.com"
            },
            timeout=20
        )

        response.raise_for_status()

        systems = response.json()

        if not systems:
            return False, "No FXCM trading session returned"

        trading_session_id = systems[0]["tradingSessionId"]
        trading_session_sub_id = systems[0]["tradingSessionSubId"]

        # Get XSRF token from cookies
        xsrf_token = session.cookies.get("XSRF-TOKEN")

        if not xsrf_token:
            return False, "FXCM XSRF token was not returned"

        # Step 2: Authenticate
        auth_url = f"{FXCM_BASE}/iam/authenticate"

        payload = {
            "loginId": FXCM_USERNAME,
            "password": FXCM_PASSWORD,
            "tradingSessionId": trading_session_id,
            "tradingSessionSubId": trading_session_sub_id,
            "appName": "TelegramTradingAlertBot"
        }

        auth_response = session.post(
            auth_url,
            json=payload,
            headers={
                "X-COOKIE-DOMAIN": "fxcm.com",
                "X-XSRF-TOKEN": xsrf_token
            },
            timeout=20
        )

        auth_response.raise_for_status()

        data = auth_response.json()

        if data.get("accessToken"):
            return True, "FXCM authentication successful"

        return False, "FXCM did not return an access token"

    except requests.exceptions.HTTPError as e:
        return False, f"FXCM HTTP error: {e}"

    except Exception as e:
        return False, f"FXCM connection error: {e}"


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
            "FXCM: Demo account\n"
            "Crypto: Binance"
        )

    elif text == "🗑 Remove Alert":
        await update.message.reply_text(
            "🗑 Remove Alert\n\n"
            "No alerts available."
        )

    elif text == "ℹ️ Status":
        fxcm_status = (
            "🟢 FXCM credentials configured"
            if FXCM_USERNAME and FXCM_PASSWORD
            else "🔴 FXCM credentials missing"
        )

        success, message = test_fxcm()

        if success:
            api_status = "🟢 FXCM API connected"
        else:
            api_status = f"🔴 FXCM API failed\n{message}"

        await update.message.reply_text(
            "🟢 Server Online\n\n"
            f"{fxcm_status}\n"
            f"{api_status}"
        )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

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

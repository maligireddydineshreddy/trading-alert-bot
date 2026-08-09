import os
import requests

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


BOT_TOKEN = os.getenv("BOT_TOKEN")
FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")

FXCM_BASE = "https://endpoints-demo.fxcm.com"
FXCM_MARKET = "https://api-demo.fxcm.com"


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
    """Login to FXCM and return session + access token."""

    session = requests.Session()

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
        raise RuntimeError("FXCM returned no trading session.")

    trading_session_id = systems[0]["tradingSessionId"]
    trading_session_sub_id = systems[0]["tradingSessionSubId"]

    xsrf_token = session.cookies.get("XSRF-TOKEN")

    if not xsrf_token:
        raise RuntimeError("FXCM XSRF token was not returned.")

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

    auth_data = auth_response.json()

    access_token = auth_data.get("accessToken")

    if not access_token:
        raise RuntimeError("FXCM did not return an access token.")

    return access_token


def get_fxcm_price(symbol="EUR/USD"):
    """Get current FXCM Bid/Ask price."""

    access_token = fxcm_login()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    # Subscribe the symbol so it appears in FXCM's Offers table.
    subscription_response = requests.post(
        f"{FXCM_MARKET}/trading/update_subscriptions",
        headers=headers,
        data={
            "symbol": symbol,
            "visible": "true"
        },
        timeout=20
    )

    subscription_response.raise_for_status()

    # Request current Offers snapshot.
    response = requests.get(
        f"{FXCM_MARKET}/trading/get_model",
        headers=headers,
        params={
            "models": "Offer"
        },
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    offers = data.get("offers", [])

    for offer in offers:

        if offer.get("currency") == symbol:

            bid = offer.get("sell")
            ask = offer.get("buy")

            return {
                "symbol": symbol,
                "bid": bid,
                "ask": ask,
                "spread": offer.get("spread"),
                "time": offer.get("time")
            }

    raise RuntimeError(
        f"{symbol} was not found in the FXCM Offers table."
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🚀 Universal Trading Alert Platform",
        reply_markup=ReplyKeyboardMarkup(
            main_menu,
            resize_keyboard=True
        )
    )


async def menu_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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
            "FXCM: 🟢 Connected\n"
            "Crypto: Binance\n"
        )

    elif text == "🗑 Remove Alert":

        await update.message.reply_text(
            "🗑 Remove Alert\n\n"
            "No alerts available."
        )

    elif text == "ℹ️ Status":

        try:

            price = get_fxcm_price("EUR/USD")

            await update.message.reply_text(
                "🟢 Server Online\n\n"
                "🟢 FXCM credentials configured\n"
                "🟢 FXCM API connected\n\n"
                "📊 EUR/USD\n"
                f"Bid: {price['bid']}\n"
                f"Ask: {price['ask']}\n"
                f"Spread: {price['spread']}"
            )

        except Exception as e:

            await update.message.reply_text(
                "🟢 Server Online\n\n"
                "🟢 FXCM credentials configured\n"
                "🔴 FXCM price request failed\n\n"
                f"Error: {str(e)}"
            )


def main():

    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing.")

    if not FXCM_USERNAME:
        raise RuntimeError("FXCM_USERNAME is missing.")

    if not FXCM_PASSWORD:
        raise RuntimeError("FXCM_PASSWORD is missing.")

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

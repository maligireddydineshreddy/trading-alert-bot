import os
import asyncio

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from database import (
    init_db,
    add_alert,
    get_user_alerts,
    remove_alert
)

from fxcm import get_price

import monitor


BOT_TOKEN = os.getenv("BOT_TOKEN")


# ==========================
# MENUS
# ==========================

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


# ==========================
# START COMMAND
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🚀 Universal Trading Alert Platform",
        reply_markup=ReplyKeyboardMarkup(
            main_menu,
            resize_keyboard=True
        )
    )


# ==========================
# MENU HANDLER
# ==========================

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.message.from_user.id


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
            "Enter target price:"
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
            "🪙 Crypto\n\nBTCUSDT\nETHUSDT"
        )


    elif text == "🥇 Commodities":

        await update.message.reply_text(
            "🥇 Commodities\n\nXAUUSD\nXAGUSD\nUSOIL"
        )


    elif text == "📊 Indices":

        await update.message.reply_text(
            "📊 Indices\n\nNAS100\nUS30\nSPX500"
        )


    elif text == "📋 My Alerts":

        alerts = get_user_alerts(user_id)


        if not alerts:

            await update.message.reply_text(
                "📋 No active alerts."
            )

        else:

            msg = "📋 Your Alerts:\n\n"

            for a in alerts:

                msg += (
                    f"ID: {a[0]}\n"
                    f"{a[2]} → {a[3]}\n"
                    f"Status: {a[4]}\n\n"
                )

            await update.message.reply_text(msg)



    elif text == "🗑 Remove Alert":

        context.user_data["remove"] = True

        await update.message.reply_text(
            "Send alert ID:"
        )


    elif text == "🏦 Broker Settings":

        await update.message.reply_text(
            "🏦 Broker Settings\n\n"
            "FXCM Demo 🟢 Connected\n"
            "Binance 🟡 Pending"
        )


    elif text == "ℹ️ Status":

        try:

            price = get_price("EURUSD")

            await update.message.reply_text(
                "🟢 Server Online\n\n"
                "🟢 FXCM Connected\n\n"
                f"EURUSD\n"
                f"Bid: {price['bid']}\n"
                f"Ask: {price['ask']}"
            )

        except Exception as e:

            await update.message.reply_text(
                f"🔴 FXCM Error\n\n{e}"
            )


    elif context.user_data.get("remove"):

        try:

            remove_alert(int(text))

            context.user_data.clear()

            await update.message.reply_text(
                "🗑 Alert removed."
            )

        except:

            await update.message.reply_text(
                "❌ Invalid ID"
            )


    elif "symbol" in context.user_data:

        try:

            price = float(text)

            add_alert(
                user_id,
                context.user_data["symbol"],
                price
            )

            await update.message.reply_text(
                "✅ Alert Saved\n\n"
                f"Pair: {context.user_data['symbol']}\n"
                f"Target: {price}\n\n"
                "Monitoring started 🚀"
            )

            context.user_data.clear()


        except:

            await update.message.reply_text(
                "❌ Enter valid price"
            )


# ==========================
# START MONITOR
# ==========================

async def start_monitor(app):

    print(
        "📡 Starting monitor...",
        flush=True
    )

    monitor.telegram_bot = app.bot

    asyncio.create_task(
        monitor.monitor_loop()
    )


# ==========================
# MAIN
# ==========================

def main():

    print("STEP 1", flush=True)


    if not BOT_TOKEN:

        raise Exception(
            "BOT_TOKEN missing"
        )


    print("STEP 2", flush=True)


    init_db()


    print("STEP 3", flush=True)


    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .post_init(start_monitor)
        .build()
    )


    print("STEP 4", flush=True)


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


    print(
        "🚀 Bot Started",
        flush=True
    )


    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":

    main()

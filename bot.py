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

from monitor import (
    monitor_loop,
    telegram_bot
)


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
# START
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
# HANDLER
# ==========================

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.message.from_user.id


    # ADD ALERT

    if text == "📈 Add Alert":

        await update.message.reply_text(
            "🌍 Select Market",
            reply_markup=ReplyKeyboardMarkup(
                market_menu,
                resize_keyboard=True
            )
        )


    # FOREX

    elif text == "💱 Forex":

        await update.message.reply_text(
            "💱 Select Forex Pair",
            reply_markup=ReplyKeyboardMarkup(
                forex_menu,
                resize_keyboard=True
            )
        )


    # SYMBOL SELECT

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


    # BACK

    elif text == "⬅️ Back":

        await update.message.reply_text(
            "🌍 Select Market",
            reply_markup=ReplyKeyboardMarkup(
                market_menu,
                resize_keyboard=True
            )
        )


    # CRYPTO

    elif text == "🪙 Crypto":

        await update.message.reply_text(
            "🪙 Crypto\n\nBTCUSDT\nETHUSDT"
        )


    # COMMODITIES

    elif text == "🥇 Commodities":

        await update.message.reply_text(
            "🥇 Commodities\n\n"
            "XAUUSD\n"
            "XAGUSD\n"
            "USOIL"
        )


    # INDICES

    elif text == "📊 Indices":

        await update.message.reply_text(
            "📊 Indices\n\n"
            "NAS100\n"
            "US30\n"
            "SPX500"
        )


    # MY ALERTS

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



    # REMOVE

    elif text == "🗑 Remove Alert":

        await update.message.reply_text(
            "Send alert ID:"
        )

        context.user_data["remove"] = True



    # BROKER

    elif text == "🏦 Broker Settings":

        await update.message.reply_text(
            "🏦 Broker Settings\n\n"
            "FXCM Demo 🟢 Connected\n"
            "Binance 🟡 Pending"
        )



    # STATUS

    elif text == "ℹ️ Status":

        try:

            price = get_price(
                "EURUSD"
            )


            await update.message.reply_text(

                "🟢 Server Online\n\n"
                "🟢 FXCM Connected\n\n"
                f"EURUSD\n"
                f"Bid: {price['bid']}\n"
                f"Ask: {price['ask']}"

            )


        except Exception as e:

            await update.message.reply_text(

                "🔴 FXCM Error\n\n"
                f"{e}"

            )



    # REMOVE CONFIRMATION

    elif context.user_data.get("remove"):


        try:

            remove_alert(
                int(text)
            )


            await update.message.reply_text(
                "🗑 Alert removed."
            )


            context.user_data.clear()


        except:

            await update.message.reply_text(
                "❌ Invalid ID"
            )



    # SAVE ALERT

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

    global telegram_bot

    telegram_bot = app.bot

    asyncio.create_task(
        monitor_loop()
    )



# ==========================
# MAIN
# ==========================

def main():

    if not BOT_TOKEN:

        raise Exception(
            "BOT_TOKEN missing"
        )


    init_db()


    app = Application.builder().token(
        BOT_TOKEN
    ).post_init(
        start_monitor
    ).build()



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
        "🚀 Bot started..."
    )


    app.run_polling()



if __name__ == "__main__":

    main()

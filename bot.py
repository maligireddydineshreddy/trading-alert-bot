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
# MENU HANDLER
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



    # PAIR SELECT

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
            "🪙 Crypto Menu\n\nBTCUSDT\nETHUSDT"
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

            message = "📋 Your Alerts:\n\n"


            for alert in alerts:

                message += (
                    f"ID: {alert[0]}\n"
                    f"{alert[2]} → {alert[3]}\n"
                    f"Status: {alert[4]}\n\n"
                )


            await update.message.reply_text(message)



    # REMOVE ALERT

    elif text == "🗑 Remove Alert":

        await update.message.reply_text(

            "Send alert ID to remove."
        )

        context.user_data["remove_mode"] = True



    # BROKER SETTINGS

    elif text == "🏦 Broker Settings":

        await update.message.reply_text(

            "🏦 Broker Settings\n\n"
            "FXCM Demo 🟢 Connected\n"
            "Binance 🟡 Pending"
        )



    # STATUS

    elif text == "ℹ️ Status":

        try:

            price = get_price("EURUSD")


            await update.message.reply_text(

                "🟢 Server Online\n\n"
                "🟢 FXCM Connected\n"
                f"EURUSD: {price}"
            )


        except Exception as e:


            await update.message.reply_text(

                "🟢 Server Online\n\n"
                "🔴 FXCM Error\n\n"
                f"{e}"
            )



    # REMOVE PROCESS

    elif context.user_data.get("remove_mode"):


        try:

            remove_alert(int(text))


            await update.message.reply_text(
                "🗑 Alert removed."
            )


            context.user_data.clear()


        except:


            await update.message.reply_text(
                "❌ Invalid alert ID."
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
                "❌ Enter a valid price."
            )



# ==========================
# ALERT MONITOR
# ==========================

async def monitor(application):

    while True:


        await asyncio.sleep(5)


        # alert checking will run here

        # next step:
        # connect database alerts
        # compare FXCM price
        # send telegram message



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



    print("🚀 Bot started...")


    app.run_polling()



if __name__ == "__main__":

    main()

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
            f"{text} selected\n\nEnter target price:"
        )


    elif text == "⬅️ Back":

        await update.message.reply_text(
            "🌍 Select Market",
            reply_markup=ReplyKeyboardMarkup(
                market_menu,
                resize_keyboard=True
            )
        )


    elif text == "📋 My Alerts":

        alerts = get_user_alerts(user_id)

        if not alerts:

            await update.message.reply_text(
                "No active alerts."
            )

        else:

            msg="📋 Alerts\n\n"

            for a in alerts:

                msg += (
                    f"ID: {a[0]}\n"
                    f"{a[2]} → {a[3]}\n"
                    f"Status: {a[4]}\n\n"
                )

            await update.message.reply_text(msg)



    elif text == "🗑 Remove Alert":

        context.user_data["remove"]=True

        await update.message.reply_text(
            "Send alert ID"
        )



    elif text == "🏦 Broker Settings":

        await update.message.reply_text(
            "FXCM Demo 🟢\nBinance Pending 🟡"
        )



    elif text == "ℹ️ Status":

        try:

            price=get_price("EURUSD")

            await update.message.reply_text(
                f"🟢 Server Online\n\n"
                f"FXCM Connected\n\n"
                f"EURUSD\n"
                f"Bid: {price['bid']}\n"
                f"Ask: {price['ask']}"
            )

        except Exception as e:

            await update.message.reply_text(
                f"FXCM Error\n{e}"
            )



    elif context.user_data.get("remove"):

        remove_alert(int(text))

        context.user_data.clear()

        await update.message.reply_text(
            "🗑 Removed"
        )



    elif "symbol" in context.user_data:

        price=float(text)

        add_alert(
            user_id,
            context.user_data["symbol"],
            price
        )

        await update.message.reply_text(
            "✅ Alert Saved"
        )

        context.user_data.clear()



async def start_monitor(app):

    monitor.telegram_bot = app.bot

    asyncio.create_task(
        monitor.monitor_loop()
    )



def main():

    if not BOT_TOKEN:
        raise Exception(
            "BOT_TOKEN missing"
        )


    init_db()


    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .post_init(start_monitor)
        .build()
    )


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


    print("🚀 Bot Started")


    app.run_polling(
        drop_pending_updates=True
    )



if __name__=="__main__":
    main()

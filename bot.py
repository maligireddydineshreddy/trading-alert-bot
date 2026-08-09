import os
import asyncio


from telegram import (
    ReplyKeyboardMarkup,
    Update
)


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


from fxcm import (
    get_price,
    validate_symbol
)


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

    ["✏️ Enter Pair"],

    ["⬅️ Back"]

]



crypto_menu = [

    ["BTCUSDT", "ETHUSDT"],

    ["SOLUSDT", "XRPUSDT"],

    ["✍️ Enter Pair"],

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



    # FOREX MENU

    elif text == "💱 Forex":


        await update.message.reply_text(

            "💱 Select Forex Pair\n\n"
            "Or enter any FXCM pair manually",

            reply_markup=ReplyKeyboardMarkup(

                forex_menu,

                resize_keyboard=True

            )

        )



    # CRYPTO MENU

    elif text == "🪙 Crypto":


        await update.message.reply_text(

            "🪙 Select Crypto Pair",

            reply_markup=ReplyKeyboardMarkup(

                crypto_menu,

                resize_keyboard=True

            )

        )



    # MANUAL FOREX INPUT MODE

    elif text == "✏️ Enter Pair":


        context.user_data["custom_symbol"] = True


        await update.message.reply_text(

            "✏️ Enter Forex symbol\n\n"

            "Examples:\n"
            "AUDUSD\n"
            "AUD/USD\n"
            "EURJPY\n"
            "USDCHF"

        )



    # BUTTON SYMBOLS

    elif text in [

        "EURUSD",
        "GBPUSD",
        "USDJPY",
        "GBPJPY",

        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT"

    ]:


        context.user_data["symbol"] = text


        await update.message.reply_text(

            f"📊 {text} Selected\n\n"
            "Enter target price:"

        )

    # BACK BUTTON

    elif text == "⬅️ Back":


        await update.message.reply_text(

            "🌍 Select Market",

            reply_markup=ReplyKeyboardMarkup(

                market_menu,

                resize_keyboard=True

            )

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




    # REMOVE ALERT

    elif text == "🗑 Remove Alert":


        context.user_data["remove"] = True


        await update.message.reply_text(

            "Send alert ID:"

        )




    # BROKER SETTINGS

    elif text == "🏦 Broker Settings":


        await update.message.reply_text(

            "🏦 Broker Settings\n\n"

            "FXCM Demo 🟢 Connected\n"

            "Binance 🟢 Connected"

        )




    # STATUS

    elif text == "ℹ️ Status":


        try:


            price = get_price("EURUSD")


            await update.message.reply_text(

                "🟢 Server Online\n\n"

                "🟢 FXCM Connected\n"

                "🟢 Binance Connected\n\n"

                f"EURUSD\n"

                f"Bid: {price['bid']}\n"

                f"Ask: {price['ask']}"

            )


        except Exception as e:


            await update.message.reply_text(

                f"🔴 Error\n\n{e}"

            )




    # MANUAL SYMBOL VALIDATION

    elif context.user_data.get("custom_symbol"):


        symbol = text.upper().replace("/", "")


        try:


            valid = validate_symbol(symbol)


            if not valid:


                await update.message.reply_text(

                    "❌ Invalid symbol\n\n"

                    "This pair is not available on FXCM."

                )

                return



            context.user_data.pop(
                "custom_symbol"
            )


            context.user_data["symbol"] = symbol


            await update.message.reply_text(

                f"📊 {symbol} Selected\n\n"

                "Enter target price:"

            )


        except Exception as e:


            await update.message.reply_text(

                f"❌ Symbol check failed\n\n{e}"

            )




    # REMOVE PROCESS

    elif context.user_data.get("remove"):


        try:


            remove_alert(

                int(text)

            )


            context.user_data.clear()


            await update.message.reply_text(

                "🗑 Alert removed."

            )


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


    print(

        "📡 Starting monitor...",

        flush=True

    )


    monitor.set_bot(

        app.bot

    )


    asyncio.create_task(

        monitor.monitor_loop()

    )





# ==========================
# MAIN
# ==========================


def main():


    print(
        "STEP 1",
        flush=True
    )


    if not BOT_TOKEN:

        raise Exception(
            "BOT_TOKEN missing"
        )


    print(
        "STEP 2",
        flush=True
    )


    init_db()


    print(
        "STEP 3",
        flush=True
    )


    app = (

        Application

        .builder()

        .token(BOT_TOKEN)

        .post_init(start_monitor)

        .build()

    )


    print(
        "STEP 4",
        flush=True
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



    print(

        "🚀 Bot Started",

        flush=True

    )



    app.run_polling(

        drop_pending_updates=True,

        allowed_updates=Update.ALL_TYPES

    )





if __name__ == "__main__":

    main()

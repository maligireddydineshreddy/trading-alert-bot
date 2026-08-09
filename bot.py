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


from crypto import (
    validate_crypto
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





# ==========================
# FOREX MENU
# ==========================


forex_menu = [

    ["EURUSD", "GBPUSD"],

    ["USDJPY", "GBPJPY"],

    ["✏️ Enter Forex Pair"],

    ["⬅️ Back"]

]





# ==========================
# CRYPTO MENU
# ==========================


crypto_menu = [

    ["BTCUSDT", "ETHUSDT"],

    ["SOLUSDT", "XRPUSDT"],

    ["✍️ Enter Crypto Pair"],

    ["⬅️ Back"]

]





# ==========================
# COMMODITY MENU
# ==========================


commodity_menu = [

    ["XAUUSD", "XAGUSD"],

    ["USOIL", "COPPER"],

    ["✍️ Enter Commodity"],

    ["⬅️ Back"]

]





# ==========================
# INDICES MENU
# ==========================


indices_menu = [

    ["SPX500", "NAS100"],

    ["US30", "US100"],

    ["✏️ Enter Index"],

    ["⬅️ Back"]

]





# ==========================
# HOT SYMBOLS
# ==========================


HOT_SYMBOLS = [

    # Forex
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "GBPJPY",


    # Crypto
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",


    # Commodities
    "XAUUSD",
    "XAGUSD",
    "USOIL",
    "COPPER",


    # Indices
    "SPX500",
    "NAS100",
    "US30",
    "US100"

]





# ==========================
# START COMMAND
# ==========================


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


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


async def menu_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    text = update.message.text

    user_id = update.message.from_user.id




    # ==========================
    # ADD ALERT
    # ==========================


    if text == "📈 Add Alert":


        await update.message.reply_text(

            "🌍 Select Market",

            reply_markup=ReplyKeyboardMarkup(

                market_menu,

                resize_keyboard=True

            )

        )




    # ==========================
    # FOREX
    # ==========================


    elif text == "💱 Forex":


        context.user_data["market"] = "forex"


        await update.message.reply_text(

            "💱 Select Forex Pair\n\n"
            "Or enter any FXCM pair manually",

            reply_markup=ReplyKeyboardMarkup(

                forex_menu,

                resize_keyboard=True

            )

        )





    # ==========================
    # CRYPTO
    # ==========================


    elif text == "🪙 Crypto":


        context.user_data["market"] = "crypto"


        await update.message.reply_text(

            "🪙 Select Crypto Pair\n\n"
            "Or enter Binance pair manually",

            reply_markup=ReplyKeyboardMarkup(

                crypto_menu,

                resize_keyboard=True

            )

        )





    # ==========================
    # COMMODITIES
    # ==========================


    elif text == "🥇 Commodities":


        context.user_data["market"] = "commodity"


        await update.message.reply_text(

            "🥇 Select Commodity\n\n"
            "Or enter FXCM symbol manually",

            reply_markup=ReplyKeyboardMarkup(

                commodity_menu,

                resize_keyboard=True

            )

        )





    # ==========================
    # INDICES
    # ==========================


    elif text == "📊 Indices":


        context.user_data["market"] = "indices"


        await update.message.reply_text(

            "📊 Select Index\n\n"
            "Or enter FXCM symbol manually",

            reply_markup=ReplyKeyboardMarkup(

                indices_menu,

                resize_keyboard=True

            )

        )





    # ==========================
    # MANUAL INPUT
    # ==========================


    elif text in [

        "✏️ Enter Forex Pair",

        "✍️ Enter Crypto Pair",

        "✍️ Enter Commodity",

        "✏️ Enter Index"

    ]:


        context.user_data["custom_symbol"] = True



        if text == "✍️ Enter Crypto Pair":


            context.user_data["market"] = "crypto"


            await update.message.reply_text(

                "🪙 Enter Crypto Symbol\n\n"

                "Examples:\n"
                "BNBUSDT\n"
                "DOGEUSDT\n"
                "ADAUSDT"

            )



        elif text == "✏️ Enter Index":


            context.user_data["market"] = "indices"


            await update.message.reply_text(

                "📊 Enter Index Symbol\n\n"

                "Examples:\n"
                "GER30\n"
                "UK100\n"
                "JPN225"

            )



        elif text == "✍️ Enter Commodity":


            context.user_data["market"] = "commodity"


            await update.message.reply_text(

                "🥇 Enter Commodity Symbol\n\n"

                "Examples:\n"
                "NATGAS\n"
                "COFFEE\n"
                "PLATINUM"

            )



        else:


            context.user_data["market"] = "forex"


            await update.message.reply_text(

                "💱 Enter Forex Pair\n\n"

                "Examples:\n"
                "AUDUSD\n"
                "AUD/USD\n"
                "EURJPY"

            )





    # ==========================
    # HOT BUTTON SYMBOLS
    # ==========================


    elif text in HOT_SYMBOLS:


        context.user_data["symbol"] = text



        await update.message.reply_text(

            f"📊 {text} Selected\n\n"

            "Enter target price:"

        )





    # ==========================
    # BACK
    # ==========================


    elif text == "⬅️ Back":


        await update.message.reply_text(

            "🌍 Select Market",

            reply_markup=ReplyKeyboardMarkup(

                market_menu,

                resize_keyboard=True

            )

        )





    # ==========================
    # MY ALERTS
    # ==========================


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





    # ==========================
    # REMOVE ALERT
    # ==========================


    elif text == "🗑 Remove Alert":


        context.user_data["remove"] = True


        await update.message.reply_text(

            "Send alert ID:"

        )

    # ==========================
    # BROKER SETTINGS
    # ==========================


    elif text == "🏦 Broker Settings":


        await update.message.reply_text(

            "🏦 Broker Settings\n\n"

            "🟢 FXCM Connected\n"

            "🟢 Binance Connected"

        )





    # ==========================
    # STATUS
    # ==========================


    elif text == "ℹ️ Status":


        try:


            price = get_price("EURUSD")



            await update.message.reply_text(

                "🟢 Server Online\n\n"

                "🟢 FXCM Connected\n"

                "🟢 Binance Connected\n\n"

                "EURUSD\n"

                f"Bid: {price['bid']}\n"

                f"Ask: {price['ask']}"

            )


        except Exception as e:


            await update.message.reply_text(

                f"🔴 Error\n\n{e}"

            )






    # ==========================
    # CUSTOM SYMBOL VALIDATION
    # ==========================


    elif context.user_data.get("custom_symbol"):


        symbol = text.upper().replace("/", "")


        market = context.user_data.get(
            "market"
        )



        try:


            if market == "crypto":


                valid = validate_crypto(symbol)



            else:


                # Forex + Commodities + Indices
                # FXCM validation

                valid = validate_symbol(symbol)




            if not valid:


                await update.message.reply_text(

                    "❌ Invalid Symbol\n\n"

                    "Symbol not available."

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

                f"❌ Validation Error\n\n{e}"

            )






    # ==========================
    # REMOVE ALERT PROCESS
    # ==========================


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

                "❌ Invalid Alert ID"

            )






    # ==========================
    # SAVE ALERT
    # ==========================


    elif "symbol" in context.user_data:


        try:


            target = float(text)



            add_alert(

                user_id,

                context.user_data["symbol"],

                target

            )



            await update.message.reply_text(

                "✅ Alert Saved\n\n"

                f"Symbol: {context.user_data['symbol']}\n"

                f"Target: {target}\n\n"

                "🚀 Monitoring Started"

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


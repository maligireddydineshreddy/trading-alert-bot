import os
import asyncio


from telegram import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update
)


from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)



from database import (
    init_db,
    add_alert,
    get_user_alerts,
    remove_multiple_alerts
)


from fxcm import (
    get_price,
    validate_symbol,
    init_fxcm
)


from crypto import (
    validate_crypto,
    get_crypto_price
)


import monitor




BOT_TOKEN = os.getenv("BOT_TOKEN")






# ==========================
# MAIN MENU
# ==========================


main_menu = [

    ["📈 Add Alert", "📋 My Alerts"],

    ["🏦 Broker Settings", "🗑 Remove Alert"],

    ["ℹ️ Status"]

]







# ==========================
# MARKET MENU
# ==========================


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


    context.user_data.clear()



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


        context.user_data.clear()



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
            "Or enter FXCM pair manually",

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
    # MANUAL SYMBOL INPUT
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




        elif text == "✍️ Enter Commodity":


            context.user_data["market"] = "commodity"


            await update.message.reply_text(

                "🥇 Enter Commodity Symbol\n\n"

                "Examples:\n"
                "NATGAS\n"
                "COFFEE\n"
                "PLATINUM"

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




        else:


            context.user_data["market"] = "forex"


            await update.message.reply_text(

                "💱 Enter Forex Symbol\n\n"

                "Examples:\n"
                "AUDUSD\n"
                "EURJPY\n"
                "AUD/USD"

            )







    # ==========================
    # HOT SYMBOL BUTTONS
    # ==========================


    elif text in HOT_SYMBOLS:


        context.user_data["symbol"] = text



        await update.message.reply_text(

            f"📊 {text} Selected\n\n"

            "Enter target price:"

        )







    # ==========================
    # BACK BUTTON
    # ==========================


    elif text == "⬅️ Back":


        context.user_data.clear()



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

            return





        msg = "📋 Your Active Alerts:\n\n"



        for a in alerts:


            msg += (

                f"🆔 ID: {a[0]}\n"

                f"📊 Symbol: {a[2]}\n"

                f"🎯 Target: {a[3]}\n"

                f"📈 Direction: {a[4]}\n\n"

            )



        await update.message.reply_text(msg)








# ==========================
# REMOVE ALERT MENU
# ==========================


    elif text == "🗑 Remove Alert":



        alerts = get_user_alerts(user_id)





        if not alerts:


            await update.message.reply_text(

                "📋 No active alerts to remove."

            )

            return






        buttons = []





        for alert in alerts:



            buttons.append(

                [

                    InlineKeyboardButton(

                        f"{alert[2]} | {alert[3]} | {alert[4]}",

                        callback_data=f"select_{alert[0]}"

                    )

                ]

            )







        buttons.append(

            [

                InlineKeyboardButton(

                    "🗑 Delete Selected",

                    callback_data="delete_selected"

                )

            ]

        )







        context.user_data["delete_list"] = []





        await update.message.reply_text(

            "🗑 Select alerts to remove:\n\n"

            "Tap alerts then press Delete Selected",

            reply_markup=InlineKeyboardMarkup(buttons)

        )









# ==========================
# INLINE CALLBACK HANDLER
# ==========================


async def delete_callback(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    data = query.data






    # SELECT / UNSELECT


    if data.startswith("select_"):



        alert_id = int(

            data.split("_")[1]

        )



        selected = context.user_data.get(

            "delete_list",

            []

        )





        if alert_id in selected:


            selected.remove(alert_id)


        else:


            selected.append(alert_id)





        context.user_data["delete_list"] = selected





        if selected:


            ids = "\n".join(

                str(x)

                for x in selected

            )

        else:

            ids = "None"





        await query.edit_message_text(

            "🗑 Selected Alert IDs:\n\n"

            f"{ids}\n\n"

            "Press Delete Selected."

        )







    # DELETE


    elif data == "delete_selected":



        selected = context.user_data.get(

            "delete_list",

            []

        )





        if not selected:


            await query.edit_message_text(

                "❌ No alerts selected."

            )

            return





        remove_multiple_alerts(

            selected

        )




        context.user_data.clear()





        await query.edit_message_text(

            "✅ Selected alerts removed."

        )









# ==========================
# SAVE ALERT
# ==========================


async def save_alert(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    user_id = update.message.from_user.id



    try:


        target = float(

            update.message.text

        )



        symbol = context.user_data.get(

            "symbol"

        )





        if not symbol:


            return







        # GET PRICE


        if symbol.endswith("USDT"):


            data = get_crypto_price(symbol)


            current_price = float(

                data["price"]

            )



        else:


            data = get_price(symbol)


            current_price = float(

                data["bid"]

            )







        # DIRECTION


        if current_price > target:


            direction = "BELOW"


        else:


            direction = "ABOVE"








        add_alert(

            user_id,

            symbol,

            target,

            direction

        )






        await update.message.reply_text(

            "✅ Alert Saved\n\n"

            f"📊 Symbol: {symbol}\n"

            f"💵 Current: {current_price}\n"

            f"🎯 Target: {target}\n"

            f"📈 Direction: {direction}\n\n"

            "🚀 Monitoring Started"

        )





        context.user_data.clear()





    except Exception as e:



        await update.message.reply_text(

            f"❌ Error creating alert\n\n{e}"

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
    "Connecting FXCM...",
    flush=True
    )

    init_fxcm()





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








    # ==========================
    # COMMANDS
    # ==========================


    app.add_handler(

        CommandHandler(

            "start",

            start

        )

    )








    # ==========================
    # INLINE BUTTONS
    # ==========================


    app.add_handler(

        CallbackQueryHandler(

            delete_callback

        )

    )








    # ==========================
    # SAVE TARGET PRICE
    # IMPORTANT:
    # Must come BEFORE menu handler
    # ==========================


    app.add_handler(

        MessageHandler(

            filters.Regex(r"^\d+(\.\d+)?$"),

            save_alert

        )

    )








    # ==========================
    # NORMAL MENU TEXT
    # ==========================


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

        drop_pending_updates=False,

        allowed_updates=Update.ALL_TYPES

    )









# ==========================
# RUN
# ==========================


if __name__ == "__main__":


    main()

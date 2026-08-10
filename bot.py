import requests
from datetime import datetime
from zoneinfo import ZoneInfo
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
    init_fxcm
)



from crypto import (
    get_crypto_price
)



import monitor





BOT_TOKEN = os.getenv("BOT_TOKEN")





# ==================================================
# MAIN MENU
# ==================================================


main_menu = [

    ["📈 Add Alert", "📋 My Alerts"],

    ["🗑 Remove Alert"],

    ["ℹ️ Status"]

]







# ==================================================
# MARKET MENU
# ==================================================


market_menu = [

    ["💱 Forex", "🪙 Crypto"],

    ["🥇 Commodities", "📊 Indices"],

    ["⬅️ Back"]

]








# ==================================================
# FOREX MENU
# ==================================================


forex_menu = [

    ["EURUSD", "GBPUSD"],

    ["USDJPY", "GBPJPY"],

    ["✏️ Enter Forex Pair"],

    ["⬅️ Back"]

]








# ==================================================
# CRYPTO MENU
# ==================================================


crypto_menu = [

    ["BTCUSDT", "ETHUSDT"],

    ["SOLUSDT", "XRPUSDT"],

    ["✍️ Enter Crypto Pair"],

    ["⬅️ Back"]

]








# ==================================================
# COMMODITY MENU
# ==================================================


commodity_menu = [

    ["XAUUSD", "XAGUSD"],

    ["USOIL", "COPPER"],

    ["✍️ Enter Commodity"],

    ["⬅️ Back"]

]








# ==================================================
# INDICES MENU
# ==================================================


indices_menu = [

    ["SPX500", "NAS100"],

    ["US30", "US100"],

    ["✏️ Enter Index"],

    ["⬅️ Back"]

]








# ==================================================
# HOT SYMBOLS
# ==================================================


HOT_SYMBOLS = [

    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "GBPJPY",


    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",


    "XAUUSD",
    "XAGUSD",
    "USOIL",
    "COPPER",


    "SPX500",
    "NAS100",
    "US30",
    "US100"

]








# ==================================================
# START COMMAND
# ==================================================


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
# ==================================================
# SYSTEM STATUS CHECK
# ==================================================

async def system_status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # ==========================
    # BOT STATUS
    # ==========================

    bot_status = "🟢 Bot: Online"



    # ==========================
    # FXCM LIVE CHECK
    # ==========================

    try:

        fxcm_check = get_price("EURUSD")


        if fxcm_check:

            eurusd_price = fxcm_check["bid"]

            fxcm_status = (
                "🟢 FXCM: Connected\n"
                f"💱 EURUSD: {eurusd_price}"
            )

        else:

            fxcm_status = (
                "🔴 FXCM: Disconnected"
            )


    except Exception:


        fxcm_status = (
            "🔴 FXCM: Disconnected"
        )





    # ==========================
    # BINANCE LIVE CHECK
    # ==========================

    try:


        response = requests.get(

            "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",

            timeout=5

        )


        data = response.json()


        btc_price = data["price"]


        binance_status = (

            "🟢 Binance: Connected\n"
            f"₿ BTCUSDT: {btc_price}"

        )



    except Exception:


        binance_status = (

            "🔴 Binance: Disconnected"

        )





    # ==========================
    # TIME
    # ==========================

   ist_time = datetime.now(
       ZoneInfo("Asia/Kolkata")
   )

   current_time = ist_time.strftime(
       "%d-%m-%Y %H:%M:%S"
   )





    message = f"""
ℹ️ System Status


{bot_status}


{fxcm_status}


{binance_status}


🕒 Last Update:
{current_time}
"""





    await update.message.reply_text(

        message,

        reply_markup=ReplyKeyboardMarkup(

            main_menu,

            resize_keyboard=True

        )

    )
# ==================================================
# MENU HANDLER
# ==================================================


async def menu_handler(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    text = update.message.text

    user_id = update.message.from_user.id





    # ==================================================
    # ADD ALERT
    # ==================================================


    if text == "📈 Add Alert":


        context.user_data.clear()



        await update.message.reply_text(

            "🌍 Select Market",

            reply_markup=ReplyKeyboardMarkup(

                market_menu,

                resize_keyboard=True

            )

        )







    # ==================================================
    # MARKET BACK BUTTON
    # ==================================================


    elif text == "⬅️ Back":


        context.user_data.clear()



        await update.message.reply_text(

            "🚀 Universal Trading Alert Platform",

            reply_markup=ReplyKeyboardMarkup(

                main_menu,

                resize_keyboard=True

            )

        )







    # ==================================================
    # FOREX
    # ==================================================


    elif text == "💱 Forex":


        context.user_data["market"] = "forex"



        await update.message.reply_text(

            "💱 Select Forex Pair",

            reply_markup=ReplyKeyboardMarkup(

                forex_menu,

                resize_keyboard=True

            )

        )








    # ==================================================
    # CRYPTO
    # ==================================================


    elif text == "🪙 Crypto":


        context.user_data["market"] = "crypto"



        await update.message.reply_text(

            "🪙 Select Crypto Pair",

            reply_markup=ReplyKeyboardMarkup(

                crypto_menu,

                resize_keyboard=True

            )

        )








    # ==================================================
    # COMMODITIES
    # ==================================================


    elif text == "🥇 Commodities":


        context.user_data["market"] = "commodity"



        await update.message.reply_text(

            "🥇 Select Commodity",

            reply_markup=ReplyKeyboardMarkup(

                commodity_menu,

                resize_keyboard=True

            )

        )








    # ==================================================
    # INDICES
    # ==================================================


    elif text == "📊 Indices":


        context.user_data["market"] = "indices"



        await update.message.reply_text(

            "📊 Select Index",

            reply_markup=ReplyKeyboardMarkup(

                indices_menu,

                resize_keyboard=True

            )

        )








    # ==================================================
    # SYMBOL SELECTED
    # ==================================================


    elif text in HOT_SYMBOLS:


        context.user_data["symbol"] = text



        price_keyboard = [

            ["⬅️ Back"]

        ]



        await update.message.reply_text(

            f"📊 {text} Selected\n\n"
            "Enter target price:",

            reply_markup=ReplyKeyboardMarkup(

                price_keyboard,

                resize_keyboard=True

            )

        )








    # ==================================================
    # MANUAL INPUT BUTTONS
    # ==================================================


    elif text in [

        "✏️ Enter Forex Pair",

        "✍️ Enter Crypto Pair",

        "✍️ Enter Commodity",

        "✏️ Enter Index"

    ]:


        context.user_data["custom_symbol"] = True



        market = context.user_data.get(

            "market"

        )



        if market == "crypto":


            await update.message.reply_text(

                "🪙 Enter Crypto Symbol\n\n"
                "Example:\n"
                "BNBUSDT\nDOGEUSDT\nADAUSDT"

            )



        elif market == "commodity":


            await update.message.reply_text(

                "🥇 Enter Commodity Symbol\n\n"
                "Example:\n"
                "NATGAS\nCOFFEE"

            )



        elif market == "indices":


            await update.message.reply_text(

                "📊 Enter Index Symbol\n\n"
                "Example:\n"
                "GER30\nUK100"

            )



        else:


            await update.message.reply_text(

                "💱 Enter Forex Pair\n\n"
                "Example:\n"
                "AUDUSD\nEURJPY"

            )

# ==================================================
# MY ALERTS
# ==================================================


    elif text == "📋 My Alerts":


        alerts = get_user_alerts(user_id)



        if not alerts:


            await update.message.reply_text(

                "📋 No active alerts."

            )

            return






        msg = (

            "📋 Your Active Alerts:\n\n"

        )



        for alert in alerts:


            msg += (

                f"🆔 ID: {alert[0]}\n"
                f"📊 Symbol: {alert[2]}\n"
                f"🎯 Target: {alert[3]}\n"
                f"📈 Direction: {alert[4]}\n\n"

            )





        await update.message.reply_text(

            msg

        )









# ==================================================
# REMOVE ALERT
# ==================================================


    elif text == "🗑 Remove Alert":


        alerts = get_user_alerts(user_id)



        if not alerts:


            await update.message.reply_text(

                "📋 No active alerts."

            )

            return





        buttons = []



        for alert in alerts:


            buttons.append(

                [

                    InlineKeyboardButton(

                        f"{alert[2]} | {alert[3]}",

                        callback_data=f"toggle_{alert[0]}"

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
            "Tap alerts to select\n"
            "Then press Delete Selected",

            reply_markup=InlineKeyboardMarkup(

                buttons

            )

        )









# ==================================================
# STATUS BUTTON
# ==================================================


    elif text == "ℹ️ Status":

            await system_status(
                update,
                context
            )








# ==================================================
# REMOVE UNUSED BUTTON
# ==================================================



# ==================================================
# INLINE CALLBACK HANDLER
# ==================================================


async def delete_callback(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query


    await query.answer()



    data = query.data





    # ======================================
    # SELECT / UNSELECT ALERT
    # ======================================


    if data.startswith("toggle_"):



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





        alerts = get_user_alerts(

            query.from_user.id

        )



        buttons = []





        for alert in alerts:



            mark = "✅ " if alert[0] in selected else ""



            buttons.append(

                [

                    InlineKeyboardButton(

                        f"{mark}{alert[2]} | {alert[3]}",

                        callback_data=f"toggle_{alert[0]}"

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






        await query.edit_message_reply_markup(

            reply_markup=InlineKeyboardMarkup(

                buttons

            )

        )







    # ======================================
    # DELETE SELECTED
    # ======================================


    elif data == "delete_selected":



        selected = context.user_data.get(

            "delete_list",

            []

        )





        if not selected:



            await query.answer(

                "Select alerts first",

                show_alert=True

            )

            return







        remove_multiple_alerts(

            selected

        )





        context.user_data.clear()






        await query.edit_message_text(

            "✅ Selected alerts removed."

        )

# ==================================================
# SAVE ALERT
# ==================================================


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






        # ==========================
        # GET CURRENT PRICE
        # ==========================


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








        # ==========================
        # DETERMINE DIRECTION
        # ==========================


        if current_price >= target:


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

            "🚀 Monitoring Started",


            reply_markup=ReplyKeyboardMarkup(

                main_menu,

                resize_keyboard=True

            )


        )







        context.user_data.clear()






    except Exception as e:



        await update.message.reply_text(

            f"❌ Error creating alert\n\n{e}"

        )








# ==================================================
# MONITOR START
# ==================================================


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








# ==================================================
# MAIN
# ==================================================


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
    # COMMAND
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
    # PRICE INPUT
    # MUST BE ABOVE MENU
    # ==========================


    app.add_handler(

        MessageHandler(

            filters.Regex(

                r"^\d+(\.\d+)?$"

            ),

            save_alert

        )

    )








    # ==========================
    # NORMAL BUTTONS
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







# ==================================================
# RUN
# ==================================================


if __name__ == "__main__":


    main()

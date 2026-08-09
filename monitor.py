import asyncio
import os

from fxcm import get_price
from database import get_active_alerts, disable_alert


# Telegram bot instance will be connected from bot.py
telegram_bot = None



# ==========================
# SEND TELEGRAM MESSAGE
# ==========================

async def send_alert(user_id, message):

    if telegram_bot:

        await telegram_bot.send_message(
            chat_id=user_id,
            text=message
        )



# ==========================
# CHECK ALERTS
# ==========================

async def check_alerts():


    alerts = get_active_alerts()


    for alert in alerts:


        alert_id = alert[0]

        user_id = alert[1]

        symbol = alert[2]

        target_price = alert[3]



        try:

            price = get_price(symbol)


            current_price = float(
                price["bid"]
            )



            # Price reached

            if current_price >= float(target_price):


                message = (

                    "🚨 PRICE ALERT HIT\n\n"

                    f"Pair: {symbol}\n"

                    f"Target: {target_price}\n"

                    f"Current: {current_price}\n\n"

                    "Your level has been reached."

                )



                await send_alert(
                    user_id,
                    message
                )


                disable_alert(
                    alert_id
                )



        except Exception as e:


            print(
                f"Monitor error {symbol}: {e}"
            )



# ==========================
# BACKGROUND LOOP
# ==========================

async def monitor_loop():


    print(
        "📡 Alert Monitor Started"
    )


    while True:


        await check_alerts()


        # Check every 10 seconds

        await asyncio.sleep(10)

import asyncio


from fxcm import get_price
from crypto import get_crypto_price


from database import (
    get_active_alerts,
    disable_alert
)



telegram_bot = None




def set_bot(bot):

    global telegram_bot

    telegram_bot = bot






async def send_alert(user_id, message):


    if telegram_bot:


        await telegram_bot.send_message(

            chat_id=user_id,

            text=message

        )







# ==========================
# PRICE ROUTER
# ==========================


def get_current_price(symbol):


    symbol = symbol.upper()



    # ======================
    # CRYPTO
    # ======================


    if symbol.endswith("USDT"):


        data = get_crypto_price(symbol)


        return float(

            data["price"]

        )





    # ======================
    # FXCM
    # Forex
    # Commodities
    # Indices
    # ======================


    else:


        data = get_price(symbol)


        return float(

            data["bid"]

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

        target = float(alert[3])

        direction = alert[4]





        try:



            current = get_current_price(symbol)





            print(

                f"{symbol} | Current: {current} | Target: {target} | {direction}",

                flush=True

            )







            # ==========================
            # DIRECTION CHECK
            # ==========================



            hit = False



            if direction == "ABOVE":


                if current >= target:

                    hit = True





            elif direction == "BELOW":


                if current <= target:

                    hit = True







            # ==========================
            # SEND ALERT
            # ==========================


            if hit:



                await send_alert(


                    user_id,


                    f"""
🚨 PRICE ALERT HIT


Symbol:
{symbol}


Direction:
{direction}


Target:
{target}


Current:
{current}

"""

                )



                disable_alert(alert_id)






        except Exception as e:



            print(

                "Monitor error:",

                e,

                flush=True

            )









# ==========================
# MONITOR LOOP
# ==========================


async def monitor_loop():


    print(

        "📡 Monitor running",

        flush=True

    )



    while True:



        await check_alerts()



        await asyncio.sleep(10)

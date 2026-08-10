import asyncio


from fxcm import get_price

from crypto import get_crypto_price


from database import (
    get_active_alerts,
    disable_alert
)



telegram_bot = None





# ==========================
# SET TELEGRAM BOT
# ==========================


def set_bot(bot):

    global telegram_bot

    telegram_bot = bot







# ==========================
# SEND ALERT
# ==========================


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


        return {

            "bid": float(data["bid"]),

            "ask": float(data["ask"])

        }








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





            # ======================
            # PRINT LIVE PRICE
            # ======================


            if isinstance(current, dict):


                print(

                    f"{symbol} | Bid: {current['bid']} | Ask: {current['ask']} | Target: {target} | Direction: {direction}",

                    flush=True

                )


            else:


                print(

                    f"{symbol} | Price: {current} | Target: {target} | Direction: {direction}",

                    flush=True

                )








            # ======================
            # DIRECTION LOGIC
            # ======================


            hit = False





            # ======================
            # FXCM BID / ASK
            # ======================


            if isinstance(current, dict):


                bid = current["bid"]

                ask = current["ask"]




                # Price moving upward

                if direction == "ABOVE":


                    # Ask hits target

                    if ask >= target:

                        hit = True






                # Price moving downward

                elif direction == "BELOW":


                    # Bid hits target

                    if bid <= target:

                        hit = True








            # ======================
            # CRYPTO
            # ======================


            else:



                if direction == "ABOVE":


                    if current >= target:

                        hit = True





                elif direction == "BELOW":


                    if current <= target:

                        hit = True







            # ======================
            # ALERT TRIGGER
            # ======================


            if hit:



                if isinstance(current, dict):

                    display_price = current["ask"]


                else:

                    display_price = current






                await send_alert(

                    user_id,


                    f"""
🚨 PRICE ALERT HIT


📊 Symbol:
{symbol}


📍 Direction:
{direction}


🎯 Target:
{target}


💰 Current Price:
{display_price}


✅ Alert Completed

"""

                )



                disable_alert(alert_id)








        except Exception as e:



            print(

                f"Monitor error for {symbol}: {e}",

                flush=True

            )









# ==========================
# MAIN MONITOR LOOP
# ==========================


async def monitor_loop():


    print(

        "📡 Monitor running",

        flush=True

    )



    while True:



        try:


            await check_alerts()



        except Exception as e:


            print(

                "Monitor loop error:",

                e,

                flush=True

            )





        await asyncio.sleep(10)

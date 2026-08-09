import asyncio


from fxcm import get_price

from crypto import get_crypto_price, validate_crypto


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







def get_current_price(symbol):


    symbol = symbol.upper()



    # Check crypto through Binance

    if validate_crypto(symbol):


        data = get_crypto_price(symbol)


        return float(

            data["price"]

        )



    # Otherwise FXCM Forex

    else:


        data = get_price(symbol)


        return float(

            data["bid"]

        )








async def check_alerts():


    alerts = get_active_alerts()



    for alert in alerts:


        alert_id = alert[0]

        user_id = alert[1]

        symbol = alert[2]

        target = float(alert[3])



        try:


            current = get_current_price(symbol)



            print(

                f"{symbol} | {current} | Target {target}",

                flush=True

            )



            if current >= target:



                await send_alert(

                    user_id,


                    f"""
🚨 PRICE ALERT HIT

Symbol:
{symbol}

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








async def monitor_loop():


    print(

        "📡 Monitor running",

        flush=True

    )



    while True:


        await check_alerts()


        await asyncio.sleep(10)

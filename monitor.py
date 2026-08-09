import asyncio

from fxcm import get_price
from database import (
    get_active_alerts,
    disable_alert
)


telegram_bot=None



async def send_alert(user_id,message):

    if telegram_bot:

        await telegram_bot.send_message(
            chat_id=user_id,
            text=message
        )



async def check_alerts():

    alerts=get_active_alerts()


    for alert in alerts:

        alert_id=alert[0]
        user_id=alert[1]
        symbol=alert[2]
        target=alert[3]


        try:

            price=get_price(symbol)

            current=float(
                price["bid"]
            )


            if current >= float(target):

                await send_alert(
                    user_id,
                    f"""
🚨 PRICE ALERT HIT

Pair: {symbol}

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
                e
            )



async def monitor_loop():

    print(
        "📡 Monitor running"
    )


    while True:

        await check_alerts()

        await asyncio.sleep(10)

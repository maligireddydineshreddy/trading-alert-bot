import os
import requests


PUSHOVER_APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN")


def send_pushover(user_key, title, message):

    if not PUSHOVER_APP_TOKEN:
        print("❌ PUSHOVER_APP_TOKEN missing", flush=True)
        return None


    url = "https://api.pushover.net/1/messages.json"


    data = {

        "token": PUSHOVER_APP_TOKEN,

        "user": user_key,

        "title": title,

        "message": message,


        # Emergency priority
        "priority": 2,


        # Repeat alert every 60 seconds
        "retry": 60,


        # Stop after 1 hour
        "expire": 3600,


        # Your selected sound
        "sound": "alien_alarm"

    }


    try:

        response = requests.post(
            url,
            data=data,
            timeout=15
        )


        print(
            "Pushover Status:",
            response.status_code,
            flush=True
        )


        print(
            "Pushover Response:",
            response.text,
            flush=True
        )


        return response.json()


    except Exception as e:

        print(
            "Pushover Error:",
            e,
            flush=True
        )

        return None

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


        # Emergency notification
        "priority": 2,


        # Repeat every 20 seconds
        "retry": 30,


        # Stop repeating after 10 minutes
        "expire": 600

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

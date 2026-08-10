import os
import requests


PUSHOVER_APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN")


def send_pushover(user_key, title, message):

    if not PUSHOVER_APP_TOKEN:
        print(
            "❌ PUSHOVER_APP_TOKEN missing",
            flush=True
        )
        return None


    url = "https://api.pushover.net/1/messages.json"


    data = {

        # Your Pushover application token
        "token": PUSHOVER_APP_TOKEN,


        # User's Pushover key
        "user": user_key,


        # Notification content
        "title": title,
        "message": message,


        # ==========================
        # EMERGENCY ALERT
        # ==========================

        "priority": 2,


        # Repeat every 60 seconds
        # until acknowledged
        "retry": 60,


        # Stop after 1 hour
        "expire": 3600,


        # ==========================
        # SOUND
        # ==========================

        "sound": "alien"


    }


    try:

        response = requests.post(
            url,
            data=data,
            timeout=10
        )


        result = response.json()


        print(
            "Pushover Response:",
            result,
            flush=True
        )


        return result



    except Exception as e:

        print(
            "Pushover Error:",
            e,
            flush=True
        )

        return None

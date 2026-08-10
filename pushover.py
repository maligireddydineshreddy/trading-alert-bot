import os
import requests


PUSHOVER_APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN")


def send_pushover(user_key, title, message):

    url = "https://api.pushover.net/1/messages.json"

    data = {
        "token": PUSHOVER_APP_TOKEN,
        "user": user_key,
        "title": title,
        "message": message,

        # Emergency alert
        "priority": 2,
        "retry": 60,
        "expire": 3600,
        "sound": "siren"
    }

    response = requests.post(
        url,
        data=data,
        timeout=10
    )

    print(
        "Pushover:",
        response.text,
        flush=True
    )

    return response.json()

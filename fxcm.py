import os
import requests


FXCM_USER = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")


BASE_URL = "https://api-demo.fxcm.com"


def get_session():

    session = requests.Session()

    payload = {
        "login": FXCM_USER,
        "password": FXCM_PASSWORD
    }


    response = session.post(
        f"{BASE_URL}/trading/open_session",
        json=payload,
        timeout=20
    )


    print(response.text)


    response.raise_for_status()


    return session



def get_price(symbol="EUR/USD"):

    session = get_session()


    response = session.get(

        f"{BASE_URL}/trading/get_model",

        params={
            "models": "Offer"
        },

        timeout=20
    )


    response.raise_for_status()


    data = response.json()


    offers = data.get("offers", [])


    for offer in offers:

        if offer.get("currency") == symbol:

            return {
                "bid": offer.get("sell"),
                "ask": offer.get("buy")
            }


    raise Exception(
        f"{symbol} not found"
    )

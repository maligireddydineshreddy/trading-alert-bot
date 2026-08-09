import os
import requests


FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")


BASE_URL = "https://api-demo.fxcm.com"


def fxcm_login():

    session = requests.Session()

    # FXCM authentication
    response = session.post(

        f"{BASE_URL}/trading/open_session",

        data={

            "username": FXCM_USERNAME,

            "password": FXCM_PASSWORD

        },

        timeout=20

    )


    response.raise_for_status()


    data = response.json()


    token = data.get("access_token")


    if not token:

        raise Exception(
            "FXCM token missing"
        )


    return token





def get_price(symbol="EURUSD"):


    token = fxcm_login()


    headers = {

        "Authorization":
            f"Bearer {token}"

    }



    response = requests.get(

        f"{BASE_URL}/trading/get_model",

        headers=headers,

        params={

            "models":
                "Offer"

        },

        timeout=20

    )


    response.raise_for_status()


    data = response.json()


    offers = data.get(
        "offers",
        []
    )


    for offer in offers:


        if offer.get("currency") == symbol:


            return {

                "symbol": symbol,

                "bid":
                    offer.get("sell"),

                "ask":
                    offer.get("buy")

            }


    raise Exception(
        f"{symbol} not found"
    )

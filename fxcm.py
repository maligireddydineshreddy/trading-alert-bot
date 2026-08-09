import os
import requests


FXCM_BASE = "https://api-demo.fxcm.com"


FXCM_TOKEN = os.getenv("FXCM_TOKEN")


def fxcm_headers():

    if not FXCM_TOKEN:
        raise Exception(
            "FXCM_TOKEN missing in environment variables"
        )

    return {
        "Authorization": f"Bearer {FXCM_TOKEN}",
        "Content-Type": "application/json"
    }



def fxcm_test():

    headers = fxcm_headers()

    response = requests.get(

        f"{FXCM_BASE}/trading/get_model",

        headers=headers,

        params={
            "models": "Offer"
        },

        timeout=20
    )


    response.raise_for_status()


    return response.json()



def get_price(symbol="EUR/USD"):


    data = fxcm_test()


    offers = data.get(
        "offers",
        []
    )


    for offer in offers:


        if offer.get("currency") == symbol:


            return {

                "bid": offer.get("sell"),

                "ask": offer.get("buy")

            }



    raise Exception(
        f"{symbol} price not found"
    )

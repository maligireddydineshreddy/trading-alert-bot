import os
import requests


FXCM_BASE = "https://api-demo.fxcm.com"


FXCM_TOKEN = os.getenv("FXCM_TOKEN")


def get_price(symbol="EUR/USD"):

    if not FXCM_TOKEN:
        raise Exception(
            "FXCM_TOKEN missing in Railway variables"
        )


    headers = {
        "Authorization": f"Bearer {FXCM_TOKEN}",
        "Accept": "application/json"
    }


    url = (
        f"{FXCM_BASE}/trading/get_model"
    )


    response = requests.get(

        url,

        headers=headers,

        params={
            "models": "Offer"
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

                "bid": offer.get("sell"),

                "ask": offer.get("buy"),

                "spread": offer.get("spread")

            }


    raise Exception(
        f"{symbol} price not found"
    )

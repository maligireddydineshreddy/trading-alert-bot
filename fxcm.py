import os
import requests


FXCM_ENDPOINT = "https://endpoints-demo.fxcm.com"

FXCM_USERNAME = os.getenv("FXCM_USERNAME")


def get_session():

    url = (
        f"{FXCM_ENDPOINT}/iam/trading-systems/"
        f"{FXCM_USERNAME}"
    )

    r = requests.get(
        url,
        headers={
            "X-COOKIE-DOMAIN": "fxcm.com"
        },
        timeout=20
    )

    r.raise_for_status()

    data = r.json()

    if not data:
        raise Exception("No FXCM trading session found")

    session = data[0]

    return session



def get_price(symbol="EUR/USD"):

    session = get_session()

    trading_session = session["tradingSessionId"]
    sub_session = session["tradingSessionSubId"]

    url = (
        f"{FXCM_ENDPOINT}/"
        f"trading/get_model"
    )


    headers = {
        "X-COOKIE-DOMAIN": "fxcm.com"
    }


    params = {
        "models": "Offer",
        "tradingSessionId": trading_session,
        "tradingSessionSubId": sub_session
    }


    r = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=20
    )


    r.raise_for_status()

    data = r.json()


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

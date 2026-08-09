import os
import requests


FXCM_BASE = "https://endpoints-demo.fxcm.com"
FXCM_API = "https://api-demo.fxcm.com"


USERNAME = os.getenv("FXCM_USERNAME")
PASSWORD = os.getenv("FXCM_PASSWORD")


def login():

    session = requests.Session()


    r = session.get(
        f"{FXCM_BASE}/iam/trading-systems/{USERNAME}",
        headers={
            "X-COOKIE-DOMAIN": "fxcm.com"
        },
        timeout=20
    )

    r.raise_for_status()


    systems = r.json()


    if not systems:
        raise Exception(
            "No FXCM account found"
        )


    tsid = systems[0]["tradingSessionId"]
    tssid = systems[0]["tradingSessionSubId"]


    xsrf = session.cookies.get(
        "XSRF-TOKEN"
    )


    auth = session.post(

        f"{FXCM_BASE}/iam/authenticate",

        json={

            "loginId": USERNAME,

            "password": PASSWORD,

            "tradingSessionId": tsid,

            "tradingSessionSubId": tssid,

            "appName": "TradingAlertBot"

        },

        headers={

            "X-COOKIE-DOMAIN": "fxcm.com",

            "X-XSRF-TOKEN": xsrf

        },

        timeout=20
    )


    auth.raise_for_status()


    token = auth.json()["accessToken"]


    return token



def get_price(symbol="EUR/USD"):


    token = login()


    headers = {

        "Authorization": f"Bearer {token}",

        "Accept": "application/json"

    }


    r = requests.get(

        f"{FXCM_API}/trading/get_model",

        headers=headers,

        params={
            "models":"Offer"
        },

        timeout=20
    )


    r.raise_for_status()


    data = r.json()


    for offer in data.get("offers", []):


        if offer.get("currency") == symbol:


            return {

                "bid": offer.get("sell"),

                "ask": offer.get("buy"),

                "spread": offer.get("spread")

            }


    raise Exception(
        "Symbol not available"
    )

import os
import requests


FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")


FXCM_BASE = "https://api-demo.fxcm.com"


def get_token():

    session = requests.Session()


    # Get trading systems
    r = session.get(
        f"https://endpoints-demo.fxcm.com/iam/trading-systems/{FXCM_USERNAME}",
        headers={
            "X-COOKIE-DOMAIN": "fxcm.com"
        },
        timeout=20
    )

    r.raise_for_status()


    systems = r.json()


    if not systems:
        raise Exception(
            "No FXCM trading system found"
        )


    trading_session_id = systems[0]["tradingSessionId"]
    trading_session_sub_id = systems[0]["tradingSessionSubId"]


    xsrf = session.cookies.get(
        "XSRF-TOKEN"
    )


    auth = session.post(

        "https://endpoints-demo.fxcm.com/iam/authenticate",

        json={

            "loginId": FXCM_USERNAME,

            "password": FXCM_PASSWORD,

            "tradingSessionId": trading_session_id,

            "tradingSessionSubId": trading_session_sub_id,

            "appName": "TradingAlertBot"

        },

        headers={

            "X-COOKIE-DOMAIN":"fxcm.com",

            "X-XSRF-TOKEN":xsrf

        },

        timeout=20

    )


    auth.raise_for_status()


    data = auth.json()


    token = data.get(
        "accessToken"
    )


    if not token:
        raise Exception(
            "FXCM token missing"
        )


    return token




def get_price(symbol):


    token = get_token()


    headers = {

        "Authorization":
        f"Bearer {token}",

        "Accept":
        "application/json"

    }


    url = (
        "https://api-demo.fxcm.com"
        "/trading/get_model"
    )


    response = requests.get(

        url,

        headers=headers,

        params={

            "models":"Offer"

        },

        timeout=20

    )


    response.raise_for_status()


    data=response.json()


    offers=data["offers"]


    for offer in offers:

        if offer["currency"] == symbol:

            return offer["ask"]


    return "Symbol not found"

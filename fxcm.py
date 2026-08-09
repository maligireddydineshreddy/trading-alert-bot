import os
import requests


FXCM_ENDPOINT = "https://endpoints-demo.fxcm.com"

FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")


def create_session():

    session = requests.Session()


    # Get trading system

    r = session.get(
        f"{FXCM_ENDPOINT}/iam/trading-systems/{FXCM_USERNAME}",
        headers={
            "X-COOKIE-DOMAIN": "fxcm.com"
        },
        timeout=20
    )

    r.raise_for_status()


    system = r.json()[0]


    trading_session_id = system["tradingSessionId"]
    trading_session_sub_id = system["tradingSessionSubId"]


    xsrf = session.cookies.get("XSRF-TOKEN")


    if not xsrf:
        raise Exception(
            "XSRF token missing"
        )


    # Authenticate

    login = session.post(

        f"{FXCM_ENDPOINT}/iam/authenticate",

        json={

            "loginId": FXCM_USERNAME,

            "password": FXCM_PASSWORD,

            "tradingSessionId": trading_session_id,

            "tradingSessionSubId": trading_session_sub_id,

            "appName": "TelegramTradingAlertBot"

        },

        headers={

            "X-COOKIE-DOMAIN":"fxcm.com",

            "X-XSRF-TOKEN":xsrf

        },

        timeout=20
    )


    login.raise_for_status()


    return session



def get_price(symbol="EUR/USD"):


    session=create_session()


    # NEW FXCM PRICE ENDPOINT

    r=session.get(

        f"{FXCM_ENDPOINT}/trading/marketdata/{symbol}",

        timeout=20

    )


    r.raise_for_status()


    data=r.json()


    return {

        "bid":data["bid"],

        "ask":data["ask"]

    }

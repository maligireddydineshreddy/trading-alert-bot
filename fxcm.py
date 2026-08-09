import os
import requests


FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")

# Working FXCM endpoint
FXCM_BASE = "https://endpoints-demo.fxcm.com"


session = requests.Session()

ACCESS_TOKEN = None



def fxcm_login():

    global ACCESS_TOKEN


    # Step 1: Get trading system

    response = session.get(

        f"{FXCM_BASE}/iam/trading-systems/{FXCM_USERNAME}",

        headers={
            "X-COOKIE-DOMAIN": "fxcm.com"
        },

        timeout=20
    )


    response.raise_for_status()


    systems = response.json()


    if not systems:
        raise Exception(
            "No FXCM trading system found"
        )


    trading_session_id = systems[0]["tradingSessionId"]

    trading_session_sub_id = systems[0]["tradingSessionSubId"]



    # Step 2: Get XSRF token

    xsrf_token = session.cookies.get(
        "XSRF-TOKEN"
    )


    if not xsrf_token:

        raise Exception(
            "FXCM XSRF token missing"
        )



    # Step 3: Authenticate

    auth_response = session.post(

        f"{FXCM_BASE}/iam/authenticate",

        json={

            "loginId": FXCM_USERNAME,

            "password": FXCM_PASSWORD,

            "tradingSessionId": trading_session_id,

            "tradingSessionSubId": trading_session_sub_id,

            "appName": "TelegramTradingAlertBot"

        },


        headers={

            "X-COOKIE-DOMAIN": "fxcm.com",

            "X-XSRF-TOKEN": xsrf_token

        },


        timeout=20

    )


    auth_response.raise_for_status()


    data = auth_response.json()


    ACCESS_TOKEN = data.get(
        "accessToken"
    )


    if not ACCESS_TOKEN:

        raise Exception(
            "FXCM access token not received"
        )


    return ACCESS_TOKEN





def get_price(symbol="EURUSD"):

    global ACCESS_TOKEN


    if ACCESS_TOKEN is None:

        fxcm_login()



    headers = {

        "Authorization":
            f"Bearer {ACCESS_TOKEN}",

        "Accept":
            "application/json"

    }



    # Get market prices

    response = session.get(

        f"{FXCM_BASE}/trading/get_model",

        params={

            "models":
                "Offer"

        },


        headers=headers,


        timeout=20

    )


    response.raise_for_status()


    data = response.json()



    offers = data.get(
        "Offer",
        []
    )



    for offer in offers:


        if offer.get("currency") == symbol:


            return {

                "symbol": symbol,

                "bid":
                    offer.get("sell"),

                "ask":
                    offer.get("buy"),

                "spread":
                    offer.get("spread"),

                "time":
                    offer.get("time")

            }



    raise Exception(
        f"{symbol} price not found"
    )





def test_connection():

    token = fxcm_login()


    return {

        "connected": True,

        "token":
            token[:10] + "..."

    }

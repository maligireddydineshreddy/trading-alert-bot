import os
import requests


FXCM_BASE = "https://endpoints-demo.fxcm.com"


FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")



# ==========================
# LOGIN
# ==========================

def fxcm_login():

    if not FXCM_USERNAME:
        raise Exception("FXCM_USERNAME missing")

    if not FXCM_PASSWORD:
        raise Exception("FXCM_PASSWORD missing")


    session = requests.Session()


    # Step 1:
    # Get trading system information

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


    trading_session_id = systems[0].get(
        "tradingSessionId"
    )


    trading_session_sub_id = systems[0].get(
        "tradingSessionSubId"
    )



    xsrf = session.cookies.get(
        "XSRF-TOKEN"
    )


    if not xsrf:

        raise Exception(
            "FXCM XSRF token missing"
        )



    # Step 2:
    # Authenticate

    auth = session.post(

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

            "X-XSRF-TOKEN": xsrf

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
            "FXCM access token not received"
        )


    return session, token





# ==========================
# GET MARKET DATA
# ==========================

def get_price(symbol="EUR/USD"):


    session, token = fxcm_login()



    headers = {

        "Authorization":
        f"Bearer {token}",

        "Accept":
        "application/json"

    }



    response = session.get(

        f"{FXCM_BASE}/trading/get_model",

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


        currency = offer.get(
            "currency"
        )


        if currency == symbol:


            return {

                "bid":
                offer.get("sell"),

                "ask":
                offer.get("buy")

            }



    raise Exception(
        f"{symbol} not found"
    )

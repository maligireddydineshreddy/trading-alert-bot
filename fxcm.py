import os
import requests


FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")


FXCM_BASE = "https://endpoints-demo.fxcm.com"


# ==========================
# FXCM LOGIN
# ==========================

def fxcm_login():

    session = requests.Session()


    # Get trading systems

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



    trading_session_id = systems[0][
        "tradingSessionId"
    ]


    trading_session_sub_id = systems[0][
        "tradingSessionSubId"
    ]



    xsrf = session.cookies.get(
        "XSRF-TOKEN"
    )


    if not xsrf:

        raise Exception(
            "FXCM XSRF token missing"
        )



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
            "FXCM access token missing"
        )



    return token





# ==========================
# GET PRICE
# ==========================

def get_price(symbol):


    token = fxcm_login()



    headers = {

        "Authorization":
        f"Bearer {token}",

        "Accept":
        "application/json"

    }



    response = requests.get(

        "https://api-demo.fxcm.com/trading/get_model",

        headers=headers,

        params={

            "models":"Offer"

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

                "bid":
                offer.get("sell"),


                "ask":
                offer.get("buy")

            }



    raise Exception(
        f"{symbol} price not found"
    )

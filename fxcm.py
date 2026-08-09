import os
import requests


FXCM_ENDPOINT = "https://endpoints-demo.fxcm.com"

FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")


# ==================================
# CREATE AUTHENTICATED FXCM SESSION
# ==================================

def create_session():

    session = requests.Session()


    # Get trading system

    system_response = session.get(

        f"{FXCM_ENDPOINT}/iam/trading-systems/{FXCM_USERNAME}",

        headers={
            "X-COOKIE-DOMAIN": "fxcm.com"
        },

        timeout=20
    )


    system_response.raise_for_status()


    system = system_response.json()[0]


    trading_session_id = system["tradingSessionId"]

    trading_session_sub_id = system["tradingSessionSubId"]



    xsrf = session.cookies.get(
        "XSRF-TOKEN"
    )


    if not xsrf:

        raise Exception(
            "FXCM XSRF token missing"
        )



    # Login

    login_response = session.post(

        f"{FXCM_ENDPOINT}/iam/authenticate",

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


    login_response.raise_for_status()



    return session



# ==================================
# GET FXCM PRICE
# ==================================

def get_price(symbol="EUR/USD"):


    session = create_session()



    response = session.get(

        f"{FXCM_ENDPOINT}/trading/get_model",

        params={

            "models": "Offer"

        },


        headers={

            "X-COOKIE-DOMAIN": "fxcm.com"

        },


        timeout=20

    )


    print(
        "FXCM STATUS:",
        response.status_code
    )


    if response.status_code != 200:

        print(
            response.text
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

                "ask": offer.get("buy")

            }



    raise Exception(

        f"{symbol} price not found"

    )



# ==================================
# CONNECTION TEST
# ==================================

def test_connection():

    session = create_session()

    return True

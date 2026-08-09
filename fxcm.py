import os
import requests


FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")


BASE_URL = "https://endpoints-demo.fxcm.com"


session = requests.Session()
TOKEN = None



def login():

    global TOKEN


    # Get trading systems

    r = session.get(
        f"{BASE_URL}/iam/trading-systems/{FXCM_USERNAME}",
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


    if not xsrf:
        raise Exception(
            "XSRF token missing"
        )



    auth = session.post(

        f"{BASE_URL}/iam/authenticate",

        json={

            "loginId": FXCM_USERNAME,

            "password": FXCM_PASSWORD,

            "tradingSessionId":
                trading_session_id,

            "tradingSessionSubId":
                trading_session_sub_id,

            "appName":
                "TelegramTradingAlertBot"
        },


        headers={

            "X-COOKIE-DOMAIN":
                "fxcm.com",

            "X-XSRF-TOKEN":
                xsrf
        },


        timeout=20
    )


    auth.raise_for_status()


    data = auth.json()


    TOKEN = data["accessToken"]


    return TOKEN





def get_price(symbol):


    global TOKEN


    if TOKEN is None:
        login()



    r = session.get(

        f"{BASE_URL}/trading/get_model",

        params={

            "models":
                "Offer"

        },


        headers={

            "Authorization":
                f"Bearer {TOKEN}"

        },


        timeout=20
    )


    r.raise_for_status()


    data = r.json()


    offers = data["Offer"]



    for offer in offers:

        if offer["currency"] == symbol:


            return {

                "bid":
                    offer["bid"],

                "ask":
                    offer["ask"]

            }



    raise Exception(
        f"{symbol} not found"
    )

import os
import requests


FXCM_ENDPOINT = "https://endpoints-demo.fxcm.com"

FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")


def fxcm_login():

    session = requests.Session()


    # Create session
    r = session.post(

        f"{FXCM_ENDPOINT}/trading/open_session",

        timeout=20

    )


    r.raise_for_status()


    session_data = r.json()


    return session, session_data



def authenticate():

    session, data = fxcm_login()


    response = session.post(

        f"{FXCM_ENDPOINT}/trading/login",

        json={

            "username": FXCM_USERNAME,

            "password": FXCM_PASSWORD

        },

        timeout=20

    )


    response.raise_for_status()


    return session



def get_price(symbol="EUR/USD"):


    session = authenticate()


    response = session.get(

        f"{FXCM_ENDPOINT}/trading/get_model",

        params={

            "models":"Offer"

        },

        timeout=20

    )


    response.raise_for_status()


    data=response.json()


    offers=data.get("offers",[])


    for offer in offers:

        if offer.get("currency") == symbol:


            return {

                "bid":offer.get("sell"),

                "ask":offer.get("buy")

            }


    raise Exception(
        f"{symbol} not found"
    )

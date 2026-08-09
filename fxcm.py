import os
import requests


FXCM_ENDPOINT = "https://endpoints-demo.fxcm.com"

FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")


def create_session():

    s = requests.Session()

    # get trading system
    r = s.get(
        f"{FXCM_ENDPOINT}/iam/trading-systems/{FXCM_USERNAME}",
        headers={
            "X-COOKIE-DOMAIN": "fxcm.com"
        }
    )

    r.raise_for_status()

    system = r.json()[0]


    xsrf = s.cookies.get("XSRF-TOKEN")


    # login
    r = s.post(
        f"{FXCM_ENDPOINT}/iam/authenticate",
        json={
            "loginId": FXCM_USERNAME,
            "password": FXCM_PASSWORD,
            "tradingSessionId": system["tradingSessionId"],
            "tradingSessionSubId": system["tradingSessionSubId"],
            "appName": "TelegramTradingAlertBot"
        },
        headers={
            "X-COOKIE-DOMAIN":"fxcm.com",
            "X-XSRF-TOKEN":xsrf
        }
    )

    r.raise_for_status()

    data=r.json()

    s.headers.update({
        "Authorization": "Bearer " + data["accessToken"],
        "X-COOKIE-DOMAIN":"fxcm.com"
    })


    return s



def get_price(symbol="EUR/USD"):

    s=create_session()


    url=f"{FXCM_ENDPOINT}/trading/get_model"


    params={
        "models":"Offer",
        "symbols":symbol
    }


    r=s.get(
        url,
        params=params
    )


    print("STATUS:",r.status_code)
    print(r.text[:500])


    r.raise_for_status()


    data=r.json()


    return data

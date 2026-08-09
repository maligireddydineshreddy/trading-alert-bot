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
        },
        timeout=20
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
            "X-COOKIE-DOMAIN": "fxcm.com",
            "X-XSRF-TOKEN": xsrf
        },
        timeout=20
    )

    r.raise_for_status()

    token = r.json()["accessToken"]

    s.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    })

    return s



def get_price(symbol="EUR/USD"):

    s = create_session()

    url = (
        f"{FXCM_ENDPOINT}"
        f"/trading/marketdata/{symbol}"
    )

    r = s.get(url, timeout=20)

    print("STATUS:", r.status_code)
    print(r.text[:300])

    r.raise_for_status()

    data = r.json()

    return data

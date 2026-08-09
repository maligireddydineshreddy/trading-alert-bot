import os

os.environ["LD_LIBRARY_PATH"] = "/app/forexconnect/lib"

from forexconnect import ForexConnect, fxcorepy


def get_price(symbol):

    fx = ForexConnect()

    login = os.getenv("FXCM_USERNAME")
    password = os.getenv("FXCM_PASSWORD")
    url = os.getenv("FXCM_URL")


    fx.login(
        login,
        password,
        url,
        "Demo",
        session_status_callback=None
    )


    offers = fx.get_table(
        fxcorepy.O2GTableType.Offers
    )


    for row in offers:

        if row.instrument == symbol:

            return {
                "bid": row.bid,
                "ask": row.ask
            }


    raise Exception(
        "Symbol not found"
    )

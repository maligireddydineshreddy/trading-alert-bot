import os

os.environ["LD_LIBRARY_PATH"] = "/app/forexconnect/lib"

from forexconnect import ForexConnect, fxcorepy


FXCM_URL = os.getenv(
    "FXCM_URL",
    "https://www.fxcorporate.com/Hosts.jsp"
)


def get_price(symbol):

    login = os.getenv("FXCM_USERNAME")
    password = os.getenv("FXCM_PASSWORD")

    if not login or not password:
        raise Exception(
            "FXCM credentials missing"
        )

    fx = ForexConnect()

    try:

        fx.login(
            login,
            password,
            FXCM_URL,
            "Demo"
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
            f"Symbol {symbol} not found"
        )


    finally:

        fx.logout()

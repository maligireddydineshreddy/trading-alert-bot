import os
import time

from forexconnect import ForexConnect, fxcorepy


FXCM_USERNAME = os.getenv("FXCM_USERNAME")
FXCM_PASSWORD = os.getenv("FXCM_PASSWORD")


def get_price(symbol="EUR/USD"):

    fx = ForexConnect()

    try:

        fx.login(
            FXCM_USERNAME,
            FXCM_PASSWORD,
            "https://www.fxcorporate.com/Hosts.jsp",
            "Demo"
        )

        offers = fx.get_table(
            fxcorepy.O2GTableType.OFFERS
        )


        for row in offers:

            if row.instrument == symbol:

                price = {
                    "bid": row.bid,
                    "ask": row.ask
                }

                fx.logout()

                return price


        fx.logout()

        raise Exception(
            f"{symbol} not found"
        )


    except Exception as e:

        try:
            fx.logout()
        except:
            pass

        raise e

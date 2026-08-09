import os
from forexconnect import ForexConnect, fxcorepy


def get_price(symbol):

    fx = ForexConnect()

    username = os.getenv("FXCM_USERNAME")
    password = os.getenv("FXCM_PASSWORD")
    url = os.getenv("FXCM_URL")

    try:

        fx.login(
            username,
            password,
            url,
            "Demo"
        )

        offers = fx.get_table(
            fxcorepy.O2GTableType.OFFERS
        )


        # FXCM format conversion
        if symbol == "EURUSD":
            symbol = "EUR/USD"

        if symbol == "GBPUSD":
            symbol = "GBP/USD"

        if symbol == "USDJPY":
            symbol = "USD/JPY"

        if symbol == "GBPJPY":
            symbol = "GBP/JPY"


        for row in offers:

            if row.instrument == symbol:

                return {
                    "symbol": row.instrument,
                    "bid": row.bid,
                    "ask": row.ask
                }


        return {
            "error": f"{symbol} not found"
        }


    except Exception as e:

        return {
            "error": str(e)
        }


    finally:

        try:
            fx.logout()
        except:
            pass

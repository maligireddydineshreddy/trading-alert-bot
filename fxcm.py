import os

os.environ["LD_LIBRARY_PATH"] = "/app/forexconnect/lib"

from forexconnect import ForexConnect, fxcorepy


SYMBOL_MAP = {
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY",
    "GBPJPY": "GBP/JPY",

    "BTCUSDT": "BTC/USD",
    "ETHUSDT": "ETH/USD",

    "XAUUSD": "XAU/USD",
}


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


        fx_table = fx.get_table(
            fxcorepy.O2GTableType.OFFERS
        )


        target = SYMBOL_MAP.get(symbol, symbol)


        for row in fx_table:

            if row.instrument == target:

                return {
                    "symbol": row.instrument,
                    "bid": row.bid,
                    "ask": row.ask
                }


        raise Exception(
            f"{target} not found"
        )


    finally:

        try:
            fx.logout()
        except:
            pass

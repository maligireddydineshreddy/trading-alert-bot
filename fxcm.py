import os

os.environ["LD_LIBRARY_PATH"] = "/app/forexconnect/lib"

from forexconnect import ForexConnect, fxcorepy


FXCM_URL = os.getenv(
    "FXCM_URL",
    "https://www.fxcorporate.com/Hosts.jsp"
)


SYMBOL_MAP = {
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY",
    "GBPJPY": "GBP/JPY",

    "BTCUSDT": "BTC/USD",
    "ETHUSDT": "ETH/USD"
}


def get_price(symbol):

    login = os.getenv("FXCM_USERNAME")
    password = os.getenv("FXCM_PASSWORD")

    if symbol in SYMBOL_MAP:
        symbol = SYMBOL_MAP[symbol]


    fx = ForexConnect()

    try:

        fx.login(
            login,
            password,
            FXCM_URL,
            "Demo"
        )


        offers = fx.get_table(
            fxcorepy.O2GTableType.OFFERS
        )


        for row in offers:

            if row.instrument == symbol:

                return {
                    "symbol": symbol,
                    "bid": row.bid,
                    "ask": row.ask
                }


        raise Exception(
            f"{symbol} not found"
        )


    finally:

        fx.logout()

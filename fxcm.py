import os

from forexconnect import ForexConnect, fxcorepy


def get_price(symbol):

    symbol_map = {
        "EURUSD": "EUR/USD",
        "GBPUSD": "GBP/USD",
        "USDJPY": "USD/JPY",
        "GBPJPY": "GBP/JPY",
        "XAUUSD": "XAU/USD"
    }

    target = symbol_map.get(symbol, symbol)

    fx = ForexConnect()

    fx.login(
        os.getenv("FXCM_USERNAME"),
        os.getenv("FXCM_PASSWORD"),
        os.getenv("FXCM_URL"),
        "Demo"
    )


    offers = fx.get_table(
        fxcorepy.O2GTableType.OFFERS
    )


    for row in offers:

        if row.instrument == target:

            data = {
                "symbol": row.instrument,
                "bid": row.bid,
                "ask": row.ask
            }

            fx.logout()

            return data


    fx.logout()

    raise Exception(
        f"{symbol} not found"
    )

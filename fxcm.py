import os

from forexconnect import ForexConnect, fxcorepy


def get_price(symbol):

    symbol_map = {
        "EURUSD": "EUR/USD",
        "GBPUSD": "GBP/USD",
        "USDJPY": "USD/JPY",
        "GBPJPY": "GBP/JPY",
        "BTCUSDT": "BTC/USD",
        "ETHUSDT": "ETH/USD",
    }

    instrument = symbol_map.get(symbol, symbol)

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

        if row.instrument == instrument:

            price = {
                "symbol": row.instrument,
                "bid": row.bid,
                "ask": row.ask
            }

            fx.logout()

            return price


    fx.logout()

    raise Exception(
        f"{instrument} not found"
    )

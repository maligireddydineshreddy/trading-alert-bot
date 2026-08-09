from binance.client import Client


client = Client()



def get_crypto_price(symbol):


    supported = [

        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT"

    ]


    if symbol not in supported:

        raise Exception(
            "Crypto symbol not supported"
        )



    ticker = client.get_symbol_ticker(

        symbol=symbol

    )



    return {

        "symbol": symbol,

        "price": float(
            ticker["price"]
        )

    }

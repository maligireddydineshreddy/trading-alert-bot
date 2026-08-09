from binance.client import Client


client = Client()


def get_crypto_price(symbol):

    symbol_map = {
        "BTCUSDT": "BTCUSDT",
        "ETHUSDT": "ETHUSDT"
    }


    if symbol not in symbol_map:
        raise Exception("Crypto symbol not supported")


    ticker = client.get_symbol_ticker(
        symbol=symbol_map[symbol]
    )


    return {
        "symbol": symbol,
        "price": float(ticker["price"])
    }

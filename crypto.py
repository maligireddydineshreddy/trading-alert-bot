from binance.client import Client


client = Client()



# ==========================
# HOT BUTTON CRYPTO
# ==========================

COMMON_CRYPTO = [

    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",

    # Backend only
    "BNBUSDT"

]





# ==========================
# GET CRYPTO PRICE
# ==========================


def get_crypto_price(symbol):


    symbol = symbol.upper()



    try:


        ticker = client.get_symbol_ticker(

            symbol=symbol

        )


        return {


            "symbol": symbol,


            "price": float(

                ticker["price"]

            )

        }



    except Exception:


        raise Exception(

            "Crypto symbol not supported"

        )






# ==========================
# VALIDATE CRYPTO
# ==========================


def validate_crypto(symbol):


    symbol = symbol.upper()



    # Fast check for common coins

    if symbol in COMMON_CRYPTO:

        return True



    # Binance API check for any coin

    try:


        client.get_symbol_ticker(

            symbol=symbol

        )


        return True



    except Exception:


        return False

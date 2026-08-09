from binance.client import Client


client = Client()



# ==========================
# SUPPORTED CRYPTO
# ==========================

COMMON_CRYPTO = [

    # Hot buttons
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



    if symbol not in COMMON_CRYPTO:


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






# ==========================
# VALIDATE CRYPTO
# ==========================


def validate_crypto(symbol):


    symbol = symbol.upper()



    # Fast local check

    if symbol in COMMON_CRYPTO:

        return True



    # Binance fallback

    try:


        client.get_symbol_ticker(

            symbol=symbol

        )


        return True



    except:


        return False

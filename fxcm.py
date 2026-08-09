import os

os.environ["LD_LIBRARY_PATH"] = "/app/forexconnect/lib"


from forexconnect import (
    ForexConnect,
    fxcorepy
)



# ==========================
# COMMON FOREX PAIRS
# ==========================


COMMON_FOREX = [

    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "USDCHF",
    "USDCAD",
    "AUDUSD",
    "NZDUSD",

    "EURGBP",
    "EURJPY",
    "EURCHF",
    "EURAUD",

    "GBPJPY",
    "GBPCHF",
    "GBPAUD",

    "AUDJPY",
    "CADJPY",
    "CHFJPY",
    "NZDJPY",

    "AUDCAD",
    "AUDNZD",
    "EURNZD",
    "GBPCAD"

]





# ==========================
# COMMON COMMODITIES
# ==========================


COMMON_COMMODITIES = [

    "XAUUSD",
    "XAGUSD",
    "USOIL",
    "COPPER"

]







# ==========================
# FXCM LOGIN
# ==========================


def login_fxcm():


    fx = ForexConnect()


    fx.login(

        os.getenv("FXCM_USERNAME"),

        os.getenv("FXCM_PASSWORD"),

        os.getenv("FXCM_URL"),

        "Demo"

    )


    return fx







# ==========================
# GET PRICE
# ==========================


def get_price(symbol):


    symbol = symbol.upper().replace("/", "")


    fx = login_fxcm()



    offers = fx.get_table(

        fxcorepy.O2GTableType.OFFERS

    )



    for row in offers:


        fx_symbol = row.instrument.replace("/", "")



        if fx_symbol == symbol:


            result = {


                "symbol": row.instrument,

                "bid": row.bid,

                "ask": row.ask

            }



            fx.logout()


            return result





    fx.logout()



    raise Exception(

        f"{symbol} not found"

    )








# ==========================
# VALIDATE SYMBOL
# ==========================


def validate_symbol(symbol):


    symbol = symbol.upper().replace("/", "")



    # FAST LOCAL CHECK

    if symbol in COMMON_FOREX:

        return True



    if symbol in COMMON_COMMODITIES:

        return True





    # FXCM FALLBACK CHECK

    try:


        fx = login_fxcm()



        offers = fx.get_table(

            fxcorepy.O2GTableType.OFFERS

        )



        for row in offers:


            fx_symbol = row.instrument.replace("/", "")



            if fx_symbol == symbol:


                fx.logout()

                return True



        fx.logout()



    except Exception as e:


        print(

            "FXCM validation error:",

            e,

            flush=True

        )



    return False

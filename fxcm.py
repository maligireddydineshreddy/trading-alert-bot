import os
import time

os.environ["LD_LIBRARY_PATH"] = "/app/forexconnect/lib"


from forexconnect import (
    ForexConnect,
    fxcorepy
)



# ==========================
# COMMON SYMBOLS
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



COMMON_COMMODITIES = [

    "XAUUSD",
    "XAGUSD",
    "USOIL",
    "COPPER"

]





# ==========================
# GLOBAL FXCM CONNECTION
# ==========================


fx_connection = None






# ==========================
# INITIALIZE FXCM
# ==========================


def init_fxcm():


    global fx_connection



    if fx_connection:


        print(

            "FXCM already connected",

            flush=True

        )

        return





    print(

        "Connecting FXCM...",

        flush=True

    )



    fx = ForexConnect()



    fx.login(

        os.getenv("FXCM_USERNAME"),

        os.getenv("FXCM_PASSWORD"),

        os.getenv("FXCM_URL"),

        "Demo"

    )



    fx_connection = fx



    print(

        "✅ FXCM Connected",

        flush=True

    )








# ==========================
# CHECK CONNECTION
# ==========================


def get_connection():


    global fx_connection



    if fx_connection is None:


        init_fxcm()



    return fx_connection








# ==========================
# GET PRICE
# ==========================


def get_price(symbol):


    symbol = (

        symbol

        .upper()

        .replace("/", "")

    )



    global fx_connection



    try:



        fx = get_connection()



        offers = fx.get_table(

            fxcorepy.O2GTableType.OFFERS

        )





        for row in offers:



            fx_symbol = (

                row.instrument

                .replace("/", "")

                .upper()

            )





            if fx_symbol == symbol:



                return {


                    "symbol": row.instrument,


                    "bid": row.bid,


                    "ask": row.ask


                }





        raise Exception(

            f"{symbol} not found"

        )





    except Exception as e:



        print(

            "FXCM price error:",

            e,

            flush=True

        )



        # reconnect once


        fx_connection = None


        init_fxcm()



        return get_price(symbol)









# ==========================
# VALIDATE SYMBOL
# ==========================


def validate_symbol(symbol):


    symbol = (

        symbol

        .upper()

        .replace("/", "")

    )





    if symbol in COMMON_FOREX:


        return True





    if symbol in COMMON_COMMODITIES:


        return True






    try:



        fx = get_connection()



        offers = fx.get_table(

            fxcorepy.O2GTableType.OFFERS

        )





        for row in offers:



            fx_symbol = (

                row.instrument

                .replace("/", "")

                .upper()

            )





            if fx_symbol == symbol:


                return True





    except Exception as e:



        print(

            "FXCM validation error:",

            e,

            flush=True

        )





    return False








# ==========================
# CLOSE CONNECTION
# ==========================


def close_fxcm():


    global fx_connection



    if fx_connection:


        try:


            fx_connection.logout()



        except:


            pass



        fx_connection = None



        print(

            "FXCM disconnected",

            flush=True

        )

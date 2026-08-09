import os
import time

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


    try:


        fx.login(

            os.getenv("FXCM_USERNAME"),

            os.getenv("FXCM_PASSWORD"),

            os.getenv("FXCM_URL"),

            "Demo"

        )


        return fx



    except Exception as e:


        print(

            "FXCM LOGIN ERROR:",

            repr(e),

            flush=True

        )


        raise







# ==========================
# GET PRICE
# ==========================


def get_price(symbol):


    symbol = symbol.upper().replace("/", "")



    last_error = None





    # RETRY 3 TIMES

    for attempt in range(3):


        fx = None



        try:


            print(

                f"FXCM price request {symbol} attempt {attempt+1}",

                flush=True

            )



            fx = login_fxcm()



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



                    result = {


                        "symbol": row.instrument,


                        "bid": row.bid,


                        "ask": row.ask


                    }





                    print(

                        "FXCM PRICE:",

                        result,

                        flush=True

                    )



                    return result






            raise Exception(

                f"{symbol} not found in FXCM offers"

            )







        except Exception as e:



            last_error = e



            print(

                f"FXCM attempt {attempt+1} failed:",

                repr(e),

                flush=True

            )



            time.sleep(2)







        finally:



            if fx:


                try:


                    fx.logout()



                except:


                    pass








    raise Exception(

        f"FXCM timeout fetching {symbol}: {last_error}"

    )









# ==========================
# VALIDATE SYMBOL
# ==========================


def validate_symbol(symbol):


    symbol = (

        symbol

        .upper()

        .replace("/", "")

    )





    # LOCAL CHECK FIRST


    if symbol in COMMON_FOREX:


        return True





    if symbol in COMMON_COMMODITIES:


        return True






    # FXCM CHECK


    fx = None



    try:



        fx = login_fxcm()



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

            repr(e),

            flush=True

        )





    finally:



        if fx:


            try:


                fx.logout()


            except:


                pass





    return False

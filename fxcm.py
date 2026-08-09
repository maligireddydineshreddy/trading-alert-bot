import os

os.environ["LD_LIBRARY_PATH"] = "/app/forexconnect/lib"


from forexconnect import (
    ForexConnect,
    fxcorepy
)



def login_fxcm():

    fx = ForexConnect()


    fx.login(

        os.getenv("FXCM_USERNAME"),

        os.getenv("FXCM_PASSWORD"),

        os.getenv("FXCM_URL"),

        "Demo"

    )


    return fx





def get_price(symbol):


    symbol = symbol.upper().replace("/", "")


    fx = login_fxcm()



    offers = fx.get_table(

        fxcorepy.O2GTableType.OFFERS

    )



    for row in offers:


        fx_symbol = row.instrument.replace("/", "")



        if fx_symbol == symbol:


            price = {


                "symbol": row.instrument,

                "bid": row.bid,

                "ask": row.ask

            }


            fx.logout()


            return price



    fx.logout()


    raise Exception(

        f"{symbol} not found"

    )







def validate_symbol(symbol):


    symbol = symbol.upper().replace("/", "")


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


    return False

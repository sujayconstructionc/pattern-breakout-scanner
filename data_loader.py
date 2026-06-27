import pandas as pd
import streamlit as st


# ==================================
# NSE SYMBOLS
# ==================================

@st.cache_data(ttl=86400)
def get_nse_symbols():

    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

    try:

        df = pd.read_csv(url)

        symbols = (
            df["SYMBOL"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        return [f"{s}.NS" for s in symbols]

    except Exception as e:

        print("NSE ERROR:", e)

        return []


# ==================================
# BSE SYMBOLS
# ==================================

@st.cache_data(ttl=86400)
def get_bse_symbols():

    return [

        "500325.BO",  # RELIANCE
        "532540.BO",  # TCS
        "500209.BO",  # INFY
        "500112.BO",  # SBIN
        "532174.BO",  # ICICIBANK
        "500180.BO",  # HDFCBANK
        "532215.BO",  # AXISBANK
        "500696.BO",  # HINDUNILVR
        "500034.BO",  # BAJAJFINSV
        "532978.BO",  # BAJAJFINANCE
        "500820.BO",  # ASIANPAINT
        "500875.BO",  # ITC
        "532500.BO",  # MARUTI
        "500010.BO",  # HDFC
        "500247.BO",  # KOTAKBANK
        "500470.BO",  # TATASTEEL
        "532281.BO",  # HCLTECH
        "532977.BO",  # COALINDIA
        "500312.BO",  # ONGC
        "500790.BO",  # NESTLEIND
        "500510.BO",  # LT
        "500570.BO",  # TATAMOTORS
        "532755.BO",  # TECHM
        "500087.BO",  # CIPLA
        "500300.BO",  # GRASIM
        "532898.BO",  # POWERGRID
        "500875.BO",  # ITC
        "500820.BO",  # ASIANPAINT
        "500877.BO",  # APOLLOHOSP
        "532454.BO",  # BHARTIARTL

    ]


# ==================================
# MAIN FUNCTION
# ==================================

def get_symbols(exchange):

    if exchange == "NSE":

        return get_nse_symbols()

    elif exchange == "BSE":

        return get_bse_symbols()

    elif exchange == "NSE+BSE":

        return (
            get_nse_symbols()
            +
            get_bse_symbols()
        )

    return []

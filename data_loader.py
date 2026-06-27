import pandas as pd
import streamlit as st


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

        print(e)
        return []


@st.cache_data(ttl=86400)
def get_bse_symbols():

    try:

        # Yahoo-compatible major BSE stocks
        df = pd.read_csv(
            "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
        )

        symbols = []

        for s in df["Symbol"].tolist():

            symbols.append(f"{s}.BO")

        return list(set(symbols))

    except Exception as e:

        print(e)
        return []


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

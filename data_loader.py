import pandas as pd
import streamlit as st
from bse_mapper import get_bse_yahoo_symbols


@st.cache_data(ttl=86400)
def get_nse_symbols():

    try:

        url = (
            "https://archives.nseindia.com/"
            "content/equities/EQUITY_L.csv"
        )

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

        st.error(f"NSE Error: {e}")

        return []


def get_bse_symbols():

    return get_bse_yahoo_symbols()


def get_symbols(exchange):

    if exchange == "NSE":

        return get_nse_symbols()

    elif exchange == "BSE":

        return get_bse_symbols()

    elif exchange == "NSE+BSE":

        nse = get_nse_symbols()

        bse = get_bse_symbols()

        return list(dict.fromkeys(nse + bse))

    return []

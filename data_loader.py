import pandas as pd
import streamlit as st
import requests
from io import StringIO

from bse_mapper import get_bse_yahoo_symbols


@st.cache_data(ttl=86400)
def get_nse_symbols():

    try:

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/137.0 Safari/537.36"
            )
        }

        url = (
            "https://archives.nseindia.com/"
            "content/equities/EQUITY_L.csv"
        )

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        df = pd.read_csv(
            StringIO(response.text)
        )

        symbols = (
            df["SYMBOL"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        return [
            f"{s}.NS"
            for s in symbols
        ]

    except Exception as e:

        st.error(
            f"NSE Error: {e}"
        )

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

        merged = list(
            dict.fromkeys(
                nse + bse
            )
        )

        st.write(
            f"NSE Symbols: {len(nse)}"
        )

        st.write(
            f"BSE Symbols: {len(bse)}"
        )

        st.write(
            f"Total Symbols: {len(merged)}"
        )

        return merged

    return []

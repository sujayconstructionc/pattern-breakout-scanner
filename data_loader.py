import pandas as pd
import streamlit as st


@st.cache_data(ttl=86400)
def get_symbols(exchange):

    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

    df = pd.read_csv(url)

    symbols = (
        df["SYMBOL"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    return [f"{s}.NS" for s in symbols]

import pandas as pd
import streamlit as st

@st.cache_data(ttl=86400)
def get_symbols(exchange):

```
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

    symbols = [
        f"{s}.NS"
        for s in symbols
    ]

    return symbols

except Exception as e:

    st.error(
        f"Symbol Load Error: {e}"
    )

    return []
```

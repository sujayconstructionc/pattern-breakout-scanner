import streamlit as st
import pandas as pd

from data_loader import get_symbols
from scanner import (
    scan_symbol,
    scan_pattern_only
)

st.set_page_config(
    page_title="Pattern Breakout Scanner",
    layout="wide"
)

st.title("📈 Pattern Breakout Scanner")

exchange = st.sidebar.selectbox(
    "Exchange",
    ["NSE"]
)

scan_mode = st.sidebar.radio(
    "Scan Mode",
    [
        "Pattern Only",
        "Pattern + Breakout"
    ]
)

breakout_mode = st.sidebar.radio(
    "Breakout Type",
    ["Close", "High"]
)

max_stocks = st.sidebar.number_input(
    "Max Stocks To Scan",
    min_value=1,
    max_value=3000,
    value=500
)

scan = st.sidebar.button(
    "SCAN NOW"
)

if scan:

    symbols = get_symbols("NSE")

    symbols = symbols[:max_stocks]

    results = []

    progress = st.progress(0)

    total = len(symbols)

    for i, symbol in enumerate(symbols):

        try:

            if scan_mode == "Pattern Only":

                rows = scan_pattern_only(
                    symbol
                )

            else:

                rows = scan_symbol(
                    symbol=symbol,
                    breakout_mode=breakout_mode
                )

            results.extend(rows)

        except Exception:
            pass

        progress.progress(
            (i + 1) / total
        )

    st.success(
        f"Total Results Found = {len(results)}"
    )

    if len(results):

        df = pd.DataFrame(results)

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            "Download CSV",
            csv,
            file_name="scanner_results.csv",
            mime="text/csv"
        )

    else:

        st.error(
            "No pattern found"
        )

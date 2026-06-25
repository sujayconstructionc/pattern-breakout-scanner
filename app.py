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

st.title("📈 Pattern Breakout Scanner (DEBUG MODE)")

# =====================
# SIDEBAR
# =====================

exchange = st.sidebar.selectbox(
    "Exchange",
    ["NSE", "BSE", "NSE+BSE"]
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

scan = st.sidebar.button("SCAN NOW")

# =====================
# SCAN
# =====================

if scan:

    st.info("Loading symbols...")

    try:

        symbols = get_symbols(exchange)
        symbols = ["RELIANCE.NS"]
        st.success(
            f"Symbols Loaded = {len(symbols)}"
        )

        st.write(
            "First 10 Symbols:",
            symbols[:10]
        )

    except Exception as e:

        st.error(
            f"Symbol Load Error: {e}"
        )

        st.stop()

    symbols = symbols[:max_stocks]

    st.write(
        f"Scanning First {len(symbols)} Stocks"
    )

    results = []

    progress = st.progress(0)

    debug_errors = []

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

        except Exception as e:

            debug_errors.append(
                f"{symbol} -> {e}"
            )

        progress.progress(
            (i + 1) / total
        )

    st.success(
        "Scan Completed"
    )

    st.write(
        f"Total Results Found = {len(results)}"
    )

    if len(debug_errors):

        st.warning(
            f"Errors Found = {len(debug_errors)}"
        )

        st.write(
            debug_errors[:20]
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

import streamlit as st
import pandas as pd

from data_loader import get_symbols
from scanner import (
    scan_symbol,
    scan_pattern_only
)

st.set_page_config(
    page_title="Pattern Breakout Scanner V4",
    layout="wide"
)

st.title("📈 Pattern Breakout Scanner V4")

# =====================================
# SIDEBAR
# =====================================

st.sidebar.header("Scanner Filters")

exchange = st.sidebar.selectbox(
    "Exchange",
    [
        "NSE",
        "BSE",
        "NSE+BSE"
    ]
)

timeframe = st.sidebar.selectbox(
    "Timeframe",
    [
        "Monthly",
        "Quarterly",
        "6 Month",
        "1 Year"
    ]
)

scan_mode = st.sidebar.radio(
    "Scan Mode",
    [
        "Pattern Only",
        "Historical Breakout",
        "Latest Breakout"
    ]
)

breakout_mode = st.sidebar.radio(
    "Breakout Type",
    [
        "Close",
        "High"
    ]
)

max_stocks = st.sidebar.number_input(
    "Max Stocks To Scan",
    min_value=1,
    max_value=5000,
    value=500
)

scan = st.sidebar.button(
    "SCAN NOW"
)

# =====================================
# SCAN
# =====================================

if scan:

    st.info("Loading NSE symbols...")

    symbols = get_symbols(exchange)

    if len(symbols) == 0:

        st.error("No symbols loaded.")
        st.stop()

    symbols = symbols[:max_stocks]

    st.success(
        f"Symbols Loaded = {len(symbols)}"
    )

    progress = st.progress(0)

    results = []
    errors = []

    total = len(symbols)

    for i, symbol in enumerate(symbols):

        try:

            if scan_mode == "Pattern Only":

                rows = scan_pattern_only(
                    symbol=symbol,
                    timeframe=timeframe
                )

            elif scan_mode == "Historical Breakout":

                rows = scan_symbol(
                    symbol=symbol,
                    timeframe=timeframe,
                    breakout_mode=breakout_mode,
                    latest_only=False
                )

            else:

                rows = scan_symbol(
                    symbol=symbol,
                    timeframe=timeframe,
                    breakout_mode=breakout_mode,
                    latest_only=True
                )

            if rows:
                results.extend(rows)

        except Exception as e:

            errors.append(
                f"{symbol} -> {e}"
            )

        progress.progress(
            (i + 1) / total
        )

    st.success(
        f"Scan Completed | Results Found = {len(results)}"
    )

    if len(errors):

        with st.expander("Show Errors"):

            st.write(errors[:50])

    if len(results):

        df = pd.DataFrame(results)

        if "PatternDate" in df.columns:

            df = df.sort_values(
                by="PatternDate",
                ascending=False
            )

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            "⬇ Download CSV",
            csv,
            file_name="scanner_results.csv",
            mime="text/csv"
        )

    else:

        st.warning(
            "No Results Found"
        )

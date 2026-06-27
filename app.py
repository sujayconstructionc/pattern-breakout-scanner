import streamlit as st
import pandas as pd

from data_loader import get_symbols

from scanner import (
    scan_symbol,
    scan_pattern_only
)

st.set_page_config(
    page_title="Pattern Breakout Scanner V2",
    layout="wide"
)

st.title("📈 Pattern Breakout Scanner V2")

# =========================
# SIDEBAR
# =========================

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

scan_mode = st.sidebar.selectbox(
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

price_min = st.sidebar.number_input(
    "Min Close Price",
    min_value=0.0,
    value=0.0
)

price_max = st.sidebar.number_input(
    "Max Close Price",
    min_value=0.0,
    value=100000.0
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

# =========================
# SCAN
# =========================

if scan:

    st.info(
        "Loading symbols..."
    )

    symbols = get_symbols(
        exchange
    )

    st.success(
        f"Symbols Loaded = {len(symbols)}"
    )

    symbols = symbols[:max_stocks]

    st.write(
        f"Scanning First {len(symbols)} Stocks"
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

                results.extend(
                    rows
                )

        except Exception as e:

            errors.append(
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

    if errors:

        with st.expander(
            "Show Errors"
        ):

            st.write(
                errors[:50]
            )

    if len(results):

        df = pd.DataFrame(
            results
        )

        # =====================
        # PRICE FILTER
        # =====================

        if "BreakoutPrice" in df.columns:

            df = df[
                (
                    df["BreakoutPrice"]
                    >= price_min
                )
                &
                (
                    df["BreakoutPrice"]
                    <= price_max
                )
            ]

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
            file_name="pattern_breakout_results.csv",
            mime="text/csv"
        )

    else:

        st.error(
            "No Results Found"
        )

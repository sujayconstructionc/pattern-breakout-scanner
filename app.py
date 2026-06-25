import streamlit as st
import pandas as pd

from data_loader import get_symbols
from scanner import scan_symbol

st.set_page_config(
    page_title="Pattern Breakout Scanner",
    layout="wide"
)

st.title("📈 Pattern Breakout Scanner")

st.sidebar.header("Scanner Filters")

exchange = st.sidebar.selectbox(
    "Exchange",
    ["NSE", "BSE", "NSE+BSE"]
)

market_cap_min = st.sidebar.number_input(
    "Min Market Cap (Cr)",
    min_value=0,
    value=300
)

market_cap_max = st.sidebar.number_input(
    "Max Market Cap (Cr)",
    min_value=0,
    value=20000
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

st.info(
    "Monthly Pattern Scanner (Testing Version)"
)

if scan:

    symbols = get_symbols(exchange)

    symbols = symbols[:max_stocks]

    results = []

    progress = st.progress(0)

    total = len(symbols)

    for i, symbol in enumerate(symbols):

        rows = scan_symbol(
            symbol=symbol,
            breakout_mode=breakout_mode
        )

        results.extend(rows)

        progress.progress(
            (i + 1) / total
        )

    if len(results) == 0:

        st.warning(
            "No pattern found"
        )

    else:

        df = pd.DataFrame(results)

        st.success(
            f"{len(df)} Signals Found"
        )

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

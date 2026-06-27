import streamlit as st
import pandas as pd

from data_loader import get_symbols
from scanner import (
scan_symbol,
scan_pattern_only
)

st.set_page_config(
page_title="Pattern Breakout Scanner V3",
layout="wide"
)

st.title("📈 Pattern Breakout Scanner V3")

# ==================================

# SIDEBAR

# ==================================

st.sidebar.header("Scanner Filters")

exchange = st.sidebar.selectbox(
"Exchange",
[
"NSE"
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
"Pattern + Breakout"
]
)

breakout_mode = st.sidebar.radio(
"Breakout Type",
[
"Close",
"High"
]
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

max_stocks = st.sidebar.number_input(
"Max Stocks To Scan",
min_value=1,
max_value=3000,
value=500
)

scan = st.sidebar.button(
"SCAN NOW"
)

# ==================================

# SCAN

# ==================================

if scan:

```
st.info("Loading NSE symbols...")

symbols = get_symbols("NSE")

symbols = symbols[:max_stocks]

st.success(
    f"Symbols Loaded = {len(symbols)}"
)

results = []

progress = st.progress(0)

total = len(symbols)

for i, symbol in enumerate(symbols):

    try:

        if scan_mode == "Pattern Only":

            rows = scan_pattern_only(
                symbol=symbol,
                timeframe=timeframe
            )

        else:

            rows = scan_symbol(
                symbol=symbol,
                timeframe=timeframe,
                breakout_mode=breakout_mode
            )

        if rows:

            results.extend(rows)

    except Exception:
        pass

    progress.progress(
        (i + 1) / total
    )

st.success(
    f"Scan Completed | Results = {len(results)}"
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
        "⬇ Download CSV",
        csv,
        file_name="scanner_results.csv",
        mime="text/csv"
    )

else:

    st.warning(
        "No pattern found"
    )
```

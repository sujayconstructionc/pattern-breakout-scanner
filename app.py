python
import streamlit as st
import pandas as pd

from data_loader import get_symbols
from scanner import scan_symbol, scan_pattern_only
from bse_mapper import get_bse_symbol_map

st.set_page_config(
    page_title="Pattern Breakout Scanner V5",
    layout="wide"
)

st.title("📈 Pattern Breakout Scanner V5")

# =====================================
# SIDEBAR
# =====================================

st.sidebar.header("Scanner Filters")

exchange = st.sidebar.selectbox(
    "Exchange",
    ["NSE", "BSE", "NSE+BSE"]
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
    max_value=20000,
    value=500
)

st.sidebar.markdown("---")

min_mcap = st.sidebar.number_input(
    "Min Market Cap (Cr)",
    value=300
)

max_mcap = st.sidebar.number_input(
    "Max Market Cap (Cr)",
    value=30000
)

min_price = st.sidebar.number_input(
    "Min CMP",
    value=0.0
)

max_price = st.sidebar.number_input(
    "Max CMP",
    value=100000.0
)

min_volume = st.sidebar.number_input(
    "Min Volume",
    value=0
)

scan = st.sidebar.button("SCAN NOW")

# =====================================
# SCAN
# =====================================

if scan:

    st.info(f"Loading {exchange} symbols...")

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
            st.write(errors[:100])

    if len(results):

        df = pd.DataFrame(results)

        # ==========================
        # FILTERS
        # ==========================

        if "MarketCapCr" in df.columns:

            df = df[
                (df["MarketCapCr"] >= min_mcap)
                &
                (df["MarketCapCr"] <= max_mcap)
            ]

        if "CMP" in df.columns:

            df = df[
                (df["CMP"] >= min_price)
                &
                (df["CMP"] <= max_price)
            ]

        if "Volume" in df.columns:

            df = df[
                df["Volume"] >= min_volume
            ]

        # ==========================
        # BSE MAP
        # ==========================

        try:

            bse_map = get_bse_symbol_map()

            df["TradingSymbol"] = df["Symbol"].apply(
                lambda x:
                bse_map.get(
                    x,
                    {}
                ).get(
                    "TradingSymbol",
                    ""
                )
            )

            df["Name"] = df["Symbol"].apply(
                lambda x:
                bse_map.get(
                    x,
                    {}
                ).get(
                    "Name",
                    ""
                )
            )

        except Exception:
            pass

        # ==========================
        # TRADINGVIEW LINK
        # ==========================

        def make_tv_link(sym):

            if sym.endswith(".NS"):

                base = sym.replace(".NS", "")

                return (
                    f"https://www.tradingview.com/chart/?symbol=NSE:{base}"
                )

            elif sym.endswith(".BO"):

                base = sym.replace(".BO", "")

                return (
                    f"https://www.tradingview.com/chart/?symbol=BSE:{base}"
                )

            return ""

        df["TradingView"] = df["Symbol"].apply(
            make_tv_link
        )

        # ==========================
        # SORT
        # ==========================

        if "PatternDate" in df.columns:

            df = df.sort_values(
                by="PatternDate",
                ascending=False
            )

        front_cols = []

        for col in [
            "Symbol",
            "TradingSymbol",
            "Name",
            "CMP",
            "MarketCapCr",
            "Volume",
            "RVOL",
            "Sector",
            "Industry"
        ]:

            if col in df.columns:
                front_cols.append(col)

        other_cols = [
            c for c in df.columns
            if c not in front_cols
        ]

        df = df[
            front_cols + other_cols
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
            file_name="scanner_results.csv",
            mime="text/csv"
        )

    else:

        st.warning(
            "No Results Found"
        )


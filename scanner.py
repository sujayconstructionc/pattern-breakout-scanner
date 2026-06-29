import pandas as pd
import yfinance as yf


# =====================================
# CLEAN YFINANCE DATA
# =====================================

def clean_yf_data(df):

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    return df


# =====================================
# CANDLE COLOR
# =====================================

def candle_color(row):

    if row["Close"] > row["Open"]:
        return "G"

    elif row["Close"] < row["Open"]:
        return "R"

    else:
        return "D"


# =====================================
# RESAMPLE
# =====================================

def resample_data(df, timeframe="Monthly"):

    if timeframe == "Monthly":

        df = df.resample("ME").agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })

    elif timeframe == "Quarterly":

        df = df.resample("QE").agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })

    elif timeframe == "6 Month":

        monthly = df.resample("ME").agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })

        monthly["Year"] = monthly.index.year

        monthly["Half"] = monthly.index.month.map(
            lambda x: 1 if x <= 6 else 2
        )

        df = monthly.groupby(
            ["Year", "Half"]
        ).agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })

        dates = []

        for yr, half in df.index:

            if half == 1:

                dates.append(
                    pd.Timestamp(
                        year=yr,
                        month=6,
                        day=30
                    )
                )

            else:

                dates.append(
                    pd.Timestamp(
                        year=yr,
                        month=12,
                        day=31
                    )
                )

        df.index = dates

    elif timeframe == "1 Year":

        df = df.resample("YE").agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })

    return df.dropna()


# =====================================
# PATTERN MATCH
# =====================================

def pattern_match(colors):

    bull = ["G", "R", "G", "R", "G"]
    bear = ["R", "G", "R", "G", "R"]

    return colors == bull or colors == bear


# =====================================
# PATTERN ONLY
# =====================================

def scan_pattern_only(
    symbol,
    timeframe="Monthly"
):

    try:

        df = yf.download(
            symbol,
            period="15y",
            progress=False,
            auto_adjust=False
        )

        if df is None or len(df) < 50:
            return []

        df = clean_yf_data(df)

        df = resample_data(
            df,
            timeframe
        )

        if len(df) < 10:
            return []

        df["Color"] = df.apply(
            candle_color,
            axis=1
        )

        results = []

        for i in range(5, len(df) + 1):

            block = df.iloc[i - 5:i]

            colors = block["Color"].tolist()

            if pattern_match(colors):

                results.append({

                    "Symbol": symbol,

                    "Timeframe": timeframe,

                    "PatternDate":
                        block.index[-1],

                    "PatternHigh":
                        round(
                            float(
                                block["High"].max()
                            ),
                            2
                        ),

                    "PatternLow":
                        round(
                            float(
                                block["Low"].min()
                            ),
                            2
                        ),

                    "Pattern":
                        "".join(colors)
                })

        return results

    except Exception as e:

        print(symbol, e)

        return []


# =====================================
# BREAKOUT SCAN
# =====================================

def scan_symbol(
    symbol,
    timeframe="Monthly",
    breakout_mode="Close",
    latest_only=False
):

    try:

        df = yf.download(
            symbol,
            period="15y",
            progress=False,
            auto_adjust=False
        )

        if df is None or len(df) < 50:
            return []

        df = clean_yf_data(df)

        df = resample_data(
            df,
            timeframe
        )

        if len(df) < 10:
            return []

        df["Color"] = df.apply(
            candle_color,
            axis=1
        )

        results = []

        latest_bar = df.index[-1]

        for i in range(5, len(df)):

            block = df.iloc[i - 5:i]

            colors = block["Color"].tolist()

            if not pattern_match(colors):
                continue

            pattern_high = block["High"].max()

            future = df.iloc[i:]

            breakout_date = None
            breakout_price = None

            for idx, row in future.iterrows():

                if breakout_mode == "High":

                    cond = (
                        row["High"]
                        > pattern_high
                    )

                else:

                    cond = (
                        row["Close"]
                        > pattern_high
                    )

                if cond:

                    breakout_date = idx

                    breakout_price = row["Close"]

                    break

            if breakout_date:

                if latest_only:

                    if breakout_date != latest_bar:
                        continue

                results.append({

                    "Symbol": symbol,

                    "Timeframe": timeframe,

                    "PatternDate":
                        block.index[-1],

                    "BreakoutDate":
                        breakout_date,

                    "PatternHigh":
                        round(
                            float(pattern_high),
                            2
                        ),

                    "BreakoutPrice":
                        round(
                            float(breakout_price),
                            2
                        )
                })

        return results

    except Exception as e:

        print(symbol, e)

        return []

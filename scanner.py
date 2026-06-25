import pandas as pd
import yfinance as yf


# =========================
# YFINANCE FIX
# =========================

def clean_yf_data(df):

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    return df


# =========================
# CANDLE COLOR
# =========================

def candle_color(row):

    if row["Close"] > row["Open"]:
        return "G"

    elif row["Close"] < row["Open"]:
        return "R"

    return "D"


# =========================
# RESAMPLING
# =========================

def resample_data(df, timeframe):

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

        df = df.resample("2QE").agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })

    return df.dropna()


# =========================
# PATTERN
# =========================

def pattern_match(colors):

    bull = ["G", "R", "G", "R", "G"]

    bear = ["R", "G", "R", "G", "R"]

    if colors == bull:
        return "GRGRG"

    if colors == bear:
        return "RGRGR"

    return None


# =========================
# PATTERN ONLY
# =========================

def scan_pattern_only(symbol, timeframe):

    try:

        df = yf.download(
            symbol,
            period="15y",
            auto_adjust=False,
            progress=False
        )

        if len(df) < 50:
            return []

        df = clean_yf_data(df)

        df = resample_data(
            df,
            timeframe
        )

        df["Color"] = df.apply(
            candle_color,
            axis=1
        )

        results = []

        for i in range(5, len(df)+1):

            block = df.iloc[i-5:i]

            pattern = pattern_match(
                block["Color"].tolist()
            )

            if pattern:

                results.append({

                    "Symbol": symbol,

                    "Timeframe": timeframe,

                    "Pattern": pattern,

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
                        )
                })

        return results

    except:

        return []


# =========================
# BREAKOUT SCANNER
# =========================

def scan_symbol(
        symbol,
        timeframe,
        breakout_mode,
        latest_only=False
):

    try:

        df = yf.download(
            symbol,
            period="15y",
            auto_adjust=False,
            progress=False
        )

        if len(df) < 50:
            return []

        df = clean_yf_data(df)

        df = resample_data(
            df,
            timeframe
        )

        df["Color"] = df.apply(
            candle_color,
            axis=1
        )

        results = []

        for i in range(5, len(df)):

            block = df.iloc[i-5:i]

            pattern = pattern_match(
                block["Color"].tolist()
            )

            if not pattern:
                continue

            pattern_high = (
                block["High"].max()
            )

            pattern_date = (
                block.index[-1]
            )

            future = df.iloc[i:]

            breakout_found = False

            for idx, row in future.iterrows():

                if breakout_mode == "Close":

                    cond = (
                        row["Close"]
                        > pattern_high
                    )

                else:

                    cond = (
                        row["High"]
                        > pattern_high
                    )

                if cond:

                    months = (
                        (
                            idx.year -
                            pattern_date.year
                        ) * 12
                    ) + (
                        idx.month -
                        pattern_date.month
                    )

                    results.append({

                        "Symbol":
                            symbol,

                        "Timeframe":
                            timeframe,

                        "Pattern":
                            pattern,

                        "PatternDate":
                            pattern_date,

                        "PatternHigh":
                            round(
                                float(
                                    pattern_high
                                ),
                                2
                            ),

                        "BreakoutDate":
                            idx,

                        "MonthsToBreakout":
                            months,

                        "BreakoutPrice":
                            round(
                                float(
                                    row["Close"]
                                ),
                                2
                            )
                    })

                    breakout_found = True

                    break

            if (
                latest_only and
                breakout_found and
                len(results)
            ):

                return [results[-1]]

        return results

    except:

        return []

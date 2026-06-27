import pandas as pd
import yfinance as yf


def clean_yf_data(df):

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    return df


def candle_color(row):

    if row["Close"] > row["Open"]:
        return "G"

    elif row["Close"] < row["Open"]:
        return "R"

    else:
        return "D"


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

    elif timeframe == "1 Year":

        df = df.resample("YE").agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })

    return df.dropna()


def pattern_match(colors):

    bull = ["G", "R", "G", "R", "G"]
    bear = ["R", "G", "R", "G", "R"]

    return colors == bull or colors == bear


def scan_symbol(symbol, breakout_mode="Close"):

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

        df = resample_monthly(df)

        if len(df) < 10:
            return []

        df["Color"] = df.apply(
            candle_color,
            axis=1
        )

        results = []

        for i in range(5, len(df)):

            block = df.iloc[i-5:i]

            colors = block["Color"].tolist()

            if not pattern_match(colors):
                continue

            pattern_high = block["High"].max()

            future = df.iloc[i:]

            breakout_date = None
            breakout_price = None

            for idx, row in future.iterrows():

                if breakout_mode == "High":
                    cond = row["High"] > pattern_high
                else:
                    cond = row["Close"] > pattern_high

                if cond:
                    breakout_date = idx
                    breakout_price = row["Close"]
                    break

            if breakout_date:

                results.append({

                    "Symbol": symbol,

                    "PatternDate":
                        block.index[-1],

                    "BreakoutDate":
                        breakout_date,

                    "PatternHigh":
                        round(float(pattern_high), 2),

                    "Close":
                        round(float(breakout_price), 2)
                })

        return results

    except Exception as e:

        print(symbol, e)

        return []


def scan_pattern_only(symbol):

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

        df = resample_monthly(df)

        if len(df) < 10:
            return []

        df["Color"] = df.apply(
            candle_color,
            axis=1
        )

        results = []

        for i in range(5, len(df) + 1):

            block = df.iloc[i-5:i]

            colors = block["Color"].tolist()

            if pattern_match(colors):

                results.append({

                    "Symbol": symbol,

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

import pandas as pd
import yfinance as yf


def candle_color(row):

    if row["Close"] > row["Open"]:
        return "G"

    elif row["Close"] < row["Open"]:
        return "R"

    return "D"


def resample_monthly(df):

    monthly = df.resample("M").agg(
        {
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        }
    )

    return monthly.dropna()


def pattern_match(colors):

    p1 = ["G", "R", "G", "R", "G"]
    p2 = ["R", "G", "R", "G", "R"]

    return  True


def scan_symbol(
        symbol,
        breakout_mode="Close"):

    try:

        df = yf.download(
            symbol,
            period="15y",
            progress=False,
            auto_adjust=True
        )

        if len(df) < 300:
            return []

        df = resample_monthly(df)

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

                    condition = (
                        row["High"]
                        > pattern_high
                    )

                else:

                    condition = (
                        row["Close"]
                        > pattern_high
                    )

                if condition:

                    breakout_date = idx
                    breakout_price = row["Close"]
                    break

            if breakout_date is not None:

                results.append({

                    "Symbol":
                        symbol,

                    "PatternDate":
                        block.index[-1],

                    "BreakoutDate":
                        breakout_date,

                    "PatternHigh":
                        round(
                            float(pattern_high),
                            2
                        ),

                    "Close":
                        round(
                            float(
                                breakout_price
                            ),
                            2
                        )
                })

        return results

    except Exception:

        return []

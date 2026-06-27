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

    if colors == bull:
        return "GRGRG"

    if colors == bear:
        return "RGRGR"

    return None


def scan_pattern_only(symbol, timeframe):

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

            pattern = pattern_match(
                colors
            )

            if pattern:

                results.append({

                    "Symbol": symbol,

                    "Timeframe": timeframe,

                    "Pattern": pattern,

                    "Colors":
                        "".join(colors),

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

        # DEBUG
        if len(results) == 0:

            last10 = "".join(
                df["Color"]
                .tail(10)
                .tolist()
            )

            results.append({

                "Symbol": symbol,

                "Timeframe": timeframe,

                "Pattern":
                    "NOT_FOUND",

                "Colors":
                    last10,

                "PatternDate":
                    df.index[-1],

                "PatternHigh":
                    round(
                        float(
                            df["High"]
                            .tail(5)
                            .max()
                        ),
                        2
                    ),

                "PatternLow":
                    round(
                        float(
                            df["Low"]
                            .tail(5)
                            .min()
                        ),
                        2
                    )
            })

        return results

    except Exception as e:

        return [{

            "Symbol": symbol,

            "Timeframe": timeframe,

            "Pattern":
                "ERROR",

            "Colors":
                str(e),

            "PatternDate":
                "",

            "PatternHigh":
                0,

            "PatternLow":
                0
        }]


def scan_symbol(
    symbol,
    timeframe,
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

        if len(df) < 50:
            return []

        df = clean_yf_data(df)

        df = resample_data(df, timeframe)

        if len(df) < 10:
            return []

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

            pattern_high = block["High"].max()

            future = df.iloc[i:]

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

                    results.append({

                        "Symbol": symbol,
                        "Timeframe": timeframe,
                        "Pattern": pattern,
                        "PatternDate": block.index[-1],
                        "BreakoutDate": idx,
                        "PatternHigh": round(float(pattern_high), 2),
                        "BreakoutPrice": round(float(row["Close"]), 2)

                    })

                    break

        if latest_only and len(results):

            return [results[-1]]

        return results

    except Exception:

        return []
def scan_symbol(
    symbol,
    timeframe,
    breakout_mode="Close",
    latest_only=False
):
    return []


def scan_pattern_only(
    symbol,
    timeframe
):
    return []

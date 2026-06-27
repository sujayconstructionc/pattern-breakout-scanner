import pandas as pd
import yfinance as yf

def clean_yf_data(df):

```
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel(1)

return df
```

def candle_color(row):

```
if row["Close"] > row["Open"]:
    return "G"

elif row["Close"] < row["Open"]:
    return "R"

return "D"
```

def resample_data(df, timeframe):

```
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
```

def pattern_match(colors):

```
bull = ["G", "R", "G", "R", "G"]
bear = ["R", "G", "R", "G", "R"]

return colors == bull or colors == bear
```

def scan_pattern_only(symbol, timeframe="Monthly"):

```
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

        block = df.iloc[i-5:i]

        colors = block["Color"].tolist()

        if pattern_match(colors):

            results.append({

                "Symbol": symbol,
                "Timeframe": timeframe,
                "Pattern": "".join(colors),
                "PatternDate": block.index[-1],
                "PatternHigh": round(float(block["High"].max()), 2),
                "PatternLow": round(float(block["Low"].min()), 2)

            })

    return results

except Exception as e:

    print(symbol, e)

    return []
```

def scan_symbol(
symbol,
timeframe="Monthly",
breakout_mode="Close"
):

```
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

    for i in range(5, len(df)):

        block = df.iloc[i-5:i]

        colors = block["Color"].tolist()

        if not pattern_match(colors):
            continue

        pattern_high = block["High"].max()

        future = df.iloc[i:]

        for idx, row in future.iterrows():

            if breakout_mode == "High":

                cond = row["High"] > pattern_high

            else:

                cond = row["Close"] > pattern_high

            if cond:

                results.append({

                    "Symbol": symbol,
                    "Timeframe": timeframe,
                    "PatternDate": block.index[-1],
                    "BreakoutDate": idx,
                    "PatternHigh": round(float(pattern_high), 2),
                    "BreakoutPrice": round(float(row["Close"]), 2)

                })

                break

    return results

except Exception as e:

    print(symbol, e)

    return []
```

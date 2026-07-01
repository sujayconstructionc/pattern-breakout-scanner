import pandas as pd
import yfinance as yf

# =====================================

# CLEAN DATA

# =====================================

def clean_yf_data(df):

```
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel(1)

return df
```

# =====================================

# COMPANY INFO

# =====================================

def get_stock_info(symbol):

```
try:

    info = yf.Ticker(symbol).info

    return {
        "MarketCapCr": round(
            info.get("marketCap", 0) / 10000000,
            2
        ),
        "Sector": info.get("sector", ""),
        "Industry": info.get("industry", "")
    }

except:

    return {
        "MarketCapCr": 0,
        "Sector": "",
        "Industry": ""
    }
```

# =====================================

# CANDLE COLOR

# =====================================

def candle_color(row):

```
if row["Close"] > row["Open"]:
    return "G"

elif row["Close"] < row["Open"]:
    return "R"

return "D"
```

# =====================================

# RESAMPLE

# =====================================

def resample_data(df, timeframe):

```
if timeframe == "Monthly":

    return df.resample("ME").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

elif timeframe == "Quarterly":

    return df.resample("QE").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

elif timeframe == "1 Year":

    return df.resample("YE").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

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

    out = monthly.groupby(
        ["Year", "Half"]
    ).agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    })

    dates = []

    for y, h in out.index:

        if h == 1:

            dates.append(
                pd.Timestamp(
                    year=y,
                    month=6,
                    day=30
                )
            )

        else:

            dates.append(
                pd.Timestamp(
                    year=y,
                    month=12,
                    day=31
                )
            )

    out.index = dates

    return out

return df
```

# =====================================

# PATTERN MATCH

# =====================================

def pattern_match(colors):

```
bull = ["G", "R", "G", "R", "G"]
bear = ["R", "G", "R", "G", "R"]

return colors == bull or colors == bear
```

# =====================================

# PATTERN ONLY

# =====================================

def scan_pattern_only(
symbol,
timeframe="Monthly"
):

```
try:

    raw = yf.download(
        symbol,
        period="15y",
        progress=False,
        auto_adjust=False
    )

    if raw is None or len(raw) < 100:
        return []

    raw = clean_yf_data(raw)

    cmp_price = round(
        float(raw["Close"].iloc[-1]),
        2
    )

    volume = int(
        raw["Volume"].iloc[-1]
    )

    avg20 = int(
        raw["Volume"].tail(20).mean()
    )

    rvol = round(
        volume / avg20,
        2
    ) if avg20 else 0

    info = get_stock_info(symbol)

    df = resample_data(
        raw,
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
                "PatternDate": block.index[-1],

                "Pattern":
                "".join(colors),

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

                "CMP": cmp_price,
                "Volume": volume,
                "AvgVolume20": avg20,
                "RVOL": rvol,

                "MarketCapCr":
                info["MarketCapCr"],

                "Sector":
                info["Sector"],

                "Industry":
                info["Industry"]
            })

    return results

except Exception as e:

    print(symbol, e)

    return []
```

# =====================================

# BREAKOUT SCAN

# =====================================

def scan_symbol(
symbol,
timeframe="Monthly",
breakout_mode="Close",
latest_only=False
):

```
try:

    raw = yf.download(
        symbol,
        period="15y",
        progress=False,
        auto_adjust=False
    )

    if raw is None or len(raw) < 100:
        return []

    raw = clean_yf_data(raw)

    cmp_price = round(
        float(raw["Close"].iloc[-1]),
        2
    )

    volume = int(
        raw["Volume"].iloc[-1]
    )

    avg20 = int(
        raw["Volume"].tail(20).mean()
    )

    rvol = round(
        volume / avg20,
        2
    ) if avg20 else 0

    info = get_stock_info(symbol)

    df = resample_data(
        raw,
        timeframe
    )

    if len(df) < 10:
        return []

    df["Color"] = df.apply(
        candle_color,
        axis=1
    )

    latest_bar = df.index[-1]

    results = []

    for i in range(5, len(df)):

        block = df.iloc[i-5:i]

        colors = block["Color"].tolist()

        if not pattern_match(colors):
            continue

        pattern_high = float(
            block["High"].max()
        )

        future = df.iloc[i:]

        breakout_date = None
        breakout_price = None

        for idx, row in future.iterrows():

            if breakout_mode == "High":

                condition = (
                    row["High"] > pattern_high
                )

            else:

                condition = (
                    row["Close"] > pattern_high
                )

            if condition:

                breakout_date = idx
                breakout_price = float(
                    row["Close"]
                )

                break

        if breakout_date is None:
            continue

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

            "Pattern":
            "".join(colors),

            "PatternHigh":
            round(pattern_high, 2),

            "BreakoutPrice":
            round(breakout_price, 2),

            "CMP":
            cmp_price,

            "Volume":
            volume,

            "AvgVolume20":
            avg20,

            "RVOL":
            rvol,

            "MarketCapCr":
            info["MarketCapCr"],

            "Sector":
            info["Sector"],

            "Industry":
            info["Industry"]
        })

    return results

except Exception as e:

    print(symbol, e)

    return []
```

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
# COMPANY INFO
# =====================================

def get_stock_info(symbol):
    try:
        tk = yf.Ticker(symbol)
        info = tk.info

        market_cap = info.get("marketCap", 0)
        market_cap_cr = round(market_cap / 10000000, 2)

        return {
            "MarketCapCr": market_cap_cr,
            "Sector": info.get("sector", ""),
            "Industry": info.get("industry", "")
        }

    except Exception:
        return {
            "MarketCapCr": 0,
            "Sector": "",
            "Industry": ""
        }


# =====================================
# CANDLE COLOR
# =====================================

def candle_color(row):
    if row["Close"] > row["Open"]:
        return "G"
    elif row["Close"] < row["Open"]:
        return "R"
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

    elif timeframe == "1 Year":
        df = df.resample("YE").agg({
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
                    pd.Timestamp(year=yr, month=6, day=30)
                )
            else:
                dates.append(
                    pd.Timestamp(year=yr, month=12, day=31)
                )

        df.index = dates

    return df.dropna()


# =====================================
# PATTERN MATCH
# =====================================

def pattern_match(colors):

    bull = ["G", "R", "G", "R", "G"]
    bear = ["R", "G", "R", "G", "R"]

    return colors == bull or colors == bear

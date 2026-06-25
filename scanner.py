import pandas as pd
import yfinance as yf


def scan_symbol(symbol, breakout_mode="Close"):
    return []


def scan_pattern_only(symbol):

    try:

        if symbol != "RELIANCE.NS":
            return []

        df = yf.download(
            symbol,
            period="15y",
            progress=False,
            auto_adjust=False
        )

        monthly = df.resample("ME").agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })

        monthly = monthly.dropna()

        colors = []

        for _, row in monthly.tail(30).iterrows():

            if row["Close"] > row["Open"]:
                colors.append("G")

            elif row["Close"] < row["Open"]:
                colors.append("R")

            else:
                colors.append("D")

        return [{
            "Symbol": symbol,
            "MonthlyCandles": len(monthly),
            "Last30Colors": "".join(colors)
        }]

    except Exception as e:

        return [{
            "Symbol": symbol,
            "MonthlyCandles": 0,
            "Last30Colors": str(e)
        }]

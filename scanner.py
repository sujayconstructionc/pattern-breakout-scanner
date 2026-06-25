import yfinance as yf
import pandas as pd


def scan_symbol(symbol, breakout_mode="Close"):
    return []


def scan_pattern_only(symbol):

    try:

        if symbol != "RELIANCE.NS":
            return []

        df = yf.download(
            symbol,
            period="15y",
            auto_adjust=False,
            progress=False
        )

        return [{
            "Symbol": symbol,
            "MonthlyCandles": len(df),
            "Last30Colors": str(df.columns.tolist())
        }]

    except Exception as e:

        return [{
            "Symbol": symbol,
            "MonthlyCandles": 0,
            "Last30Colors": str(e)
        }]

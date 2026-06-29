import yfinance as yf
import pandas as pd

df = yf.download(
    "CUPID.BO",
    period="15y",
    progress=False,
    auto_adjust=False
)

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel(1)

sixm = df.resample("2QE").agg({
    "Open":"first",
    "High":"max",
    "Low":"min",
    "Close":"last",
    "Volume":"sum"
}).dropna()

sixm["Color"] = sixm.apply(
    lambda r: "G" if r["Close"] > r["Open"]
    else "R" if r["Close"] < r["Open"]
    else "D",
    axis=1
)

print("\n===== LAST 20 SIX MONTH CANDLES =====\n")

print(
    sixm[
        ["Open","High","Low","Close","Color"]
    ].tail(20)
)

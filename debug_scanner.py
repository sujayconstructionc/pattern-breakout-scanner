import pandas as pd
import yfinance as yf


def candle_color(row):

    if row["Close"] > row["Open"]:
        return "G"

    elif row["Close"] < row["Open"]:
        return "R"

    else:
        return "D"


def resample_data(df, timeframe):

    if timeframe == "Monthly":

        return df.resample("ME").agg({
            "Open":"first",
            "High":"max",
            "Low":"min",
            "Close":"last",
            "Volume":"sum"
        })

    elif timeframe == "Quarterly":

        return df.resample("QE").agg({
            "Open":"first",
            "High":"max",
            "Low":"min",
            "Close":"last",
            "Volume":"sum"
        })

    elif timeframe == "6 Month":

        return df.resample("2QE").agg({
            "Open":"first",
            "High":"max",
            "Low":"min",
            "Close":"last",
            "Volume":"sum"
        })

    elif timeframe == "1 Year":

        return df.resample("YE").agg({
            "Open":"first",
            "High":"max",
            "Low":"min",
            "Close":"last",
            "Volume":"sum"
        })

    return df


def debug_symbol(
    symbol="CUPID.BO",
    timeframe="6 Month"
):

    print(f"\nDEBUG SYMBOL = {symbol}")

    df = yf.download(
        symbol,
        period="15y",
        auto_adjust=False,
        progress=False
    )

    if len(df) == 0:

        print("NO DATA")
        return

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    df = resample_data(
        df,
        timeframe
    )

    df = df.dropna()

    df["Color"] = df.apply(
        candle_color,
        axis=1
    )

    print("\nLAST 20 CANDLES\n")

    print(df[
        [
            "Open",
            "High",
            "Low",
            "Close",
            "Color"
        ]
    ].tail(20))

    print("\nPATTERN CHECK\n")

    for i in range(5, len(df)+1):

        block = df.iloc[i-5:i]

        colors = block["Color"].tolist()

        print(
            block.index[-1].date(),
            colors
        )


if __name__ == "__main__":

    debug_symbol(
        "CUPID.BO",
        "6 Month"
    )

    debug_symbol(
        "AURIONPRO.NS",
        "6 Month"
    )

import pandas as pd


def get_nse_symbols():

    try:

        df = pd.read_csv("nse_symbols.csv")

        return [
            f"{x}.NS"
            for x in df["SYMBOL"].dropna().tolist()
        ]

    except Exception:

        return []


def get_bse_symbols():

    return []


def get_symbols(exchange):

    if exchange == "NSE":
        return get_nse_symbols()

    elif exchange == "BSE":
        return get_bse_symbols()

    elif exchange == "NSE+BSE":
        return (
            get_nse_symbols()
            + get_bse_symbols()
        )

    return []

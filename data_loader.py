import pandas as pd

def get_nse_symbols():
    """
    Demo NSE list.
    बाद में full NSE universe जोड़ेंगे.
    """
    return [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS",
        "SBIN.NS",
        "LT.NS",
        "BHARTIARTL.NS",
        "ITC.NS",
        "AXISBANK.NS"
    ]


def get_bse_symbols():
    """
    Demo BSE list.
    बाद में full BSE universe जोड़ेंगे.
    """
    return [
        "RELIANCE.BO",
        "TCS.BO",
        "INFY.BO",
        "HDFCBANK.BO",
        "ICICIBANK.BO",
        "SBIN.BO"
    ]


def get_symbols(exchange):

    if exchange == "NSE":
        return get_nse_symbols()

    elif exchange == "BSE":
        return get_bse_symbols()

    elif exchange == "NSE+BSE":
        return get_nse_symbols() + get_bse_symbols()

    return []

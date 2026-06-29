import pandas as pd
import streamlit as st


@st.cache_data(ttl=86400)
def get_bse_master():

    try:

        # BSE Scrip Master
        # Columns:
        # Scrip Code
        # Instrument Code
        # ISIN
        #
        # BSE security master format documented by BSE
        # and includes Scrip Code and ISIN. :contentReference[oaicite:0]{index=0}

        url = (
            "https://developer.paytmmoney.com/"
            "data/v1/scrips/bse_security_master.csv"
        )

        df = pd.read_csv(url)

        return df

    except:

        return pd.DataFrame()


def get_bse_yahoo_symbols():

    df = get_bse_master()

    if len(df) == 0:
        return []

    possible_cols = [
        "SEM_SMST_SECURITY_ID",
        "SecurityId",
        "Scrip Code",
        "security_id"
    ]

    code_col = None

    for c in possible_cols:

        if c in df.columns:

            code_col = c
            break

    if code_col is None:
        return []

    symbols = []

    for code in df[code_col].dropna():

        symbols.append(
            f"{int(code)}.BO"
        )

    return symbols

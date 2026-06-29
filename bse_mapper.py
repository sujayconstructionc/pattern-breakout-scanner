import pandas as pd
import streamlit as st


@st.cache_data(ttl=86400)
def get_bse_master():

    try:

        url = (
            "https://developer.paytmmoney.com/"
            "data/v1/scrips/bse_security_master.csv"
        )

        df = pd.read_csv(url)

        return df

    except Exception:

        return pd.DataFrame()


def get_bse_yahoo_symbols():

    df = get_bse_master()

    if len(df) == 0:
        return []

    # Debug
    print(df.columns.tolist())

    code_col = None

    preferred_cols = [
        "Scrip Code",
        "SCRIP_CODE",
        "SC_CODE",
        "BSECODE",
        "BSE_CODE"
    ]

    for c in preferred_cols:

        if c in df.columns:

            code_col = c
            break

    # Fallback
    if code_col is None:

        numeric_cols = []

        for c in df.columns:

            try:

                sample = (
                    df[c]
                    .dropna()
                    .astype(str)
                    .head(20)
                )

                if all(
                    len(x) == 6
                    and x.isdigit()
                    for x in sample
                ):
                    numeric_cols.append(c)

            except:
                pass

        if len(numeric_cols):

            code_col = numeric_cols[0]

    if code_col is None:
        return []

    symbols = []

    for code in df[code_col].dropna():

        try:

            code = str(int(float(code)))

            if len(code) == 6:

                symbols.append(
                    f"{code}.BO"
                )

        except:
            pass

    symbols = list(dict.fromkeys(symbols))

    return symbols

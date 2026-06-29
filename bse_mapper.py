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

    except Exception as e:

        print(e)

        return pd.DataFrame()


def get_bse_yahoo_symbols():

    df = get_bse_master()

    if len(df) == 0:
        return []

    print(df.columns.tolist())

    # TEMP TEST
    return [
        "500325.BO",
        "500209.BO",
        "532540.BO",
        "500180.BO",
        "532174.BO",
        "500112.BO",
        "532215.BO",
        "500696.BO",
        "500875.BO",
        "532978.BO"
    ]

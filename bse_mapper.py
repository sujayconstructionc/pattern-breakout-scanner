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

        print("BSE MASTER ERROR:", e)

        return pd.DataFrame()


def get_bse_yahoo_symbols():

    df = get_bse_master()

    if len(df) == 0:
        return []

    # ==========================
    # DEBUG OUTPUT
    # ==========================

    st.write("BSE Columns")
    st.write(df.columns.tolist())

    st.write("BSE Sample Data")
    st.dataframe(df.head(20))

    print(df.columns.tolist())
    print(df.head(20))

    # TEMP SYMBOLS
    return [
        "500325.BO",  # Reliance
        "500209.BO",  # Infosys
        "532540.BO",  # TCS
        "500180.BO",  # HDFC Bank
        "532174.BO",  # ICICI Bank
        "500112.BO",  # SBI
        "532215.BO",  # Axis Bank
        "500696.BO",  # HUL
        "500875.BO",  # ITC
        "532978.BO"   # Bajaj Finserv
    ]

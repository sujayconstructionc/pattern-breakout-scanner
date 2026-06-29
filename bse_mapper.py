import pandas as pd
import streamlit as st

@st.cache_data(ttl=86400)
def get_equity_master():

    try:

        url = (
            "https://developer.paytmmoney.com/"
            "data/v1/scrips/equity_security_master.csv"
        )

        return pd.read_csv(url)

    except Exception as e:

        st.error(e)

        return pd.DataFrame()


def get_bse_yahoo_symbols():

    df = get_equity_master()

    if len(df) == 0:
        return []

    st.write(df.columns.tolist())
    st.dataframe(df.head(20))

    # केवल BSE Equity
    bse = df[
        df["exchange"].astype(str).str.upper() == "BSE"
    ].copy()

    symbols = []

    for _, row in bse.iterrows():

        try:

            code = str(int(row["security_id"]))

            if len(code) == 6:
                symbols.append(f"{code}.BO")

        except:
            pass

    return list(dict.fromkeys(symbols))

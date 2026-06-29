import pandas as pd
import streamlit as st

@st.cache_data(ttl=86400)
def get_equity_master():

```
try:

    url = (
        "https://developer.paytmmoney.com/"
        "data/v1/scrips/equity_security_master.csv"
    )

    return pd.read_csv(url)

except Exception as e:

    st.error(f"Equity Master Error: {e}")

    return pd.DataFrame()
```

@st.cache_data(ttl=86400)
def get_bse_symbol_map():

```
df = get_equity_master()

if len(df) == 0:
    return {}

bse = df[
    df["exchange"]
    .astype(str)
    .str.upper()
    == "BSE"
].copy()

symbol_map = {}

for _, row in bse.iterrows():

    try:

        code = str(int(row["security_id"]))

        if len(code) != 6:
            continue

        yahoo_symbol = f"{code}.BO"

        symbol_map[yahoo_symbol] = {

            "Code": code,

            "TradingSymbol":
                str(row.get("symbol", "")),

            "Name":
                str(row.get("name", ""))
        }

    except:
        pass

return symbol_map
```

@st.cache_data(ttl=86400)
def get_bse_yahoo_symbols():

```
return list(
    get_bse_symbol_map().keys()
)
```

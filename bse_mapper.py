def get_bse_yahoo_symbols():

    df = get_bse_master()

    print(df.columns.tolist())

    if len(df) == 0:
        return []

    ...

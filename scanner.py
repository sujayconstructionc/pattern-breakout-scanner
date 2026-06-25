def scan_pattern_only(symbol):

    try:

        df = yf.download(
            symbol,
            period="15y",
            progress=False,
            auto_adjust=True
        )

        if len(df) < 300:
            return []

        df = resample_monthly(df)

        df["Color"] = df.apply(
            candle_color,
            axis=1
        )

        results = []

        for i in range(5, len(df)+1):

            block = df.iloc[i-5:i]

            colors = block["Color"].tolist()

            if pattern_match(colors):

                results.append({

                    "Symbol": symbol,

                    "PatternDate":
                        block.index[-1],

                    "PatternHigh":
                        round(
                            float(
                                block["High"].max()
                            ),
                            2
                        )
                })

        return results

    except Exception:

        return []

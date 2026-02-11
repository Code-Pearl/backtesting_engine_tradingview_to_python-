import os
import pandas as pd
import yfinance as yf

def load_data(symbol,start,end):

    os.makedirs("data_cache",exist_ok=True)
    cache=f"data_cache/{symbol}.parquet"

    if os.path.exists(cache):
        df=pd.read_parquet(cache)
    else:
        df=yf.download(
            symbol,
            start=start,
            end=end,
            auto_adjust=False,
            progress=False
        )

        if isinstance(df.columns,pd.MultiIndex):
            df.columns=df.columns.get_level_values(0)

        df.to_parquet(cache)

    return df[['Open','High','Low','Close','Volume']].dropna()

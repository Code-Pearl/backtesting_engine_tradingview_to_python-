# mtf.py

import pandas as pd

def resample_tf(df,tf):

    o=df['Open'].resample(tf).first()
    h=df['High'].resample(tf).max()
    l=df['Low'].resample(tf).min()
    c=df['Close'].resample(tf).last()
    v=df['Volume'].resample(tf).sum()

    out=pd.concat([o,h,l,c,v],axis=1)
    out.columns=['Open','High','Low','Close','Volume']
    return out.dropna()

def security(base_df,higher_df):

    aligned=higher_df.reindex(base_df.index,method='ffill')
    return aligned

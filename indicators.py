import numpy as np

def alma(series,window,offset,sigma):

    m=offset*(window-1)
    s=window/sigma

    weights=np.exp(-((np.arange(window)-m)**2)/(2*s*s))
    weights/=weights.sum()

    return series.rolling(window).apply(
        lambda x:np.dot(x,weights),
        raw=True
    )

def heikin_ashi(df):

    ha=df.copy()

    ha['Close']=(df['Open']+df['High']+df['Low']+df['Close'])/4
    ha['Open']=df['Open'].copy()

    for i in range(1,len(df)):
        ha['Open'].iloc[i]=(ha['Open'].iloc[i-1]+ha['Close'].iloc[i-1])/2

    ha['High']=ha[['Open','Close','High']].max(axis=1)
    ha['Low']=ha[['Open','Close','Low']].min(axis=1)

    return ha

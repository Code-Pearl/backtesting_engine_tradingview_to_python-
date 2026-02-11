import pandas as pd

def run_backtest(df,slippage=0.0002,capital=100000):

    position=0
    shares=0
    cash=capital

    equity=[]
    trades=[]

    for i in range(1,len(df)):

        openp=df['Open'].iloc[i]
        closep=df['Close'].iloc[i]

        long_sig=bool(df['long_signal'].iloc[i])
        short_sig=bool(df['short_signal'].iloc[i])

        if long_sig and position<=0:

            fill=openp*(1+slippage)

            if position<0:
                cash-=shares*fill

            shares=int(cash//fill)
            cash-=shares*fill
            position=1

            trades.append(("BUY",df.index[i],fill))

        elif short_sig and position>=0:

            fill=openp*(1-slippage)

            if position>0:
                cash+=shares*fill

            shares=int(cash//fill)
            cash+=shares*fill
            position=-1

            trades.append(("SELL",df.index[i],fill))

        if position==1:
            nav=cash+shares*closep
        elif position==-1:
            nav=cash-shares*closep
        else:
            nav=cash

        equity.append(nav)

    df=df.iloc[1:]
    df['Equity']=equity

    returns=pd.Series(equity,index=df.index).pct_change().dropna()

    return df,trades,returns

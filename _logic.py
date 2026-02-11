import numpy as np
import pandas as pd

# ---------------------------------------------------
# MOVING AVERAGE VARIANT ENGINE (1:1 PORT)
# ---------------------------------------------------
def variant(ma_type, src, length, off_sig, off_alma):

    sma = src.rolling(length).mean()
    ema = src.ewm(span=length, adjust=False).mean()
    dema = 2*ema - ema.ewm(span=length, adjust=False).mean()
    tema = 3*(ema - ema.ewm(span=length, adjust=False).mean()) + ema.ewm(span=length, adjust=False).mean().ewm(span=length, adjust=False).mean()
    wma = src.rolling(length).apply(lambda x: np.dot(x, np.arange(1,len(x)+1))/np.arange(1,len(x)+1).sum(), raw=True)

    hull = wma.rolling(int(np.sqrt(length))).mean()

    # ALMA
    m = off_alma*(length-1)
    s = length/off_sig if off_sig>0 else length
    weights = np.exp(-((np.arange(length)-m)**2)/(2*s*s))
    weights/=weights.sum()
    alma = src.rolling(length).apply(lambda x: np.dot(x,weights),raw=True)

    if ma_type=="TEMA":
        return tema
    elif ma_type=="HullMA":
        return hull
    elif ma_type=="ALMA":
        return alma
    else:
        return sma


# ---------------------------------------------------
# MTF RESOLUTION ENGINE (reso() PORT)
# ---------------------------------------------------
def reso(series, use_res, strat_res):

    if not use_res:
        return series

    tf = f"{int(strat_res)}T"
    resampled = series.resample(tf).last()
    aligned = resampled.reindex(series.index,method='ffill')

    return aligned


# ---------------------------------------------------
# MAIN SAIYAN SIGNAL GENERATOR
# ---------------------------------------------------
def build_signals(df, settings):

    delay = settings["delayOffset"]
    basisType = settings["basisType"]
    basisLen = settings["basisLen"]
    offSigma = settings["offsetSigma"]
    offALMA = settings["offsetALMA"]
    useRes = settings["useRes"]
    stratRes = settings["stratRes"]

    close_src = df["Close"].shift(delay)
    open_src  = df["Open"].shift(delay)

    close_series = variant(basisType, close_src, basisLen, offSigma, offALMA)
    open_series  = variant(basisType, open_src , basisLen, offSigma, offALMA)

    close_alt = reso(close_series,useRes,stratRes)
    open_alt  = reso(open_series ,useRes,stratRes)

    df["closeSeriesAlt"]=close_alt
    df["openSeriesAlt"]=open_alt

    # EXACT PINE CONDITIONS
    df["buy"]  = (df["closeSeriesAlt"].shift(1) < df["openSeriesAlt"].shift(1)) & (df["closeSeriesAlt"] > df["openSeriesAlt"])
    df["sell"] = (df["closeSeriesAlt"].shift(1) > df["openSeriesAlt"].shift(1)) & (df["closeSeriesAlt"] < df["openSeriesAlt"])

    # NON REPAINT CONFIRM
    df["long_signal"]=df["buy"].shift(1)
    df["short_signal"]=df["sell"].shift(1)

    return df

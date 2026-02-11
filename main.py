from datetime import datetime

from data_loader import load_data
from execution_engine import run_backtest
from reporting import report
from _logic import build_signals


SYMBOL = "MARA"
START  = "2015-01-01"
END    = datetime.now().strftime('%Y-%m-%d')


def main():

    print("[DATA] Loading symbol...")
    df = load_data(SYMBOL, START, END)

    print("[ENGINE] Building strategy signals...")

    settings = {
        "delayOffset":0,
        "basisType":"ALMA",
        "basisLen":2,
        "offsetSigma":5,
        "offsetALMA":0.85,
        "useRes":True,
        "stratRes":120
    }

    df = build_signals(df, settings)

    print("[BACKTEST] Running engine...")
    df, trades, returns = run_backtest(df)

    print("[BENCHMARK] Loading SPY...")
    bench = load_data("SPY", START, END)
    bench_ret = bench['Close'].pct_change().dropna()

    print("[REPORT] Generating report...")
    report("strategy", returns, bench_ret, trades)

    print("✅ DONE — check /reports folder")


if __name__ == "__main__":
    main()

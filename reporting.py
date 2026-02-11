import os
import pandas as pd
import quantstats as qs

def report(name,returns,benchmark,trades):

    os.makedirs("reports",exist_ok=True)

    qs.reports.html(
        returns,
        benchmark=benchmark,
        output=f"reports/{name}.html",
        title=name
    )

    pd.DataFrame(
        trades,
        columns=["Side","Date","Price"]
    ).to_csv(
        f"reports/{name}_trades.csv",
        index=False
    )

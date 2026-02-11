* * *

🧠 ENGINE\_STRUCTURE.md
=======================

```md
# 🧱 Python Pine Backtest Engine — Structure Guide

This engine is designed to recreate TradingView Pine strategies in Python
with:

- non-repainting execution
- next-bar open fills
- MTF (multi-timeframe) logic
- parquet caching
- HTML performance reporting
- CSV trade export

This document explains what each file does and how to reuse the framework
for new strategies.

---

# 📁 PROJECT STRUCTURE

```

project/  
│  
├── main.py  
├── data\_loader.py  
├── execution\_engine.py  
├── reporting.py  
├── mtf.py  
├── indicators.py  
├── saiyan\_logic.py (or strategy\_logic.py)  
│  
├── data\_cache/  
├── reports/

```

---

# 🚀 EXECUTION FLOW

```

main.py  
↓  
load\_data()  
↓  
build\_strategy\_signals()  
↓  
run\_backtest()  
↓  
report()

```

Strategy logic NEVER goes into execution_engine.py.

---

# 📄 FILE BREAKDOWN

---

## main.py
### Role
Main pipeline controller.

### Responsibilities
- load market data
- call strategy logic
- run backtest engine
- generate reports

### NEVER PUT:
- indicator math
- trade execution rules
- Pine logic

---

## data_loader.py
### Role
Market data ingestion + caching.

### Features
- yfinance download
- parquet caching
- column normalization

### Output
```

Open  
High  
Low  
Close  
Volume

```

### Reuse Tip
Works for any ticker or timeframe.

---

## execution_engine.py
### Role
Simulates Pine strategy execution.

### Implements
- next bar open fills
- slippage model
- reversal handling
- position sizing
- equity curve

### NEVER MODIFY FOR NEW STRATEGIES
Signals only come from strategy file.

Required Columns:
```

long\_signal  
short\_signal

```

---

## reporting.py
### Role
Performance output.

### Generates
- QuantStats HTML report
- CSV trade log

Output Folder:
```

/reports

```

---

## mtf.py
### Role
TradingView `request.security()` emulation.

### Functions
- resample_tf()
- security()

Handles:
- higher timeframe aggregation
- lower timeframe alignment
- forward filling

Used only when strategy requires MTF logic.

---

## indicators.py
### Role
Reusable Pine indicator recreations.

Examples:
- ALMA
- Hull MA
- TEMA
- Heikin Ashi

### Strategy files call functions from here.

---

## strategy_logic.py (example: saiyan_logic.py)
### Role
THE ONLY FILE THAT CHANGES BETWEEN STRATEGIES.

Contains:
- indicator calculations
- Pine signal logic
- crossover conditions
- repaint offsets

Must output:
```

df\["long\_signal"\]  
df\["short\_signal"\]

```

Execution engine reads ONLY these.

---

# 🔄 SIGNAL FLOW

```

Indicators → Strategy Logic → Signals  
Signals → Execution Engine → Trades  
Trades → Reporting → HTML + CSV

```

---

# 🧪 HOW TO PORT A NEW PINE STRATEGY

1. Copy project template
2. Rename:
```

saiyan\_logic.py → new\_strategy\_logic.py

```
3. Recreate Pine indicators in:
```

indicators.py

```
4. Implement signals in:
```

build\_strategy\_signals()

```
5. Output:
```

long\_signal  
short\_signal

```
6. Do NOT change execution_engine.py

---

# ⚠️ COMMON MISTAKES

- putting entry logic in execution_engine
- not shifting signals for non-repaint
- forgetting next-bar execution
- mixing indicator math with main.py
- breaking parquet caching

---

# ✅ ENGINE GUARANTEES

- deterministic non-repaint execution
- reproducible backtests
- TradingView-like fills
- reusable architecture
- strategy isolation

---

# 📌 FUTURE ADDITIONS

Optional modules:
- structure_engine.py
- zigzag_engine.py
- supply_demand_engine.py
- risk_engine.py
- portfolio_engine.py

---

# 🔥 TL;DR

Only change:
```

strategy\_logic.py

```

Everything else = reusable trading engine.
```

* * *

# RISE Trader - Success Criteria

This document defines the key performance indicators (KPIs) and operational metrics used to measure the success of RISE Trader Version 1.

## 1. Functional Success Metrics
* **Stock Universe Coverage**: The system must successfully process 100% of the active NIFTY 50 index constituents (all 50 tickers) during each run.
* **Indicator Calculation Accuracy**: All quantitative indicators (Volume Ratio, VWAP, ORB, Relative Strength) must be calculated successfully without errors for each constituent stock.
* **Recommendation Delivery**: The system must generate exactly 2 stock recommendations (when thresholds are met) and successfully broadcast them to the Telegram channel.
* **Telegram Notification Latency**: Telegram messages must be delivered within 30 seconds of the recommendation engine completing its calculations.
* **Traceable Rationale**: Every recommendation generated must be accompanied by its calculated confidence score and the exact set of quantitative rules that triggered the alert.

## 2. Validation & Auditing Success Metrics
* **Recommendation Persistence**: 100% of generated recommendations must be recorded in the local log/database with all relevant metadata (timestamp, symbol, indicator values, confidence score).
* **Paper Trading Completeness**: The system must provide the data fields necessary to track paper trades, including:
  * Recommended entry price.
  * Recommended exit price (based on simple time-based or rule-based exit).
  * Calculated profit/loss (P&L) for each recommendation.
* **Audit Readiness**: The generated logs must be clean and structured (e.g., CSV or structured JSON/database format) so that a third-party script or spreadsheet can import them to compute total returns, win rate, and profit factor.

## 3. Operational Success Metrics
* **Zero Real-Money Trade Leakage**: Absolutely no live capital must be traded. Under no circumstances should the system make live broker connections or place actual trades in Version 1.
* **Automation Reliability**: The scheduler or script execution must run daily without manual intervention during the test validation period (e.g., a 20-day trading trial).
* **System Failure Recovery**: In the event of network dropouts or api limit hits, the system must log the error and attempt to reconnect, maintaining a failure rate of less than 2% over the validation period.

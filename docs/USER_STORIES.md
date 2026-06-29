# RISE Trader - User Stories

This document captures the business requirements in the form of agile user stories, representing the requirements from the perspective of the developer/trader.

## Theme 1: Market Data Collection
### User Story 1: Automated Market Scanning
As a **Quantitative Trader**,  
I want the system to automatically collect intraday price and volume data for all NIFTY 50 stocks during market hours,  
so that I do not have to manually look up charts and stock prices.

### User Story 2: Index Benchmark Tracking
As a **Quantitative Analyst**,  
I want the system to fetch the real-time index level of the NIFTY 50,  
so that I can compare individual stock performance against the broader market index benchmark.

---

## Theme 2: Indicator Analysis
### User Story 3: Volume Ratio Calculation
As a **Quantitative Trader**,  
I want the system to calculate the Volume Ratio of each stock compared to its historical average at that time of day,  
so that I can identify stocks experiencing unusual institutional buying or selling pressure.

### User Story 4: VWAP Alignment
As a **Quantitative Trader**,  
I want the system to evaluate stock prices relative to their intraday Volume Weighted Average Price (VWAP),  
so that I can assess whether a stock is trading at a premium or discount compared to its average intraday value.

### User Story 5: Opening Range Breakout Detection
As a **Quantitative Trader**,  
I want the system to identify the high and low prices of the first 15–30 minutes of trading and detect breakouts,  
so that I can spot high-momentum stocks starting new intraday trends.

### User Story 6: Relative Strength Assessment
As a **Quantitative Analyst**,  
I want the system to calculate the Relative Strength of each stock against the NIFTY 50 index,  
so that I can prioritize stocks that are outperforming the general market.

---

## Theme 3: Decision Support and Scoring
### User Story 7: Rule-Based Stock Ranking
As a **Quantitative Trader**,  
I want the system to rank the NIFTY 50 stocks using objective, multi-indicator scoring rules,  
so that I can identify the strongest trading candidates based on quantitative data instead of intuition.

### User Story 8: Recommendation Explanations
As a **Paper Trader**,  
I want to see a confidence score and a detailed textual explanation of why a stock was recommended,  
so that I can understand which indicators triggered the setup and verify it against my strategies.

---

## Theme 4: Alerts and Notifications
### User Story 9: Mobile Telegram Alerts
As a **Paper Trader**,  
I want the daily top 2 stock recommendations and their explanations sent directly to my Telegram chat,  
so that I can receive actionable alerts instantly on my phone while the trading session is active.

---

## Theme 5: Verification and Performance Tracking
### User Story 10: Recommendation Logging
As a **Quantitative Analyst**,  
I want the system to write every recommendation, confidence score, and indicator state to a persistent log file or database,  
so that I can maintain an auditable record of the system's decisions.

### User Story 11: Paper Trading Evaluation
As a **Paper Trader**,  
I want to log my paper trading entry and exit points for each recommendation,  
so that I can compute the historical win rate and return on investment without risking real capital.

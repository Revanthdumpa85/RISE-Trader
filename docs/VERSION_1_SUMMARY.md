# RISE Trader - Version 1 Executive Summary

## 1. Executive Summary
RISE Trader Version 1 is a rule-based decision-support system designed to systematically scan, analyze, and rank stocks within the NIFTY 50 universe. The primary objective is to replace emotional trading decisions with a transparent, quantitative framework. Version 1 functions strictly in a paper trading mode, where recommendations are logged and delivered to the user via Telegram, but no live trading accounts are accessed and no real money is risked.

---

## 2. What Version 1 Will Deliver

### Core Components
1. **NIFTY 50 Data Scraper**: A lightweight collection mechanism that fetches intraday price and volume data for the NIFTY 50 universe during trading hours.
2. **Quantitative Analysis Engine**: A calculator that processes four core indicators:
   * **Volume Ratio**: Measures intraday volume activity relative to historical averages.
   * **VWAP Alignment**: Determines if a stock is trading above or below its intraday volume weighted average price.
   * **Opening Range Breakout (ORB)**: Monitors price breakouts above/below opening range boundaries.
   * **Relative Strength (RS)**: Measures stock performance relative to the NIFTY 50 index.
3. **Ranking & Recommendation Engine**: An algorithm that applies predefined scoring rules to select the top 2 stocks of the day, computes a confidence score, and formats a plain-English explanation.
4. **Telegram Broadcast Bot**: An automated notifier that delivers recommendations, confidence levels, and explanations to the user's mobile device.
5. **Paper Trading Log**: A persistent record of all generated recommendations to track and audit historical performance.

---

## 3. Strict Scope Boundaries for Version 1

| Feature / Capability | Version 1 Status | Explanation |
| :--- | :--- | :--- |
| **NIFTY 50 Stocks** | **IN-SCOPE** | The system scans only the 50 stocks in the NIFTY index. |
| **Volume Ratio / VWAP / ORB / RS** | **IN-SCOPE** | Predefined quantitative rules are calculated. |
| **Telegram Notifications** | **IN-SCOPE** | Results are broadcast to the user via Telegram. |
| **Performance Logging** | **IN-SCOPE** | Recommendations are written to a file for analysis. |
| **AI / Machine Learning** | **OUT-OF-SCOPE** | No predictive models, regression, or neural networks. |
| **News Sentiment Analysis** | **OUT-OF-SCOPE** | No scraping of social media, news sites, or public feeds. |
| **Broker API Integration** | **OUT-OF-SCOPE** | No credentials, order management systems, or broker connections. |
| **Automated Execution** | **OUT-OF-SCOPE** | The system does not place orders or manage open trades. |
| **Real Capital Exposure** | **OUT-OF-SCOPE** | Strictly paper trading and validation. |

---

## 4. Next Step
With the business requirements, target scope, risks, success criteria, and the [Long-Term Product Roadmap & Evolution Plan](file:///c:/Users/REVANTH/OneDrive/Desktop/RISE-Trader/docs/PRODUCT_ROADMAP.md) for RISE Trader established and approved, the project is ready to transition to the technical phase. 
Please refer to the following section: **Ready for Software Architecture**.


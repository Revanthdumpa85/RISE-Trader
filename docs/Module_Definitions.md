# RISE Trader - Module Definitions

This document defines the functional boundaries, contracts, inputs, outputs, and future extension paths for each module in the RISE Trader platform. No implementation code or concrete algorithms are described here.

---

## 1. Collector Module (`src/infrastructure/collector`)
* **Purpose**: Manages the connection, data acquisition, and ingestion of raw market data from external suppliers.
* **Responsibilities**:
  * Formulates HTTP request queries to public data providers.
  * Validates connection health and handles HTTP response streams.
  * Parses raw responses (JSON/CSV) into standardized candle and tick models.
* **Inputs**:
  * Query parameters: List of stock tickers, target resolution interval, and timeline boundary.
* **Outputs**:
  * A collection of structured historical or intraday price/volume data structures.
* **Dependencies**:
  * Depends on standard network libraries and core domain interfaces.
* **Future Extensions**:
  * Add support for streaming WebSockets for real-time tickers.
  * Add broker feed connectors (e.g., Zerodha, AngelOne) for high-precision live data (Version 7).

---

## 2. Indicators Module (`src/domain/indicators`)
* **Purpose**: Performs mathematical calculations on stock price histories to generate technical analysis metrics.
* **Responsibilities**:
  * Calculates Volume Ratio (current volume vs historical baseline).
  * Computes Volume Weighted Average Price (VWAP) across intraday candles.
  * Calculates Opening Range Breakout (ORB) boundaries (High/Low limits of opening interval).
  * Computes Relative Strength index comparison values.
* **Inputs**:
  * Data arrays containing historical price, volume, and timing info for stocks and index reference benchmarks.
* **Outputs**:
  * Enriched stock data structures containing calculated decimal values for each technical indicator.
* **Dependencies**:
  * Core domain entities. Completely decoupled from network, filesystems, and configurations.
* **Future Extensions**:
  * Incorporate classic oscillators (RSI, MACD) and momentum filters (EMA, ATR) (Version 2).
  * Add volume profile indicators and order book depth analysis models.

---

## 3. Strategy Module (`src/application/strategy`)
* **Purpose**: Evaluates indicators against rule profiles to rank stocks and generate recommendations.
* **Responsibilities**:
  * Reads rule weights and criteria from configuration parameters.
  * Scores constituent stocks by applying binary or scalar scoring criteria to active indicators.
  * Sorts and selects the top 2 stocks meeting the trade setups.
  * Calculates confidence scores based on criteria execution.
  * Formulates written explanations for selections.
* **Inputs**:
  * Collections of indicator-enriched stock structures and active scoring profiles.
* **Outputs**:
  * Selected recommendation objects containing stock tickers, confidence scores, and selection rationales.
* **Dependencies**:
  * Depends on indicator schemas and configurations.
* **Future Extensions**:
  * Integration of machine learning models for scoring ranking optimization (Version 9).
  * Implementation of dynamic stop-loss and profit-target allocation algorithms (Version 4).

---

## 4. Alerts Module (`src/infrastructure/notifier`)
* **Purpose**: Transmits recommendations and operational system alerts to external messaging networks.
* **Responsibilities**:
  * Formats raw recommendation data into human-readable text payloads.
  * Interfaces with the Telegram Bot API to dispatch messages securely.
  * Manages transmission retry mechanisms and handles network errors.
* **Inputs**:
  * Structured recommendation records and destination credentials (API keys and target channels).
* **Outputs**:
  * Network packets sent over HTTPS; returns transmission status confirmations.
* **Dependencies**:
  * Depends on core domain data contracts and configuration profiles.
* **Future Extensions**:
  * Support for alternative notifications like Email, Slack, Discord, or mobile push notifications.
  * Support for interactive commands (e.g., querying active watchlists via Telegram).

---

## 5. Paper Trading Module (`src/application/paper_trading`)
* **Purpose**: Simulates the execution of trades in a risk-free environment.
* **Responsibilities**:
  * Records the exact timestamp and entry price when a stock is recommended.
  * Monitors pricing data during the session to simulate entry and exit executions.
  * Logs transaction summaries (entry price, simulated exit price, P&L) to local tracking repositories.
* **Inputs**:
  * Core recommendation payloads and current live price updates.
* **Outputs**:
  * Simulated execution events containing transaction logs and metrics.
* **Dependencies**:
  * Application scoring events and storage interface boundaries.
* **Future Extensions**:
  * Dynamic slippage and commission fee modeling to align simulation with real-world execution.
  * Simulated order book filling patterns.

---

## 6. Performance Module (`src/application/paper_trading`)
* **Purpose**: Analyzes logged paper-trading logs to generate operational performance reports.
* **Responsibilities**:
  * Pulls historical simulated transaction datasets.
  * Calculates statistical metrics: Win Rate, Profit Factor, Average P&L, Max Drawdown, and Sharpe Ratio.
  * Formats performance reports for user review.
* **Inputs**:
  * Datasets containing logged transaction histories.
* **Outputs**:
  * Performance scorecards, summary tables, and diagnostic outputs.
* **Dependencies**:
  * Storage repository interfaces.
* **Future Extensions**:
  * Visualization libraries to generate historical charts and equity curves (Version 5).
  * Dynamic parameter backtesting optimization loops (Version 8).

---

## 7. Configuration Module (`src/config`)
* **Purpose**: Manages system parameters, secrets, and environment configurations.
* **Responsibilities**:
  * Loads environment files and reads settings from files (e.g. YAML, JSON).
  * Validates configuration parameters at application initialization.
  * Exposes read-only configuration interfaces to the orchestrator.
* **Inputs**:
  * External setting files (settings.yaml) and environment maps.
* **Outputs**:
  * Unified configuration settings structures.
* **Dependencies**:
  * Standard libraries and third-party configuration parsers.
* **Future Extensions**:
  * Dynamic hot-reloading of settings without restarting the execution process.
  * Cloud vault configurations (e.g. AWS Secrets Manager or HashiCorp Vault) (Version 5).

---

## 8. Utilities Module (`src/utils`)
* **Purpose**: Provides shared helper routines.
* **Responsibilities**:
  * Formats numbers and currency values.
  * Normalizes date, time, and timezone information (e.g., converting to Indian Standard Time).
  * Implements common validation utilities.
* **Inputs**:
  * Raw dates, decimals, or strings.
* **Outputs**:
  * Formatted structures or boolean validation indicators.
* **Dependencies**:
  * Zero external or application-level dependencies.
* **Future Extensions**:
  * Specialized math libraries or custom log formatters.

---

## 9. Tests Module (`tests/`)
* **Purpose**: Contains automated tests to ensure structural and behavioral correctness.
* **Responsibilities**:
  * Exercises mathematical indicators using static datasets (`tests/unit/`).
  * Simulates network requests and mock filesystems (`tests/integration/`).
  * Runs automated execution scenarios.
* **Inputs**:
  * Test data inputs, mock outputs, and runtime execution flags.
* **Outputs**:
  * Comprehensive test reports.
* **Dependencies**:
  * Depends on testing frameworks (e.g., pytest) and the main application code.
* **Future Extensions**:
  * Automated regression tests, CI/CD integrations, and backtesting pipelines.

---

## 10. Documentation Module (`docs/`)
* **Purpose**: Serves as the developer reference, listing product scope, rules, specifications, and architecture decisions.
* **Responsibilities**:
  * Documents vision, requirements, architecture patterns, folder structures, and decisions.
  * Provides updates on project roadmaps.
* **Inputs**:
  * System updates, design decisions, and requirements changes.
* **Outputs**:
  * Clean technical Markdown documents.
* **Dependencies**:
  * None.
* **Future Extensions**:
  * Auto-generated developer documentation portals (e.g., Sphinx or MkDocs).

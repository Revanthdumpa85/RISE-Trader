# RISE Trader - Project Folder Structure

This document details the production-ready directory structure for the RISE Trader project, defining the purpose, responsibilities, and future growth path for each directory.

---

## 1. Directory Tree Overview

```text
RISE-Trader/
├── .github/                   # CI/CD Workflows & Automation Templates
├── config/                    # External Application Settings & Rules
│   ├── settings.yaml          # Core Application Settings (Tuning parameters)
│   └── tickers.txt            # Stock Universe Tickers (NIFTY 50 list)
├── docs/                      # Technical Documentation & Decisions
├── src/                       # Application Source Root
│   ├── __init__.py
│   ├── main.py                # Main Application Orchestrator
│   ├── application/           # Application Use Cases & Workflows
│   │   ├── __init__.py
│   │   ├── paper_trading/     # Simulation & Performance Tracking Logic
│   │   └── strategy/          # Scoring & Ranking Systems
│   ├── config/                # Environment & YAML Configuration Loaders
│   │   └── __init__.py
│   ├── domain/                # Core Business Logic & Models (Pure Python)
│   │   ├── __init__.py
│   │   ├── interfaces/        # Ports / Abstract Base Interfaces
│   │   ├── indicators/        # Pure Math Indicator Calculations
│   │   └── models/            # Core Data Structures & Schemas
│   ├── infrastructure/        # External Implementations (Adapters)
│   │   ├── __init__.py
│   │   ├── collector/         # Web/API Scrapers (Yahoo Finance)
│   │   ├── notifier/          # Telegram & Communication Adapters
│   │   └── storage/           # Database / Local CSV Storage Adapters
│   └── utils/                 # General-Purpose Utilities
│       ├── __init__.py
│       └── helpers.py         # Timestamp & Math Format Helpers
├── tests/                     # Test Suite Root
│   ├── __init__.py
│   ├── integration/           # Adapter & API Mock Tests
│   └── unit/                  # Domain & Indicator Logic Tests
├── requirements.txt           # Package Dependencies
└── README.md                  # Project Main Readme
```

---

## 2. Directory Details

### `config/`
* **Purpose**: Houses configuration, parameter settings, and static reference tables.
* **Responsibilities**: Stores tickers (e.g., NIFTY 50) and parameter settings (e.g., indicator thresholds, execution intervals) in a non-code format.
* **Future Growth**: Can house separate YAML profiles for testing, staging, and production environments, as well as database migration configurations.

### `docs/`
* **Purpose**: Serves as the central repository for technical design, business logic, decision logs, and roadmaps.
* **Responsibilities**: Maintains readable markdown documentation describing the architecture and business requirements.
* **Future Growth**: Will grow to include API schema documentations, backtesting reports, user deployment guidelines, and security policies.

### `src/`
* **Purpose**: The package root directory containing all executable code.
* **Responsibilities**: Houses the application launcher (`main.py`) and standard sub-packages.
* **Future Growth**: Structured to remain clean; the sub-packages are separated by layers to isolate changes.

### `src/domain/`
* **Purpose**: The heart of Clean Architecture. Contains pure core models and domain logic.
* **Responsibilities**:
  * Defines core schemas (`src/domain/models/`) like candles and ticks.
  * Calculates technical indicators (`src/domain/indicators/`) using mathematical algorithms.
  * Lists communication boundaries (`src/domain/interfaces/`) to achieve Dependency Inversion.
* **Future Growth**: Adding new indicators (RSI, MACD, EMA) involves adding files only inside the `domain/indicators/` subfolder.

### `src/application/`
* **Purpose**: Coordinates domain actions to solve business problems (Use Cases).
* **Responsibilities**:
  * Runs the strategy engine (`src/application/strategy/`) that scores and ranks stocks.
  * Audits paper-trading logs (`src/application/paper_trading/`) to compute performance metrics.
* **Future Growth**: When portfolio management, position sizing, or risk management are added (Version 4), they will live inside new subfolders in this directory.

### `src/infrastructure/`
* **Purpose**: Implements external communication adaptors (I/O operations).
* **Responsibilities**:
  * Scrapes stock datasets from Yahoo Finance (`src/infrastructure/collector/`).
  * Delivers alerts via Telegram APIs (`src/infrastructure/notifier/`).
  * Writes files or saves to disk (`src/infrastructure/storage/`).
* **Future Growth**: If Yahoo Finance is replaced with a direct broker feed (Version 7), a new collector file is added here without touching the `domain` or `application` logic. Swapping CSV files for a PostgreSQL database (Version 5) only changes code in `infrastructure/storage/`.

### `src/utils/`
* **Purpose**: Holds shared, domain-agnostic helpers.
* **Responsibilities**: Handles generic conversions (dates, strings) and mathematical formatting.
* **Future Growth**: Contains utility files for specialized math, logging formatters, or time-zone converters.

### `tests/`
* **Purpose**: Holds the automated verification suite.
* **Responsibilities**:
  * `tests/unit/` tests mathematical correctness of indicators.
  * `tests/integration/` tests network handlers and file writes using mocks.
* **Future Growth**: Will include automated performance tests, API contract tests, and machine learning model validation tests (Version 9).

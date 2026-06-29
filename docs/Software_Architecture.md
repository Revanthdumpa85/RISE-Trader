# RISE Trader - Software Architecture Specification

This document details the architectural blueprints, structural design, and operational strategies for the RISE Trader platform. It serves as the official reference for all development activities.

---

## 1. Architecture Principles

To meet the core business objectives and accommodate the 10-stage evolution roadmap, the architecture is built on the following pillars:

* **Clean Architecture**: High-level business rules (indicators and strategies) are placed at the center, completely separated from external interfaces, databases, notification systems, and APIs.
* **SOLID Principles**:
  * *Single Responsibility Principle (SRP)*: Each module does one logical job (e.g., indicator calculations, alerts, or data harvesting).
  * *Open/Closed Principle (OCP)*: Features are added by extending the codebase (e.g., new indicators) rather than altering existing orchestration logic.
  * *Liskov Substitution Principle (LSP)*: Adapters implementing the same interface can be used interchangeably.
  * *Interface Segregation Principle (ISP)*: Large interfaces are split into small, client-specific ones.
  * *Dependency Inversion Principle (DIP)*: Core modules depend on abstract interfaces, not concrete implementations.
* **Low Coupling & High Cohesion**: Minimize dependencies between modules while ensuring that elements inside a module are highly focused on a single topic.
* **Separation of Concerns**: Strict boundaries between raw data gathering, analytical computations, selection decision-making, alert delivery, and file persistence.
* **Configuration-Driven Design**: The runtime environment, scoring rules, indicator thresholds, and notification settings are controlled externally by configuration files rather than hardcoded variables.

---

## 2. High-Level Architecture
RISE Trader employs an **Hexagonal (Ports and Adapters)** architecture model. This decouples the core domain models and application logic from external systems like third-party APIs (Yahoo Finance, Telegram) and storage layers (local files).

```
   ┌──────────────────────────────────────────────────────────┐
   │                  INFRASTRUCTURE ADAPTERS                 │
   │                                                          │
   │   ┌──────────────────┐            ┌──────────────────┐   │
   │   │  Yahoo Finance   │            │   Telegram Bot   │   │
   │   │   (Data Feed)    │            │    (Alerts)      │   │
   │   └────────┬─────────┘            └────────▲─────────┘   │
   │            │                               │             │
   └────────────┼───────────────────────────────┼─────────────┘
                │ Data Port                     │ Notifier Port
   ┌────────────▼───────────────────────────────┴─────────────┐
   │                                                          │
   │                   APPLICATION CORE                       │
   │                                                          │
   │   ┌──────────────────────────────────────────────────┐   │
   │   │                    USE CASES                     │   │
   │   │  • Orchestrate Scrape   • Rank and Score Stocks  │   │
   │   │  • Compute Indicators   • Log Recommendations    │   │
   │   └────────────────────────┬─────────────────────────┘   │
   │                            │                             │
   │   ┌────────────────────────▼─────────────────────────┐   │
   │   │                  DOMAIN MODELS                   │   │
   │   │  • Stock   • Candle   • Rule   • Recommendation  │   │
   │   └──────────────────────────────────────────────────┘   │
   │                                                          │
   └────────────────────────────┬─────────────────────────────┘
                                │ Storage Port
   ┌────────────────────────────▼─────────────────────────────┐
   │                  INFRASTRUCTURE ADAPTERS                 │
   │                                                          │
   │                   ┌──────────────────┐                   │
   │                   │  CSV / DB File   │                   │
   │                   │  (Performance)   │                   │
   │                   └──────────────────┘                   │
   └──────────────────────────────────────────────────────────┘
```

---

## 3. Layered Architecture

The application is structured into four distinct logical layers:

1. **Domain Layer (Core)**:
   * Contains core entities (Stock, Candle, AlertPayload, Recommendation).
   * Contains mathematical indicator logic (without files or network calls).
   * Defines abstract interface ports (IDataProvider, INotifier, IStorageRepository).
2. **Application Layer (Use Cases)**:
   * Directs the operational flow: fetches data, calculates indicators, ranks results, triggers notifications, and writes records.
   * Houses the ranking algorithm and rule configurations.
3. **Infrastructure Layer (Adapters)**:
   * Concrete implementations of abstract ports.
   * Yahoo Finance Adapter (fetches candles over HTTP).
   * Telegram Adapter (sends notifications over HTTPS).
   * Local Storage Adapter (handles CSV or DB file writes).
4. **Configuration & Entry Layer**:
   * CLI entry points, runners, and configuration managers (YAML/Environment files).

---

## 4. Data Flow Diagram (ASCII)

The flow of data through the system is linear and unidirectional:

```
[External Market]
       │
       ▼ (HTTP GET / JSON Data)
┌──────────────┐
│  Collector   │ (Infrastructure Adapter)
└──────┬───────┘
       │ (Domain Models: List of Candles/Ticks)
       ▼
┌──────────────┐
│  Indicators  │ (Domain Layer calculations)
└──────┬───────┘
       │ (Enriched Stocks with calculated Indicator values)
       ▼
┌──────────────┐
│   Strategy   │ (Application Layer / Ranking Engine)
└──────┬───────┘
       │ (Recommendation object with Scores and Explanations)
       ▼
 ┌─────┴────────────────────────┐
 │                              │
 ▼                              ▼
┌──────────────┐         ┌──────────────┐
│  Alerts Port │         │ Storage Port │
└──────┬───────┘         └──────┬───────┘
       │ (JSON payload)         │ (Structured CSV/DB Record)
       ▼                        ▼
┌──────────────┐         ┌──────────────┐
│ Telegram Bot │         │ Log / DB     │
└──────────────┘         └──────────────┘
```

---

## 5. Module Interaction Diagram

The orchestrator manages the lifecycle of the execution loop:

```
┌────────────┐     ┌───────────┐    ┌────────────┐    ┌──────────┐    ┌─────────┐    ┌─────────┐
│ Orchestrator│     │ Collector │    │ Indicators │    │ Strategy │    │ Notifier│    │ Storage │
└─────┬──────┘     └─────┬─────┘    └─────┬──────┘    └────┬─────┘    └────┬────┘    └────┬────┘
      │                  │                │                │               │              │
      │ 1. FetchData()   │                │                │               │              │
      ├─────────────────>│                │                │               │              │
      │                  │                │                │               │              │
      │ <─ ─ ─ ─ ─ ─ ─ ─ │                │                │               │              │
      │ (List of Candles)│                │                │               │              │
      │                  │                │                │               │              │
      │ 2. Compute()     │                │                │               │              │
      ├──────────────────────────────────>│                │               │              │
      │                  │                │                │               │              │
      │ <─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                │               │              │
      │ (Calculated Metrics)              │                │               │              │
      │                  │                │                │               │              │
      │ 3. Evaluate()    │                │                │               │              │
      ├───────────────────────────────────────────────────>│               │              │
      │                  │                │                │               │              │
      │ <─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤               │              │
      │ (Top 2 Recommendations + Score)                    │               │              │
      │                  │                │                │               │              │
      │ 4. SendAlert()   │                │                │               │              │
      ├───────────────────────────────────────────────────────────────────>│              │
      │                  │                │                │               │              │
      │ 5. Save()        │                │                │               │              │
      ├──────────────────────────────────────────────────────────────────────────────────>│
```

---

## 6. Dependency Flow

Dependencies point strictly inward to prevent infrastructural changes from leaking into the business domain.

* **Infrastructure Layer** depends on **Application Layer** and **Domain Layer** (for schemas and interfaces).
* **Application Layer** depends on **Domain Layer**.
* **Domain Layer** has zero external dependencies (purely Python standard library logic where possible).

---

## 7. Package Responsibilities

* **`src.domain`**: Houses math models, data structures, and boundary interfaces.
* **`src.application`**: Processes scoring rules and sequences the scraping-ranking-reporting workflows.
* **`src.infrastructure`**: Implements communication and data-storage mechanisms.
* **`src.config`**: Handles file reading and validation of active execution parameters.

---

## 8. Error Handling Strategy

RISE Trader implements a structured, multi-tier exception hierarchy to prevent crashes and ensure diagnostic clarity:

* **Custom Core Exceptions**: Define a set of base exceptions (e.g., `DataProviderError`, `CalculationError`, `NotificationError`, `StorageError`).
* **Boundary Catching**:
  * **Collector Boundary**: Catch network issues, parse errors, or rate limits. Recover by falling back to cached datasets or logging and skipping the execution run.
  * **Calculation Boundary**: Catch divide-by-zero errors or missing metrics. Return NaN values rather than crashing the system.
  * **Alert Boundary**: Log alert failures to the database, allowing critical notification attempts to be queued or flagged for review.

---

## 9. Logging Strategy

Logging serves as the central audit trail for the paper-trading system.

* **Log Categorization**:
  * **Standard System Logs**: System health, operational milestones, and standard error stacks (categorized into `DEBUG`, `INFO`, `WARNING`, `ERROR`).
  * **Recommendation Audits**: A separate, immutable log capture detailing the exact numerical values of indicators at the moment of recommendation.
* **Targets**: Write standard logs to daily rotating text files and print to stdout during local execution.

---

## 10. Configuration Strategy

System behavior is driven by external variables, preventing hardcoded logic leaks:

* **Secret Environment Variables**: Store passwords, Telegram API keys, and channel IDs in environment variables or `.env` files (excluded from version control).
* **Application Settings**: Store stock lists (NIFTY 50), indicators parameters (ORB window size, VWAP time spans), and scoring thresholds in structured configuration files (e.g., JSON or YAML).

---

## 11. Scalability Strategy

To scale from Version 1 (NIFTY 50) to subsequent iterations with larger universes and real-time streams:

* **Batch Collection**: The data collector interface is designed to support batch querying, reducing HTTP overhead.
* **Decoupled Workflows**: Scraped data is loaded into memory or a structured cache, allowing calculators to run asynchronously from data collectors.
* **Thread-Safe Calculations**: Calculators are designed as pure, stateless functions, allowing calculations to scale horizontally across multi-core processors.

---

## 12. Extensibility Strategy

* **Adding New Indicators (Version 2+)**: Create a new class implementing a standard `IIndicator` interface. The Orchestrator registers indicators dynamically, applying calculations without changing runner logic.
* **Adding News Sentiment (Version 3+)**: Implement a news scraper adapter conforming to an `INewsProvider` port and feed the text payload to the scoring use-case.
* **Upgrading Storage (Version 5+)**: Swap the basic CSV writer for a relational database adapter by implementing the `IStorageRepository` port.

---

## 13. Security Considerations

* **Credential Management**: No API tokens, keys, or passwords may be stored in source code. Credentials must be read at runtime from the system environment.
* **Input Validation**: All incoming data from data scrapers must be sanitized and verified for correct data types before being passed to calculation engines.
* **Sandbox Environment**: Limit file write paths to specified workspace folders to avoid arbitrary file system manipulation.

---

## 14. Testing Strategy

The architecture maximizes test coverage through structural isolation:

* **Unit Testing (Domain & Calculators)**: Test 100% of mathematical indicator routines using static mock data arrays. Since these routines are pure functions, tests require no database or network access.
* **Integration Testing (Infrastructure)**: Test adapters (Telegram, Yahoo Finance) using mocked requests and simulated response payloads to isolate tests from third-party server downtimes.
* **System End-to-End Tests**: Run mock execution loops where data collection, indicator processing, scoring, and output logging are executed sequentially using local test files.

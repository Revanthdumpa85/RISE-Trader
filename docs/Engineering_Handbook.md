# RISE Trader - Engineering Handbook

This document serves as the official Engineering Handbook for the RISE Trader project. It outlines the coding, testing, logging, error handling, documentation, security, and version control standards that every developer and AI assistant must follow.

---

## 1. Project Philosophy

* **Documentation First**: Requirements, design specifications, and API documentation must be written and approved before any software code is implemented.
* **Architecture First**: Code changes must conform strictly to the established Clean/Hexagonal layered architecture. Do not skip architectural boundaries for convenience.
* **Modular Development**: Keep components isolated, decoupling the data collectors, quantitative indicators, ranking strategy, loggers, and alert engines.
* **Single Responsibility Principle (SRP)**: Each file, class, and function must have exactly one reason to change.
* **Incremental Development**: Build features in small, testable, and version-controlled steps. Validate each version through comprehensive automated checks.
* **Data-Driven Decisions**: Refine indicators and scoring parameters based on statistical backtesting and paper-trading performance logs rather than intuition.
* **Testing First Mindset**: Design code with testability in mind. Prioritize pure mathematical functions and mock-driven integration points.
* **Readable Code Over Clever Code**: Write clean, self-explanatory, and simple code. Avoid micro-optimizations or complex syntactical tricks that reduce clarity.
* **Maintainability Over Shortcuts**: Do not introduce technical debt or tightly coupled modules to achieve quick fixes.

---

## 2. Python Coding Standards

To ensure consistency across the codebase, developers must adhere to the PEP 8 style guide and the following rules:

### Naming Conventions
* **Packages & Modules**: Lowercase with underscores (e.g., `src.domain.indicators`, `tests.unit`).
* **Files**: Lowercase with underscores (e.g., `yahoo_collector.py`, `vwap_calculator.py`).
* **Classes**: PascalCase (e.g., `YahooCollector`, `VolumeRatioCalculator`).
* **Functions & Methods**: Lowercase with underscores (e.g., `calculate_metrics()`, `send_notification()`).
* **Variables**: Lowercase with underscores (e.g., `ticker_list`, `average_volume`).
* **Constants**: Uppercase with underscores (e.g., `DEFAULT_ORB_MINUTES`, `TELEGRAM_API_URL`).
* **Enums**: PascalCase for name, UPPERCASE for values.
* **Private Methods/Attributes**: Prefix with a single underscore (e.g., `_fetch_raw_payload()`).
* **Public Methods/Attributes**: No leading underscores.

### Module Organization & Import Ordering
1. Standard library imports (e.g., `os`, `sys`, `typing`).
2. Related third-party imports (e.g., `pandas`, `requests`).
3. Local application/library specific imports (e.g., `src.domain.models`).
* *Note: Group imports logically with single blank lines separating each category. Avoid wildcard imports (`from module import *`).*

### Size Constraints
* **Maximum File Length**: Recommend keeping files under 400 lines of code. If a file exceeds this limit, consider refactoring or decomposing into smaller submodules.
* **Maximum Function Size**: Recommend keeping functions under 50 lines of code. If a function is longer, split it into smaller helper functions.

---

## 3. Documentation Standards

All modules, classes, and public functions must document their interfaces using **Google Style Docstrings**.

```python
def calculate_vwap(candles: List[Candle]) -> float:
    """Calculates the Volume Weighted Average Price (VWAP) for a list of candles.

    Args:
        candles: A list of Candle objects containing price and volume data.

    Returns:
        The calculated volume-weighted average price as a float.

    Raises:
        ValueError: If the candles list is empty or total volume is zero.
    """
    pass
```

* **Module Documentation**: Place a high-level summary at the very beginning of the file, describing its purpose, responsibilities, and external dependencies.
* **Class Documentation**: Describe the class's role, state variables, and general usage patterns.
* **Type Hints**: Explicit type signatures (using the `typing` module) must be declared on all function inputs and outputs.

---

## 4. Logging Standards

Logging provides the diagnostic data required to monitor system health and audit trading performance.

### Log Levels
* **DEBUG**: Diagnostic details for development troubleshooting (e.g., raw API responses, connection setup data).
* **INFO**: Standard operational updates (e.g., starting execution run, recommendation completed, alert sent successfully).
* **WARNING**: Unexpected events that do not halt execution (e.g., minor data gaps, API timeouts with successful retries).
* **ERROR**: Execution errors that prevent a component from completing its task (e.g., failed to fetch data for a specific stock, database write failure).
* **CRITICAL**: Fatal system crashes requiring immediate attention (e.g., Telegram API configuration missing, out of memory).

### Logging Rules
* **Format**: All logs must include `Timestamp (ISO 8601)`, `Log Level`, `Module Name`, and the `Log Message`.
* **When to Log**: Log key transition boundaries (scraping start, indicators complete, alert triggered).
* **What NOT to Log**: **NEVER** log API keys, database passwords, Telegram bot tokens, or personal identifiers in log files.

---

## 5. Error Handling Standards

* **No Silent Ignorance**: Never write empty `except` blocks. If an exception must be caught, log it as an error or warning with explanation.
* **Meaningful Exceptions**: Catch low-level exceptions (e.g., HTTP connection errors) and raise custom, context-rich exceptions (e.g., `DataProviderConnectionError`) from layer boundaries.
* **Custom Exceptions**: Define custom exception structures in a unified exceptions module under domain layers.
* **Retry Strategy**: Network operations must incorporate retry logic using exponential backoff (e.g., retrying up to 3 times with a delay of 2, 4, and 8 seconds).
* **Graceful Degradation**: If a single ticker fails to load or calculate, log the error, record its state as invalid, and proceed with the remaining 49 stocks.

---

## 6. Configuration Standards

* **Environment Variables**: Store sensitive keys, credentials, and environmental variables in a `.env` file at the root directory (never committed to Git).
* **Configuration Files**: Store non-sensitive configuration parameters (such as the ticker watchlist, indicator windows, and scoring weights) in structured settings files (e.g., YAML or JSON).
* **Secrets Management**: Read keys at runtime from environment maps.
* **No Magic Numbers**: Numbers representing settings (like ORB size, time durations, or multiplier ratios) must be defined as named configurations or constants.
* **Feature Flags**: For future upgrades, structure the configurations to support boolean flags (e.g., enabling or disabling Telegram notification alerts).

---

## 7. Testing Standards

The testing strategy is designed to verify system correctness without relying on external APIs.

* **Unit Tests**:
  * Mandatory for all domain logic and mathematical calculations (e.g., indicator formulas).
  * Must be 100% deterministic and require no network or database connections.
  * Use static arrays of candles to verify math edges (such as division by zero).
* **Integration Tests**:
  * Target external adapters (data collectors, notifiers, loggers).
  * Use mocking frameworks to simulate API responses (e.g., mocking requests response code `200` vs `500`).
* **Mocking Guidelines**: Mock network I/O, file writes, and database operations. Never make real calls to Yahoo Finance or Telegram APIs during a test suite run.

---

## 8. Git Standards

* **Branch Naming**:
  * Features: `feature/short-description` (e.g., `feature/orb-calculator`)
  * Bug fixes: `bugfix/short-description` (e.g., `bugfix/vwap-rounding`)
  * Documentation: `docs/short-description`
* **Commit Message Format**:
  * Use concise, imperative commit titles (e.g., `Add relative strength indicator calculator`).
  * Separate title from body with a blank line when describing complex logic.
* **Pull Request Checklist**:
  * Code runs locally without errors.
  * Unit and integration test suites pass 100%.
  * Code passes PEP 8 standard lint checks.
  * New features are accompanied by corresponding tests and docstrings.
* **Version Tagging**: Use semantic version tags (e.g., `v1.0.0`) for formal releases aligned with roadmap objectives.

---

## 9. Folder Responsibilities

* **`config/`**: External configurations, tickers list, and parameter adjustments.
* **`docs/`**: Architecture diagrams, roadmap, user stories, and handbook.
* **`src/domain/`**: Mathematical indicator calculations, data classes (Models), and port interfaces. Strictly code-only and decoupled from I/O.
* **`src/application/`**: Use cases including the ranking algorithm, scoring logic, and simulated paper-trading tracking logs.
* **`src/infrastructure/`**: API scrapers, Telegram communication handlers, and file log writers.
* **`src/utils/`**: General-purpose helpers (e.g., date formats, timezone conversions).
* **`tests/`**: Suite of unit and integration test fixtures.

---

## 10. LLM Development Standards

All Large Language Models (LLMs) and AI coding assistants must adhere to the following rules when modifying this codebase:

1. **Understand Before Modifying**: Analyze the [Software Architecture Specification](file:///c:/Users/REVANTH/OneDrive/Desktop/RISE-Trader/docs/Software_Architecture.md) and [Folder Structure](file:///c:/Users/REVANTH/OneDrive/Desktop/RISE-Trader/docs/Folder_Structure.md) before suggesting changes.
2. **Never Violate Layer Boundaries**: Do not import infrastructure models (like requests or file writes) directly into domain calculators.
3. **No Duplicate Logic**: Scan existing utility files and helpers before generating redundant functions.
4. **Preserve Backward Compatibility**: Ensure that new features or modifications do not break existing interfaces, schemas, or tests.
5. **Clean Code Generation**: Generated code must include type hints, Google-style docstrings, and complete error handling blocks. Never output placeholders or `TODO` comments in target files.
6. **No Scope Creep**: Do not generate, import, or describe features defined as out-of-scope for the active project version.
7. **Isolate Changes**: Modify only the files directly related to the active task. Do not rewrite surrounding files unless explicitly requested.

---

## 11. Performance Standards

* **Memory Usage**: Load data in batches. Avoid caching entire historical datasets in memory unless required by the active indicator scope.
* **CPU Efficiency**: Vectorize mathematical operations (e.g., using mathematical standard routines) to ensure processing of 50 stocks remains below 10 seconds.
* **Scalability**: Design calculations as stateless functions so they can be run in parallel processes as the stock list expands.

---

## 12. Security Standards

* **Inputs Sanitization**: Sanitize and validate all incoming data values from external data collectors before sending them to calculations.
* **Credential Isolation**: Secrets must be read at runtime. Never hardcode credentials, URLs, or personal Telegram channel IDs.
* **Dependency Auditing**: Routinely audit third-party requirements to prevent security vulnerabilities from deprecated packages.

---

## 13. Code Quality Checklist

Before any code is merged, it must satisfy:
* [ ] **Readability**: Code is clean, well-spaced, and easy to understand.
* [ ] **Maintainability**: High cohesion, low coupling, and respects Clean Architecture.
* [ ] **Documentation**: Complete Google-style docstrings and module documentation.
* [ ] **Logging**: Structured, context-rich logs with appropriate levels.
* [ ] **Error Handling**: Custom exceptions raised; retries configured for network endpoints.
* [ ] **Testing**: Matching unit or integration tests pass successfully.
* [ ] **Type Hints**: Type annotations present on all function declarations.
* [ ] **PEP 8 Compliance**: Clean format check (e.g., Black/Flake8 compliant).
* [ ] **No Dead Code**: Unused imports, variables, and functions are removed.
* [ ] **No Duplicate Logic**: No copy-pasted blocks or redundant math equations.

---

## 14. Future Contributors Guide

Welcome to the RISE Trader project! Before writing your first line of code, please complete the following steps:

1. **Read the Docs**: Read [Product Vision](file:///c:/Users/REVANTH/OneDrive/Desktop/RISE-Trader/docs/PRODUCT_VISION.md), [Business Requirements](file:///c:/Users/REVANTH/OneDrive/Desktop/RISE-Trader/docs/BUSINESS_REQUIREMENTS.md), and [Software Architecture](file:///c:/Users/REVANTH/OneDrive/Desktop/RISE-Trader/docs/Software_Architecture.md).
2. **Understand the Architecture**: Review the Hexagonal pattern. Recognize that core business logic resides in `src/domain/` and cannot communicate directly with databases, config files, or external endpoints.
3. **Follow the Handbook**: Write code that conforms to the naming, logging, testing, and documentation guidelines outlined in this handbook.
4. **Submit Clean PRs**: Ensure all test suites pass locally before submitting pull requests.

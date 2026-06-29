# RISE Trader

RISE Trader is a rule-based stock recommendation and decision-support system. It is designed to scan stock constituents, calculate objective quantitative indicators, and send notifications to assist daily trading decisions. 

The project is structured according to **Clean Architecture** and **DDD (Domain-Driven Design)** principles, separating core business computations from databases, APIs, and networking layers.

---

## 1. Directory Structure & Responsibilities

The codebase is organized into isolated layers to manage dependency direction and ensure future scalability:

```text
RISE-Trader/
├── config/                    # Non-code configuration files
│   ├── settings.yaml          # Strategy tuning and indicator windows parameters
│   └── tickers.txt            # Stock universe constituents list (NIFTY 50)
├── docs/                      # Architectural specifications and handbook documentation
├── src/                       # Main source code package
│   ├── main.py                # Main orchestrator entry point
│   ├── application/           # Coordinate domain logic (Use cases, strategy scoring, logs)
│   ├── config/                # Environment variables and YAML configuration loader
│   ├── domain/                # Core business schemas and math formulas (Zero IO dependencies)
│   ├── infrastructure/        # External systems communication adapters (Yahoo Finance, Telegram, CSV)
│   └── utils/                 # Time zone conversions, number formatters, and logging setup
└── tests/                     # Automated testing suite (Unit tests and mocked Integration tests)
```

---

## 2. Developer Setup Instructions

### Prerequisites
* Python 3.10 or higher
* Internet connection (for initial package downloads and API scraping)
* Telegram Bot API credentials (to verify live notifications)

### Step-by-Step Installation
1. **Clone the Repository**:
   Navigate to your local project directory.
2. **Create a Virtual Environment**:
   ```bash
   python -m venv .venv
   ```
3. **Activate the Virtual Environment**:
   * **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   * **Linux/macOS**:
     ```bash
     source .venv/bin/activate
     ```
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Configure Local Environment**:
   * Copy the `.env.example` template to `.env`:
     ```bash
     cp .env.example .env
     ```
   * Open the `.env` file and replace the placeholders with your actual Telegram Bot Token and Chat/Channel ID.

---

## 3. Running the Project

### Verifying Project Startup
To run the project initialization checks and ensure that configurations, directories, and standard logging are correctly loaded, run:
```bash
python -m src.main
```

### Running the Test Suite
We use `pytest` for automated test suites. To execute all unit and integration checks, run:
```bash
pytest
```

---

## 4. LLM & Coding Guidelines

All human contributors and LLM coding assistants must respect the following constraints:
* **Inward Dependencies**: External modules (like `requests` or `yfinance`) must **never** be imported into files under `src/domain/`.
* **Configuration-Driven**: Do not hardcode indicator lengths or score boundaries. Always read parameters from `settings.yaml` via `AppConfig`.
* **Documentation-First**: All newly created modules, classes, and public functions must include type annotations and Google-Style Docstrings.
* **No Scope Creep**: Keep files focused strictly on the active version objectives. Do not include features scheduled for later versions.

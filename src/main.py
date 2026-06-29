"""RISE Trader Orchestrator.

Main entry point of the RISE Trader system. Logs startup info and 
validates configurations. Contains no business or trading calculations.
"""

import logging
import sys
from src.config import AppConfig, ConfigurationError
from src.utils.logging_config import setup_logging


def main() -> None:
    """Orchestrates system startup, config loading, and logging checks."""
    try:
        # 1. Load active configurations
        config = AppConfig()

        # 2. Configure system logs
        setup_logging(log_dir=config.log_directory)
        logger = logging.getLogger("src.main")

        logger.info("Initializing RISE Trader Version 1.0.0")
        logger.info("Active environment: %s", config.environment)
        logger.info("Reference Benchmark Index: %s", config.index_benchmark)
        logger.info("Target timezone: %s", config.market_timezone)

        # 3. Verify configurations (simulate health check)
        logger.info("Verifying infrastructure configuration credentials...")
        
        # Accessing properties triggers configuration validation checks
        _ = config.telegram_bot_token
        _ = config.telegram_chat_id
        
        logger.info("Infrastructure connections validated successfully.")
        logger.info("RISE Trader is ready for developer implementation.")

    except ConfigurationError as err:
        print(f"CRITICAL CONFIGURATION ERROR: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"CRITICAL SYSTEM ERROR during startup: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

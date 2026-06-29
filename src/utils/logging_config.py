"""Logging Configuration Module.

Sets up rotating file logging and console logging.
Does not perform any business-level logging.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(log_dir: str = "logs", log_level: int = logging.INFO) -> None:
    """Configures system-wide logging with Console and Rotating File Handlers.

    Creates the log directory if it does not already exist.

    Args:
        log_dir: Path to the directory where log files will be saved.
        log_level: Numeric logging level (e.g., logging.INFO).
    """
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Standard layout format
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Root Logger Setup
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove any existing handlers to prevent double logging
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # 1. Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)

    # 2. Daily/Size Rotating File Handler (Max 5MB per file, keeping up to 5 backups)
    file_handler = RotatingFileHandler(
        log_path / "system.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    root_logger.addHandler(file_handler)

    # Prevent propagation to avoid duplicate console writes
    root_logger.propagate = False

    logging.info("Logging successfully initialized. Target folder: %s", log_path.resolve())

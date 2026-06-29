"""System Configuration Engine.

Manages application parameters, secret environment variables, and 
indicator scoring weights loaded from settings.yaml and local .env files.
"""

import os
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv
import yaml

# Automatically load local environment secrets at module ingestion
load_dotenv()


class ConfigurationError(Exception):
    """Raised when application configurations are missing or invalid."""
    pass


class AppConfig:
    """Manages application-wide settings and credentials."""

    def __init__(self, settings_path: str = "config/settings.yaml"):
        """Initializes the configuration loader.

        Args:
            settings_path: Local filesystem path to settings.yaml.

        Raises:
            ConfigurationError: If the settings file does not exist or is malformed.
        """
        self._settings_path = Path(settings_path)
        self._settings: Dict[str, Any] = self._load_settings_yaml()

    def _load_settings_yaml(self) -> Dict[str, Any]:
        """Loads and parses the settings.yaml file.

        Returns:
            A dictionary containing configuration parameters.

        Raises:
            ConfigurationError: If the settings file is missing or contains invalid YAML.
        """
        if not self._settings_path.exists():
            raise ConfigurationError(
                f"Configuration settings file not found at: {self._settings_path.resolve()}"
            )
        try:
            with open(self._settings_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file) or {}
        except yaml.YAMLError as exc:
            raise ConfigurationError(
                f"Failed to parse settings YAML file: {exc}"
            ) from exc

    @property
    def environment(self) -> str:
        """Gets the active application environment.

        Returns:
            A string representing the application environment (e.g., DEVELOPMENT).
        """
        return os.getenv("APP_ENV", "DEVELOPMENT")

    @property
    def telegram_bot_token(self) -> str:
        """Gets the Telegram Bot API secret token.

        Returns:
            The Telegram Bot API token.

        Raises:
            ConfigurationError: If the token is missing in a non-testing environment.
        """
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token and self.environment != "TESTING":
            raise ConfigurationError("TELEGRAM_BOT_TOKEN is not defined in environment variables.")
        return token or ""

    @property
    def telegram_chat_id(self) -> str:
        """Gets the Telegram Channel or Chat unique ID.

        Returns:
            The target Telegram chat identifier.

        Raises:
            ConfigurationError: If the chat ID is missing in a non-testing environment.
        """
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not chat_id and self.environment != "TESTING":
            raise ConfigurationError("TELEGRAM_CHAT_ID is not defined in environment variables.")
        return chat_id or ""

    @property
    def log_directory(self) -> str:
        """Gets the directory path where system logs are stored.

        Returns:
            Path string to the logs directory.
        """
        return os.getenv("LOG_DIR", "logs")

    @property
    def index_benchmark(self) -> str:
        """Gets the index ticker symbol for NIFTY 50 reference index.

        Returns:
            Benchmark index ticker string.
        """
        return self._settings.get("market", {}).get("index_benchmark", "^NSEI")

    @property
    def market_timezone(self) -> str:
        """Gets the operational market timezone.

        Returns:
            Timezone identifier string.
        """
        return self._settings.get("market", {}).get("timezone", "Asia/Kolkata")

    @property
    def indicators_config(self) -> Dict[str, Any]:
        """Gets configuration parameters for indicators.

        Returns:
            A dictionary containing indicator metrics parameters.
        """
        return self._settings.get("indicators", {})

    @property
    def strategy_config(self) -> Dict[str, Any]:
        """Gets configurations for strategy evaluation.

        Returns:
            A dictionary containing strategy rules parameters.
        """
        return self._settings.get("strategy", {})

    @property
    def storage_config(self) -> Dict[str, Any]:
        """Gets configuration settings for file persistence.

        Returns:
            A dictionary containing file storage paths and names.
        """
        return self._settings.get("storage", {})

"""Core RISE Trader Domain Exceptions.

Defines custom exception classes representing structural system and provider errors.
Contains no business logic or calculation implementations.
"""


class RISETraderError(Exception):
    """Base exception class for all RISE Trader system errors."""
    pass


class DataProviderError(RISETraderError):
    """Base exception for all errors originating from data providers."""
    pass


class InvalidTickerError(DataProviderError):
    """Raised when a requested ticker is invalid or not found."""
    pass


class DataCollectionError(DataProviderError):
    """Raised when there is a connection issue, rate limit, or retrieval failure."""
    pass

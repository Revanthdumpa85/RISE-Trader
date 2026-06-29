"""Market Data Provider Interface (Port).

Defines the core abstract interface for stock price and volume ingestion.
Enforces type annotations and returns raw clean DataFrames without calculations.
"""

import abc
from typing import Dict, List
import pandas as pd


class IDataProvider(abc.ABC):
    """Interface for stock data provider ports.

    All market data scraping adapters (e.g., Yahoo Finance) must implement
    this interface to maintain modular decoupling.
    """

    @abc.abstractmethod
    def fetch_ohlcv(self, ticker: str, period: str, interval: str) -> pd.DataFrame:
        """Fetches historical price and volume data for a single stock ticker.

        Args:
            ticker: The unique ticker symbol of the stock (e.g. TCS.NS).
            period: The target timeline lookback (e.g. 1d, 5d, 1mo).
            interval: The candle time interval resolution (e.g. 5m, 15m, 1d).

        Returns:
            A pandas DataFrame containing 'Open', 'High', 'Low', 'Close', 'Volume' columns.

        Raises:
            DataProviderError: If retrieval fails, connection drops, or ticker is invalid.
        """
        pass

    @abc.abstractmethod
    def fetch_ohlcv_batch(
        self, tickers: List[str], period: str, interval: str
    ) -> Dict[str, pd.DataFrame]:
        """Fetches historical price and volume data for a list of stock tickers in batch.

        Args:
            tickers: A list of unique stock ticker symbols.
            period: The target timeline lookback.
            interval: The candle time interval resolution.

        Returns:
            A dictionary mapping each ticker symbol to its clean pandas DataFrame.

        Raises:
            DataProviderError: If batch download fails or arguments are invalid.
        """
        pass

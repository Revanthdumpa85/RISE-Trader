"""Yahoo Finance Market Data Collector Adapter.

Implements the IDataProvider port using the yfinance library.
Responsible strictly for fetching and formatting price-volume data.
Does not perform any indicator calculations, scoring, or paper-trading.
"""

import logging
from typing import Dict, List, Set
import pandas as pd
import yfinance as yf
from src.domain.exceptions import DataCollectionError, InvalidTickerError
from src.domain.interfaces.data_provider import IDataProvider

logger = logging.getLogger(__name__)


class YahooDataProvider(IDataProvider):
    """Yahoo Finance concrete data provider.

    Validates parameters, downloads datasets, and returns clean DataFrames
    containing standard Open, High, Low, Close, Volume columns.
    """

    # Allowed intervals and periods defined by Yahoo Finance API specifications
    SUPPORTED_PERIODS: Set[str] = {
        "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
    }
    SUPPORTED_INTERVALS: Set[str] = {
        "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
    }

    def _validate_inputs(self, tickers: List[str], period: str, interval: str) -> None:
        """Verifies ticker lists and period/interval constraints.

        Args:
            tickers: A list of stock ticker symbols.
            period: The target timeline lookback.
            interval: The candle time interval resolution.

        Raises:
            ValueError: If tickers are empty or parameter inputs are unsupported.
        """
        if not tickers:
            raise ValueError("Ticker list cannot be empty.")
        if period not in self.SUPPORTED_PERIODS:
            raise ValueError(
                f"Unsupported period '{period}'. Allowed values: {self.SUPPORTED_PERIODS}"
            )
        if interval not in self.SUPPORTED_INTERVALS:
            raise ValueError(
                f"Unsupported interval '{interval}'. Allowed values: {self.SUPPORTED_INTERVALS}"
            )

    def fetch_ohlcv(self, ticker: str, period: str, interval: str) -> pd.DataFrame:
        """Fetches OHLCV data for a single stock ticker from Yahoo Finance.

        Args:
            ticker: The unique ticker symbol of the stock.
            period: The target timeline lookback.
            interval: The candle time interval resolution.

        Returns:
            A clean pandas DataFrame containing standard price-volume columns.

        Raises:
            InvalidTickerError: If the ticker is invalid or returns no data.
            DataCollectionError: If connection fails or columns are missing.
        """
        self._validate_inputs([ticker], period, interval)
        logger.info(
            "Fetching single ticker '%s' (Period: %s, Interval: %s) from Yahoo Finance",
            ticker,
            period,
            interval,
        )

        try:
            ticker_obj = yf.Ticker(ticker)
            df = ticker_obj.history(period=period, interval=interval, keep_metadata=False)

            if df.empty:
                logger.warning("No candles returned for ticker: %s", ticker)
                raise InvalidTickerError(f"No data returned for ticker '{ticker}'.")

            # Clean and keep standard columns only
            required_cols = ["Open", "High", "Low", "Close", "Volume"]
            if not all(col in df.columns for col in required_cols):
                raise DataCollectionError(
                    f"Missing expected OHLCV columns in Yahoo response for '{ticker}'."
                )

            return df[required_cols]

        except InvalidTickerError:
            raise
        except Exception as exc:
            logger.error("Failed to fetch market data for ticker %s: %s", ticker, exc)
            raise DataCollectionError(
                f"Failed to fetch market data for '{ticker}': {exc}"
            ) from exc

    def fetch_ohlcv_batch(
        self, tickers: List[str], period: str, interval: str
    ) -> Dict[str, pd.DataFrame]:
        """Downloads OHLCV data for multiple stock tickers in a single batch query.

        Args:
            tickers: A list of unique stock ticker symbols.
            period: The target timeline lookback.
            interval: The candle time interval resolution.

        Returns:
            A dictionary mapping ticker symbols to their clean dataframes.

        Raises:
            DataCollectionError: If the batch download fails entirely.
        """
        self._validate_inputs(tickers, period, interval)
        logger.info(
            "Downloading batch data for %d tickers (Period: %s, Interval: %s)",
            len(tickers),
            period,
            interval,
        )

        result_dict: Dict[str, pd.DataFrame] = {}
        try:
            df = yf.download(
                tickers=tickers,
                period=period,
                interval=interval,
                group_by="ticker",
                auto_adjust=True,
                progress=False,
            )

            if df.empty:
                raise DataCollectionError("Batch download returned an empty DataFrame.")

            required_cols = ["Open", "High", "Low", "Close", "Volume"]

            # If only a single ticker is queried, yfinance download returns single-level columns
            if len(tickers) == 1:
                ticker = tickers[0]
                if all(col in df.columns for col in required_cols):
                    result_dict[ticker] = df[required_cols]
                else:
                    logger.warning("Ticker %s columns missing in single-ticker batch", ticker)
                return result_dict

            # Parse multi-level columns for multi-ticker queries
            for ticker in tickers:
                if ticker in df.columns.levels[0]:
                    ticker_df = df[ticker]
                    # Filter out tickers that returned all NaNs (invalid listings)
                    if ticker_df.dropna(how="all").empty:
                        logger.warning("Ticker %s returned NaN results in batch", ticker)
                        continue

                    if all(col in ticker_df.columns for col in required_cols):
                        result_dict[ticker] = ticker_df[required_cols]
                    else:
                        logger.warning("Ticker %s columns are missing expected columns", ticker)
                else:
                    logger.warning("Ticker %s missing in downloaded levels", ticker)

            return result_dict

        except Exception as exc:
            logger.error("Failed to execute batch download: %s", exc)
            raise DataCollectionError(f"Failed to execute batch download: {exc}") from exc

"""Integration tests for the Yahoo Finance Data Provider using mocks.

Verifies input validation, mock responses, and custom exception routing.
"""

from unittest.mock import MagicMock, patch
import pandas as pd
import pytest
from src.domain.exceptions import DataCollectionError, InvalidTickerError
from src.infrastructure.collector.yahoo import YahooDataProvider


@pytest.fixture
def data_provider() -> YahooDataProvider:
    """Fixture returning an instance of the YahooDataProvider."""
    return YahooDataProvider()


@pytest.fixture
def mock_ohlcv_df() -> pd.DataFrame:
    """Fixture returning a standard OHLCV pandas DataFrame."""
    data = {
        "Open": [100.0, 101.0],
        "High": [102.0, 103.0],
        "Low": [99.0, 100.0],
        "Close": [101.5, 102.5],
        "Volume": [1000, 1500],
    }
    dates = pd.to_datetime(["2026-06-29 09:30:00", "2026-06-29 09:35:00"])
    return pd.DataFrame(data, index=dates)


def test_validate_inputs_unsupported_period(data_provider: YahooDataProvider) -> None:
    """Verifies that unsupported periods trigger ValueErrors."""
    with pytest.raises(ValueError, match="Unsupported period"):
        data_provider.fetch_ohlcv("TCS.NS", "invalid_period", "5m")


def test_validate_inputs_unsupported_interval(data_provider: YahooDataProvider) -> None:
    """Verifies that unsupported intervals trigger ValueErrors."""
    with pytest.raises(ValueError, match="Unsupported interval"):
        data_provider.fetch_ohlcv("TCS.NS", "1d", "invalid_interval")


def test_validate_inputs_empty_tickers(data_provider: YahooDataProvider) -> None:
    """Verifies that empty ticker lists trigger ValueErrors."""
    with pytest.raises(ValueError, match="Ticker list cannot be empty"):
        data_provider.fetch_ohlcv_batch([], "1d", "5m")


@patch("yfinance.Ticker")
def test_fetch_ohlcv_success(
    mock_ticker: MagicMock, data_provider: YahooDataProvider, mock_ohlcv_df: pd.DataFrame
) -> None:
    """Verifies successful single stock data downloads."""
    # Mocking Ticker().history(...)
    mock_instance = MagicMock()
    mock_instance.history.return_value = mock_ohlcv_df
    mock_ticker.return_value = mock_instance

    df = data_provider.fetch_ohlcv("RELIANCE.NS", "1d", "5m")
    
    assert not df.empty
    assert list(df.columns) == ["Open", "High", "Low", "Close", "Volume"]
    assert len(df) == 2
    mock_ticker.assert_called_once_with("RELIANCE.NS")
    mock_instance.history.assert_called_once_with(
        period="1d", interval="5m", keep_metadata=False
    )


@patch("yfinance.Ticker")
def test_fetch_ohlcv_empty_raises_invalid_ticker(
    mock_ticker: MagicMock, data_provider: YahooDataProvider
) -> None:
    """Verifies that empty response data triggers InvalidTickerError."""
    mock_instance = MagicMock()
    mock_instance.history.return_value = pd.DataFrame()  # Empty dataframe
    mock_ticker.return_value = mock_instance

    with pytest.raises(InvalidTickerError, match="No data returned"):
        data_provider.fetch_ohlcv("INVALID_TICKER", "1d", "5m")


@patch("yfinance.Ticker")
def test_fetch_ohlcv_failure_raises_collection_error(
    mock_ticker: MagicMock, data_provider: YahooDataProvider
) -> None:
    """Verifies that network issues raise DataCollectionError."""
    mock_instance = MagicMock()
    mock_instance.history.side_effect = Exception("Connection dropped")
    mock_ticker.return_value = mock_instance

    with pytest.raises(DataCollectionError, match="Failed to fetch market data"):
        data_provider.fetch_ohlcv("RELIANCE.NS", "1d", "5m")


@patch("yfinance.download")
def test_fetch_ohlcv_batch_success(
    mock_download: MagicMock, data_provider: YahooDataProvider, mock_ohlcv_df: pd.DataFrame
) -> None:
    """Verifies successful batch downloads for multiple tickers."""
    # Build multi-index columns representation for batch
    columns = pd.MultiIndex.from_product(
        [["RELIANCE.NS", "TCS.NS"], ["Open", "High", "Low", "Close", "Volume"]]
    )
    # 2 rows of dummy data for each column
    data = [
        [100, 102, 99, 101, 1000, 3000, 3050, 2990, 3020, 500],
        [101, 103, 100, 102, 1500, 3010, 3060, 3000, 3040, 600],
    ]
    dates = pd.to_datetime(["2026-06-29 09:30:00", "2026-06-29 09:35:00"])
    mock_download_df = pd.DataFrame(data, index=dates, columns=columns)
    mock_download.return_value = mock_download_df

    tickers = ["RELIANCE.NS", "TCS.NS"]
    result = data_provider.fetch_ohlcv_batch(tickers, "1d", "5m")

    assert len(result) == 2
    assert "RELIANCE.NS" in result
    assert "TCS.NS" in result
    assert list(result["RELIANCE.NS"].columns) == ["Open", "High", "Low", "Close", "Volume"]
    assert result["RELIANCE.NS"].loc[dates[0], "Close"] == 101.0
    assert result["TCS.NS"].loc[dates[1], "Close"] == 3040.0

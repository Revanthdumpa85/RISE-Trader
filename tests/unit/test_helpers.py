"""Unit tests for shared utility helper functions."""

from datetime import datetime, timezone
import pytest
from src.utils.helpers import convert_to_ist, round_decimal


def test_round_decimal() -> None:
    """Verifies that decimals are rounded to correct precisions."""
    assert round_decimal(12.3456, 2) == 12.35
    assert round_decimal(12.3412, 2) == 12.34
    assert round_decimal(12.3456, 3) == 12.346
    assert round_decimal(5.0, 1) == 5.0


def test_convert_to_ist_naive() -> None:
    """Verifies that naive UTC datetimes are localized to Indian Standard Time (IST)."""
    # 2026-06-29 12:00:00 UTC should be 2026-06-29 17:30:00 IST (+5.5 hours)
    naive_utc = datetime(2026, 6, 29, 12, 0, 0)
    ist_time = convert_to_ist(naive_utc)
    
    assert ist_time.hour == 17
    assert ist_time.minute == 30
    assert ist_time.tzinfo.zone == "Asia/Kolkata"


def test_convert_to_ist_aware() -> None:
    """Verifies that aware UTC datetimes are localized to Indian Standard Time (IST)."""
    aware_utc = datetime(2026, 6, 29, 12, 0, 0, tzinfo=timezone.utc)
    ist_time = convert_to_ist(aware_utc)
    
    assert ist_time.hour == 17
    assert ist_time.minute == 30
    assert ist_time.tzinfo.zone == "Asia/Kolkata"

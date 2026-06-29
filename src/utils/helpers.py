"""Shared Utility Helpers.

Provides helper routines for date formatting, timezone conversions, 
and mathematical precision adjustments.
"""

from datetime import datetime
import pytz


def convert_to_ist(utc_time: datetime) -> datetime:
    """Converts a UTC datetime object to Indian Standard Time (IST).

    Args:
        utc_time: A datetime object in UTC timezone.

    Returns:
        A timezone-aware datetime object localized in Asia/Kolkata timezone.
    """
    ist_timezone = pytz.timezone("Asia/Kolkata")
    if utc_time.tzinfo is None:
        # Assume UTC if naive
        utc_time = pytz.utc.localize(utc_time)
    return utc_time.astimezone(ist_timezone)


def round_decimal(value: float, precision: int = 2) -> float:
    """Rounds a floating-point number to the specified decimal precision.

    Args:
        value: The float number to round.
        precision: The number of decimal places (default is 2).

    Returns:
        The rounded floating-point number.
    """
    return round(value, precision)

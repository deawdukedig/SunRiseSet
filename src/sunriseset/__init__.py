"""
SunRiseSet Package
High-precision Solar Ephemeris & Thai Administrative Geocoding Library.
"""

from .models import Coordinates, AddressInfo, SolarResult, EnvelopeResponse
from .geocoding import reverse_geocode, forward_geocode
from .ephemeris import get_solar_times, calculate_offline_noaa
from .cache import SQLiteCache, default_cache
from .reporter import save_report, sanitize_filename
from .cli import run

__version__ = "2.0.0"
__all__ = [
    "Coordinates",
    "AddressInfo",
    "SolarResult",
    "EnvelopeResponse",
    "reverse_geocode",
    "forward_geocode",
    "get_solar_times",
    "calculate_offline_noaa",
    "SQLiteCache",
    "default_cache",
    "save_report",
    "sanitize_filename",
    "run",
]

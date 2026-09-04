import time
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from datetime import date
from sunriseset.models import Coordinates
from sunriseset.ephemeris import get_solar_times
from sunriseset.geocoding import reverse_geocode

THAI_REGIONAL_CAPITALS = [
    {"name": "Bangkok (Central)", "lat": 13.7563, "lon": 100.5018, "expected_tz": "GMT+7"},
    {"name": "Chiang Mai (North)", "lat": 18.7883, "lon": 98.9853, "expected_tz": "GMT+7"},
    {"name": "Khon Kaen (Northeast)", "lat": 16.4322, "lon": 102.8236, "expected_tz": "GMT+7"},
    {"name": "Chonburi (East)", "lat": 13.3611, "lon": 100.9847, "expected_tz": "GMT+7"},
    {"name": "Songkhla (South)", "lat": 7.1898, "lon": 100.5954, "expected_tz": "GMT+7"},
]

class TestBenchmark(unittest.TestCase):
    def test_thai_regional_accuracy(self):
        target_date = date(2026, 9, 4)
        for loc in THAI_REGIONAL_CAPITALS:
            coords = Coordinates(loc["lat"], loc["lon"])
            res = get_solar_times(coords, target_date, use_cache=True)
            self.assertEqual(res.gmt_offset, loc["expected_tz"])
            # Sunrise in Thailand should be between 05:30 and 06:45
            hour_sunrise = int(res.sunrise.split(":")[0])
            self.assertIn(hour_sunrise, (5, 6))
            # Sunset in Thailand should be between 18:00 and 19:00
            hour_sunset = int(res.sunset.split(":")[0])
            self.assertIn(hour_sunset, (18, 19))

    def test_cache_hit_latency_under_25ms(self):
        coords = Coordinates(13.7563, 100.5018)
        target_date = date(2026, 9, 4)
        # Prime cache
        _ = get_solar_times(coords, target_date, use_cache=True)

        start = time.perf_counter()
        res = get_solar_times(coords, target_date, use_cache=True)
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        self.assertTrue(res.cached)
        # Verify cached retrieval is extremely fast
        self.assertLess(elapsed_ms, 25.0, f"Cache latency too high: {elapsed_ms:.2f}ms")

if __name__ == "__main__":
    unittest.main()

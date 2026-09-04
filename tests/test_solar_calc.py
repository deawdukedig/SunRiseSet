"""
Unit tests for solar_calc.py backward-compatible interface.
"""

import unittest
from datetime import date
import sys
import os

# Ensure src is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sunriseset.models import Coordinates
from sunriseset.ephemeris import calculate_offline_noaa, get_solar_times, format_gmt_offset
from sunriseset.geocoding import extract_thai_address_fields, forward_geocode

class TestSolarCalcLegacy(unittest.TestCase):
    def test_google_maps_url(self):
        c = Coordinates(13.7563, 100.5018)
        self.assertEqual(c.google_maps_url, "https://www.google.com/maps?q=13.756300,100.501800")

    def test_format_gmt_offset(self):
        self.assertEqual(format_gmt_offset(25200), "GMT+7")
        self.assertEqual(format_gmt_offset(0), "GMT+0")
        self.assertEqual(format_gmt_offset(-18000), "GMT-5")
        self.assertEqual(format_gmt_offset(19800), "GMT+05:30")

    def test_bangkok_offline_calculation(self):
        c = Coordinates(13.7563, 100.5018)
        res = calculate_offline_noaa(c, date(2026, 9, 4))
        self.assertIn("06:", res.sunrise)
        self.assertIn("18:", res.sunset)
        self.assertIn("12 ชั่วโมง", res.daylight_duration_text)
        self.assertEqual(res.gmt_offset, "GMT+7")
        self.assertTrue(res.google_maps_url.startswith("https://www.google.com/maps?q=13.756300,100.501800"))

    def test_bangkok_online_calculation(self):
        c = Coordinates(13.7563, 100.5018)
        res = get_solar_times(c, date(2026, 9, 4), use_cache=True)
        self.assertEqual(res.timezone, "Asia/Bangkok")
        self.assertEqual(res.gmt_offset, "GMT+7")
        self.assertEqual(res.sunrise, "06:06")
        self.assertEqual(res.sunset, "18:27")

    def test_invalid_coordinates(self):
        with self.assertRaises(ValueError):
            Coordinates(95.0, 100.0)
        with self.assertRaises(ValueError):
            Coordinates(13.0, 200.0)

    def test_polar_day_offline(self):
        c = Coordinates(88.0, 0.0)
        res = calculate_offline_noaa(c, date(2026, 6, 21))
        self.assertIn("ไม่ตก", res.sunrise)
        self.assertIn("Polar Day", res.sunrise)

    def test_polar_night_offline(self):
        c = Coordinates(88.0, 0.0)
        res = calculate_offline_noaa(c, date(2026, 12, 21))
        self.assertIn("ไม่ขึ้น", res.sunrise)
        self.assertIn("Polar Night", res.sunrise)

if __name__ == "__main__":
    unittest.main()

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from datetime import date
from sunriseset.models import Coordinates
from sunriseset.ephemeris import (
    format_gmt_offset,
    calculate_offline_noaa,
    get_solar_times,
)

class TestEphemeris(unittest.TestCase):
    def test_gmt_formatting(self):
        self.assertEqual(format_gmt_offset(25200), "GMT+7")
        self.assertEqual(format_gmt_offset(0), "GMT+0")
        self.assertEqual(format_gmt_offset(-18000), "GMT-5")
        self.assertEqual(format_gmt_offset(19800), "GMT+05:30")

    def test_offline_noaa_accuracy(self):
        # Bangkok on Sep 4
        coords = Coordinates(13.7563, 100.5018)
        res = calculate_offline_noaa(coords, date(2026, 9, 4))
        self.assertEqual(res.gmt_offset, "GMT+7")
        self.assertTrue(res.sunrise.startswith("06:"))
        self.assertTrue(res.sunset.startswith("18:"))
        self.assertIn("12 ชั่วโมง", res.daylight_duration_text)

    def test_online_open_meteo(self):
        coords = Coordinates(13.7563, 100.5018)
        res = get_solar_times(coords, date(2026, 9, 4), use_cache=True)
        self.assertEqual(res.timezone, "Asia/Bangkok")
        self.assertEqual(res.gmt_offset, "GMT+7")
        self.assertEqual(res.sunrise, "06:06")
        self.assertEqual(res.sunset, "18:27")
        self.assertEqual(res.solar_noon, "12:16")

    def test_polar_day(self):
        # Svalbard Arctic summer: lat 78.22, lon 15.63 on June 21
        coords = Coordinates(78.22, 15.63)
        res = calculate_offline_noaa(coords, date(2026, 6, 21))
        self.assertIn("ไม่ตก", res.sunrise)
        self.assertIn("Polar Day", res.sunrise)
        self.assertEqual(res.daylight_duration_seconds, 86400.0)

    def test_polar_night(self):
        # Svalbard Arctic winter: lat 78.22, lon 15.63 on Dec 21
        coords = Coordinates(78.22, 15.63)
        res = calculate_offline_noaa(coords, date(2026, 12, 21))
        self.assertIn("ไม่ขึ้น", res.sunrise)
        self.assertIn("Polar Night", res.sunrise)
    def test_historical_date_archive(self):
        # Historical date in 2020 via archive API
        coords = Coordinates(13.7563, 100.5018)
        res = get_solar_times(coords, date(2020, 1, 1), use_cache=True)
        self.assertEqual(res.timezone, "Asia/Bangkok")
        self.assertEqual(res.gmt_offset, "GMT+7")
        self.assertEqual(res.sunrise, "06:41")
        self.assertEqual(res.sunset, "18:01")

    def test_historical_date_ancient_noaa(self):
        # Historical date in 1782 via offline NOAA fallback
        coords = Coordinates(13.7563, 100.5018)
        res = get_solar_times(coords, date(1782, 4, 6), use_cache=True)
        self.assertEqual(res.gmt_offset, "GMT+7")
        self.assertTrue(res.sunrise.startswith("06:"))
        self.assertTrue(res.sunset.startswith("18:"))

if __name__ == "__main__":
    unittest.main()

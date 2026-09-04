"""
Tests for UTF-8 Report Generation in sunriseset.reporter.
Verifies UTF-8 encoding for both filenames and content, directory creation, and sanitization.
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sunriseset.reporter import save_report, sanitize_filename, generate_markdown_content

class TestReporter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except (PermissionError, OSError):
            import gc, time
            gc.collect()
            time.sleep(0.05)
            try:
                self.temp_dir.cleanup()
            except Exception:
                pass

    def test_sanitize_filename(self):
        dirty = 'รายงาน: 13.75/100.50 * "test" ? <ok> | end.'
        clean = sanitize_filename(dirty)
        for char in '<>:"/\\|?*':
            self.assertNotIn(char, clean)
        self.assertIn("รายงาน", clean)

    def test_save_report_utf8_filename_and_content(self):
        mock_data = {
            "date": "2026-09-04",
            "latitude": 13.7563,
            "longitude": 100.5018,
            "timezone": "Asia/Bangkok",
            "timezone_abbreviation": "GMT+7",
            "gmt_offset": "GMT+7",
            "utc_offset_seconds": 25200,
            "sunrise": "06:06",
            "sunset": "18:27",
            "daylight_duration_text": "12 ชั่วโมง 21 นาที",
            "daylight_duration_seconds": 44463.44,
            "google_maps_url": "https://www.google.com/maps?q=13.756300,100.501800",
            "address": {
                "road": "ถนนสุขุมวิท",
                "subdistrict": "ตำบลนาเกลือ",
                "district": "อำเภอบางละมุง",
                "province": "จังหวัดชลบุรี",
                "postcode": "20150",
                "country": "ประเทศไทย",
                "full_address": "ถนนสุขุมวิท, ตำบลนาเกลือ, อำเภอบางละมุง, จังหวัดชลบุรี, ประเทศไทย"
            },
            "source": "Open-Meteo API (Online)",
            "cached": True
        }

        report_path = save_report(mock_data, output_dir=self.temp_dir.name)
        self.assertTrue(os.path.exists(report_path))
        
        # Verify Thai characters and Buddhist Era year in filename
        filename = os.path.basename(report_path)
        self.assertIn("รายงานพระอาทิตย์", filename)
        self.assertIn("2569-09-04", filename)
        self.assertIn("ชลบุรี", filename)
        self.assertIn("บางละมุง", filename)

        # Verify UTF-8 content read
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("รายงานข้อมูลเวลาพระอาทิตย์ขึ้น-ตก", content)
        self.assertIn("ถนนสุขุมวิท", content)
        self.assertIn("ตำบลนาเกลือ", content)
        self.assertIn("อำเภอบางละมุง", content)
        self.assertIn("จังหวัดชลบุรี", content)
        self.assertIn("06:06", content)
        self.assertIn("18:27", content)

    def test_save_report_without_address(self):
        mock_data = {
            "date": "2026-09-04",
            "latitude": 0.0,
            "longitude": 0.0,
            "timezone": "UTC",
            "timezone_abbreviation": "GMT+0",
            "gmt_offset": "GMT+0",
            "utc_offset_seconds": 0,
            "sunrise": "06:00",
            "sunset": "18:00",
            "daylight_duration_text": "12 ชั่วโมง",
            "google_maps_url": "https://www.google.com/maps?q=0.0,0.0"
        }
        report_path = save_report(mock_data, output_dir=self.temp_dir.name)
        self.assertTrue(os.path.exists(report_path))
        filename = os.path.basename(report_path)
        self.assertIn("พิกัด_0.0000_0.0000", filename)

if __name__ == "__main__":
    unittest.main()

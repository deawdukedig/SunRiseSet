import unittest
from datetime import date
import io
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sunriseset.thai_date import convert_year_to_ce, parse_date_input, format_thai_date, to_thai_be_date_str
from sunriseset.cli import run

class TestThaiDate(unittest.TestCase):
    def test_convert_year_to_ce(self):
        self.assertEqual(convert_year_to_ce(2569), 2026)
        self.assertEqual(convert_year_to_ce(2500), 1957)
        self.assertEqual(convert_year_to_ce(2400), 1857)
        self.assertEqual(convert_year_to_ce(2026), 2026)
        self.assertEqual(convert_year_to_ce(1940), 1940)

    def test_parse_iso_be_and_ce(self):
        # BE ISO
        d1 = parse_date_input("2569-09-04")
        self.assertEqual(d1, date(2026, 9, 4))

        # CE ISO
        d2 = parse_date_input("2026-09-04")
        self.assertEqual(d2, date(2026, 9, 4))

        # Leap year in BE (2567 = 2024 CE)
        d3 = parse_date_input("2567-02-29")
        self.assertEqual(d3, date(2024, 2, 29))

    def test_parse_dmy(self):
        d1 = parse_date_input("04/09/2569")
        self.assertEqual(d1, date(2026, 9, 4))
        d2 = parse_date_input("04-09-2026")
        self.assertEqual(d2, date(2026, 9, 4))

    def test_parse_natural_thai(self):
        # Full Thai month
        d1 = parse_date_input("4 กันยายน 2569")
        self.assertEqual(d1, date(2026, 9, 4))

        # With leading prefix
        d2 = parse_date_input("วันที่ 4 กันยายน 2569")
        self.assertEqual(d2, date(2026, 9, 4))

        # Abbreviated month
        d3 = parse_date_input("1 ม.ค. 2563")
        self.assertEqual(d3, date(2020, 1, 1))

        # Historical BE date
        d4 = parse_date_input("31 ธันวาคม 2525")
        self.assertEqual(d4, date(1982, 12, 31))

        # With explicit พ.ศ.
        d5 = parse_date_input("15 เม.ย. พ.ศ. 2568")
        self.assertEqual(d5, date(2025, 4, 15))

        # With explicit ค.ศ.
        d6 = parse_date_input("10 พฤษภาคม ค.ศ. 2024")
        self.assertEqual(d6, date(2024, 5, 10))

    def test_parse_invalid(self):
        with self.assertRaises(ValueError):
            parse_date_input("invalid-date-format")
        with self.assertRaises(ValueError):
            parse_date_input("2569-13-45")

    def test_format_thai_date(self):
        formatted_with_ce = format_thai_date(date(2026, 9, 4))
        self.assertEqual(formatted_with_ce, "4 กันยายน พ.ศ. 2569 (2026-09-04)")

        formatted_no_ce = format_thai_date(date(2026, 9, 4), include_ce=False)
        self.assertEqual(formatted_no_ce, "4 กันยายน พ.ศ. 2569")

    def test_to_thai_be_date_str(self):
        self.assertEqual(to_thai_be_date_str(date(2026, 9, 4)), "2569-09-04")
        self.assertEqual(to_thai_be_date_str("2026-09-04"), "2569-09-04")
        self.assertEqual(to_thai_be_date_str("1982-12-31"), "2525-12-31")
        self.assertEqual(to_thai_be_date_str("2569-09-04"), "2569-09-04")


    def test_cli_buddhist_era_support(self):
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            code = run(["--lat", "13.7563", "--lon", "100.5018", "--date", "2569-09-04", "--no-report"])
            self.assertEqual(code, 0)
            data = json.loads(buf.getvalue())
            self.assertTrue(data["success"])
            self.assertEqual(data["data"]["date"], "2026-09-04")
            self.assertIn("2569", data["data"]["date_thai"])
            self.assertIn("กันยายน", data["data"]["date_thai"])
        finally:
            sys.stdout = old_stdout

if __name__ == "__main__":
    unittest.main()

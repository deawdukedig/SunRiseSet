import unittest
import io
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sunriseset.cli import run

class TestCLI(unittest.TestCase):
    def test_cli_success_exit_code(self):
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            code = run(["--lat", "13.7563", "--lon", "100.5018"])
            self.assertEqual(code, 0)
            data = json.loads(buf.getvalue())
            self.assertTrue(data["success"])
            self.assertIn("sunrise", data["data"])
            self.assertIn("sunset", data["data"])
            self.assertIn("address", data["data"])
            self.assertIn("report_path", data["data"])
        finally:
            sys.stdout = old_stdout

    def test_cli_no_report_flag(self):
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            code = run(["--lat", "13.7563", "--lon", "100.5018", "--no-report"])
            self.assertEqual(code, 0)
            data = json.loads(buf.getvalue())
            self.assertTrue(data["success"])
            self.assertIsNone(data["data"].get("report_path"))
        finally:
            sys.stdout = old_stdout

    def test_cli_invalid_coordinates_exit_code(self):
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            code = run(["--lat", "105.0", "--lon", "100.0"])
            self.assertEqual(code, 1)
            data = json.loads(buf.getvalue())
            self.assertFalse(data["success"])
            self.assertEqual(data["error"]["code"], "INVALID_INPUT")
        finally:
            sys.stdout = old_stdout

    def test_cli_invalid_date_exit_code(self):
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            code = run(["--lat", "13.0", "--lon", "100.0", "--date", "2026-02-30"])
            self.assertEqual(code, 1)
            data = json.loads(buf.getvalue())
            self.assertFalse(data["success"])
            self.assertEqual(data["error"]["code"], "INVALID_DATE")
        finally:
            sys.stdout = old_stdout

    def test_cli_brief_card(self):
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            code = run(["--brief"])
            self.assertEqual(code, 0)
            data = json.loads(buf.getvalue())
            self.assertEqual(data["name"], "sunriseset")
            self.assertIn("version", data)
        finally:
            sys.stdout = old_stdout

if __name__ == "__main__":
    unittest.main()

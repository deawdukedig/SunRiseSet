import unittest
import tempfile
import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from pathlib import Path
from sunriseset.cache import SQLiteCache

class TestCache(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_cache.db")
        self.cache = SQLiteCache(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_set_and_get(self):
        self.cache.set("key1", {"value": 42}, ttl_seconds=10)
        val = self.cache.get("key1")
        self.assertEqual(val, {"value": 42})

    def test_get_nonexistent(self):
        self.assertIsNone(self.cache.get("missing_key"))

    def test_ttl_expiration(self):
        # Set with 0 second TTL
        self.cache.set("short_lived", "expired_data", ttl_seconds=0)
        time.sleep(0.05)
        self.assertIsNone(self.cache.get("short_lived"))

    def test_clear_cache(self):
        self.cache.set("a", 1)
        self.cache.set("b", 2)
        self.cache.clear()
        self.assertIsNone(self.cache.get("a"))
        self.assertIsNone(self.cache.get("b"))

if __name__ == "__main__":
    unittest.main()

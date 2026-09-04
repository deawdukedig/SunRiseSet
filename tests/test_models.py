import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sunriseset.models import Coordinates, AddressInfo, SolarResult, EnvelopeResponse

class TestModels(unittest.TestCase):
    def test_valid_coordinates(self):
        c = Coordinates(13.7563, 100.5018)
        self.assertEqual(c.latitude, 13.7563)
        self.assertEqual(c.longitude, 100.5018)
        self.assertEqual(c.google_maps_url, "https://www.google.com/maps?q=13.756300,100.501800")

    def test_invalid_lat_bounds(self):
        with self.assertRaises(ValueError):
            Coordinates(-91.0, 0.0)
        with self.assertRaises(ValueError):
            Coordinates(90.1, 0.0)

    def test_invalid_lon_bounds(self):
        with self.assertRaises(ValueError):
            Coordinates(0.0, -180.1)
        with self.assertRaises(ValueError):
            Coordinates(0.0, 180.1)

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            Coordinates("13.7563", 100.5018) # type: ignore

    def test_address_info_to_dict(self):
        addr = AddressInfo(
            road="ถนนสุขุมวิท",
            subdistrict="ตำบลนาเกลือ",
            district="อำเภอบางละมุง",
            province="จังหวัดชลบุรี",
            postcode="20150",
            country="ประเทศไทย",
            full_address="สุขุมวิท นาเกลือ บางละมุง ชลบุรี"
        )
        d = addr.to_dict()
        self.assertEqual(d["road"], "ถนนสุขุมวิท")
        self.assertEqual(d["district"], "อำเภอบางละมุง")

    def test_envelope_response(self):
        env = EnvelopeResponse(success=True, data={"sample": 123})
        d = env.to_dict()
        self.assertTrue(d["success"])
        self.assertEqual(d["data"]["sample"], 123)
        self.assertIsNone(d["error"])

if __name__ == "__main__":
    unittest.main()

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sunriseset.geocoding import extract_thai_address_fields, reverse_geocode, forward_geocode
from sunriseset.models import AddressInfo

class TestGeocoding(unittest.TestCase):
    def test_thai_address_parsing_with_prefixes(self):
        sample_addr = {
            "road": "ถนนสุขุมวิท",
            "quarter": "แขวงคลองเตย",
            "county": "เขตคลองเตย",
            "city": "กรุงเทพมหานคร",
            "postcode": "10110",
            "country": "ประเทศไทย"
        }
        res = extract_thai_address_fields(sample_addr, "ถนนสุขุมวิท, แขวงคลองเตย, เขตคลองเตย, กรุงเทพมหานคร")
        self.assertEqual(res.road, "ถนนสุขุมวิท")
        self.assertEqual(res.subdistrict, "แขวงคลองเตย")
        self.assertEqual(res.district, "เขตคลองเตย")
        self.assertEqual(res.province, "กรุงเทพมหานคร")
        self.assertEqual(res.postcode, "10110")
        self.assertEqual(res.country, "ประเทศไทย")

    def test_thai_address_parsing_provinces(self):
        sample_addr = {
            "road": "ถนนมิตรภาพ",
            "village": "ตำบลในเมือง",
            "county": "อำเภอเมืองนครราชสีมา",
            "province": "จังหวัดนครราชสีมา",
            "postcode": "30000",
            "country": "ประเทศไทย"
        }
        res = extract_thai_address_fields(sample_addr)
        self.assertEqual(res.road, "ถนนมิตรภาพ")
        self.assertEqual(res.subdistrict, "ตำบลในเมือง")
        self.assertEqual(res.district, "อำเภอเมืองนครราชสีมา")
        self.assertEqual(res.province, "จังหวัดนครราชสีมา")

    def test_reverse_geocode_live(self):
        # Bangkok Democracy Monument: 13.7563, 100.5018
        info = reverse_geocode(13.7563, 100.5018, use_cache=True)
        self.assertIsInstance(info, AddressInfo)
        self.assertEqual(info.province, "กรุงเทพมหานคร")
        self.assertEqual(info.district, "เขตพระนคร")
        self.assertEqual(info.subdistrict, "แขวงบวรนิเวศ")

    def test_forward_geocode_live(self):
        coords, info = forward_geocode("อำเภอเมือง เชียงใหม่", use_cache=True)
        self.assertAlmostEqual(coords.latitude, 18.787, places=1)
        self.assertAlmostEqual(coords.longitude, 98.967, places=1)
        self.assertIn("เชียงใหม่", info.province)

    def test_normalize_thai_query_abbreviations(self):
        from sunriseset.geocoding import normalize_thai_query

        # Test abbreviation expansions
        cands = normalize_thai_query("ต.ท่าเสา อ.เมือง จ.อุตรดิตถ์")
        self.assertTrue(any("ตำบลท่าเสา" in c and "อำเภอเมือง" in c and "จังหวัดอุตรดิตถ์" in c for c in cands))

        # Test Bangkok abbreviations
        cands_bkk = normalize_thai_query("สยามพารากอน ปทุมวัน กทม")
        self.assertTrue(any("กรุงเทพมหานคร" in c for c in cands_bkk))

        # Test isolated 'เมือง'
        cands_mueang = normalize_thai_query("หนองบัว ท่าเสา เมือง อุตรดิตถ์")
        self.assertTrue(any("อำเภอเมือง" in c for c in cands_mueang))

        # Test punctuation and separator stripping
        cands_punct = normalize_thai_query("หนองบัว, ท่าเสา - อุตรดิตถ์")
        self.assertTrue(all("," not in c and "-" not in c for c in cands_punct))

if __name__ == "__main__":
    unittest.main()

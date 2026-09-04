"""
Thai Geocoding & Reverse-Geocoding Module for SunRiseSet.
Features:
- Full extraction of Thai administrative units: ถนน, ตำบล/แขวง, อำเภอ/เขต, จังหวัด
- Rate limit throttling compliant with OpenStreetMap Nominatim Policy (max 1 req/sec)
- Local SQLite caching to eliminate repeated API queries
- Automatic retry with exponential backoff on HTTP 429 or transient network errors
- Fallback for offline environments
"""

import time
import json
import logging
import urllib.request
import urllib.parse
import urllib.error
from typing import Tuple, Optional

from .models import AddressInfo, Coordinates
from .cache import default_cache

logger = logging.getLogger("sunriseset.geocoding")

USER_AGENT = "SunRiseSet-Production/2.0 (Contact: admin@sunriseset.local)"
_last_request_time = 0.0

def _rate_limit():
    """Ensure at least 1.0 second between consecutive un-cached network calls to Nominatim."""
    global _last_request_time
    now = time.time()
    elapsed = now - _last_request_time
    if elapsed < 1.0:
        time.sleep(1.0 - elapsed)
    _last_request_time = time.time()

def _http_get_with_retry(url: str, max_retries: int = 3, timeout: float = 6.0) -> bytes:
    """Execute HTTP GET with exponential backoff for 429/5xx errors."""
    _rate_limit()
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                backoff = (2 ** attempt) + 0.5
                logger.warning(f"HTTP {e.code} received from upstream. Retrying in {backoff:.1f}s...")
                time.sleep(backoff)
            else:
                raise
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < max_retries - 1:
                backoff = (2 ** attempt) + 0.5
                logger.warning(f"Network error: {e}. Retrying in {backoff:.1f}s...")
                time.sleep(backoff)
            else:
                raise
    raise TimeoutError(f"Failed to fetch {url} after {max_retries} attempts.")

def extract_thai_address_fields(addr: dict, display_name: str = "") -> AddressInfo:
    """Parse address dictionary into Thai administrative structure."""
    road = addr.get("road") or addr.get("pedestrian") or addr.get("highway") or "-"
    subdistrict = "-"
    district = "-"
    province = "-"

    # Prioritize scanning for explicit Thai administrative prefixes
    for k, v in addr.items():
        if not isinstance(v, str):
            continue
        v_clean = v.strip()
        if (v_clean.startswith("ถนน") or v_clean.startswith("ซอย")) and road == "-":
            road = v_clean
        elif v_clean.startswith("ตำบล") or v_clean.startswith("แขวง"):
            subdistrict = v_clean
        elif (v_clean.startswith("อำเภอ") or v_clean.startswith("เขต")) and not v_clean.startswith("เขตการปกครอง"):
            district = v_clean
        elif v_clean.startswith("จังหวัด") or v_clean == "กรุงเทพมหานคร":
            province = v_clean

    # Fallback mappings if prefixes are omitted
    if subdistrict == "-":
        subdistrict = addr.get("quarter") or addr.get("suburb") or addr.get("neighbourhood") or addr.get("village") or "-"
    if district == "-":
        district = addr.get("county") or addr.get("city_district") or addr.get("suburb") or addr.get("district") or "-"
    if province == "-":
        province = addr.get("province") or addr.get("state") or addr.get("city") or "-"

    postcode = addr.get("postcode", "-")
    country = addr.get("country", "-")

    if not display_name:
        parts = [p for p in [road, subdistrict, district, province, country] if p != "-"]
        display_name = ", ".join(parts) if parts else "ไม่ทราบที่อยู่แน่ชัด"

    return AddressInfo(
        road=road,
        subdistrict=subdistrict,
        district=district,
        province=province,
        postcode=postcode,
        country=country,
        full_address=display_name
    )

def reverse_geocode(lat: float, lon: float, use_cache: bool = True) -> AddressInfo:
    """
    Reverse geocode coordinates into a structured AddressInfo.
    Checks cache first, then queries Nominatim with rate limiting.
    """
    cache_key = f"revgeo:{lat:.4f}:{lon:.4f}"
    if use_cache:
        cached_val = default_cache.get(cache_key)
        if cached_val:
            return AddressInfo(**cached_val)

    params = {
        "format": "json",
        "lat": lat,
        "lon": lon,
        "accept-language": "th",
        "addressdetails": 1,
    }
    url = f"https://nominatim.openstreetmap.org/reverse?{urllib.parse.urlencode(params)}"

    try:
        raw_data = _http_get_with_retry(url)
        data = json.loads(raw_data.decode("utf-8"))
        addr_dict = data.get("address", {})
        display_name = data.get("display_name", "")
        info = extract_thai_address_fields(addr_dict, display_name)

        if use_cache:
            default_cache.set(cache_key, info.to_dict(), ttl_seconds=86400 * 7) # 7 days
        return info
    except Exception as e:
        logger.warning(f"Reverse geocode failed for {lat}, {lon}: {e}. Using fallback.")
        return AddressInfo(
            road="-",
            subdistrict="-",
            district="-",
            province="-",
            postcode="-",
            country="-",
            full_address=f"พิกัด {lat:.4f}, {lon:.4f}"
        )

def forward_geocode(query: str, use_cache: bool = True) -> Tuple[Coordinates, AddressInfo]:
    """
    Forward geocode a location search query into Coordinates and AddressInfo.
    """
    query_clean = query.strip()
    cache_key = f"fwdgeo:{query_clean.lower()}"
    if use_cache:
        cached_val = default_cache.get(cache_key)
        if cached_val:
            coords = Coordinates(latitude=cached_val["latitude"], longitude=cached_val["longitude"])
            addr = AddressInfo(**cached_val["address"])
            return coords, addr

    params = {
        "q": query_clean,
        "format": "json",
        "limit": 1,
        "accept-language": "th",
        "addressdetails": 1
    }
    url = f"https://nominatim.openstreetmap.org/search?{urllib.parse.urlencode(params)}"

    try:
        raw_data = _http_get_with_retry(url)
        data = json.loads(raw_data.decode("utf-8"))
        if not data:
            raise ValueError(f"ไม่พบข้อมูลตำแหน่งสำหรับ: '{query_clean}'")

        item = data[0]
        coords = Coordinates(latitude=float(item["lat"]), longitude=float(item["lon"]))
        addr_dict = item.get("address", {})
        display_name = item.get("display_name", query_clean)
        addr = extract_thai_address_fields(addr_dict, display_name)

        if use_cache:
            default_cache.set(cache_key, {
                "latitude": coords.latitude,
                "longitude": coords.longitude,
                "address": addr.to_dict()
            }, ttl_seconds=86400 * 7)

        return coords, addr
    except ValueError:
        raise
    except Exception as e:
        raise ConnectionError(f"ไม่สามารถเชื่อมต่อระบบค้นหาตำแหน่งได้: {e}")

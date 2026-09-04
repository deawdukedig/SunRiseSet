"""
Astronomical Ephemeris Module for SunRiseSet.
Calculates Sunrise, Sunset, Solar Noon, and Daylight Duration.
Features:
- Primary Engine: High-precision Open-Meteo Astronomical API with official IANA Timezones and DST detection
- Offline Fallback: NOAA Solar Calculation Algorithm (Pure Python standard library)
- Caching: Caches solar results by coordinate and date to minimize latency
- Polar Handling: Accurately identifies Midnight Sun (Polar Day) and Polar Night
"""

import math
import json
import logging
import urllib.request
import urllib.error
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any

from .models import Coordinates, SolarResult, AddressInfo
from .cache import default_cache

logger = logging.getLogger("sunriseset.ephemeris")

def format_gmt_offset(offset_seconds: int) -> str:
    """Format seconds offset to standard GMT string (e.g. +25200 -> GMT+7)."""
    total_minutes = int(offset_seconds // 60)
    sign = "+" if total_minutes >= 0 else "-"
    total_minutes = abs(total_minutes)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    if minutes == 0:
        return f"GMT{sign}{hours}"
    return f"GMT{sign}{hours:02d}:{minutes:02d}"

def calculate_offline_noaa(coords: Coordinates, target_date: date) -> SolarResult:
    """
    Offline NOAA Solar Calculation Algorithm.
    Accurate to within 1-2 minutes for all non-polar latitudes.
    """
    lat = coords.latitude
    lon = coords.longitude

    approx_tz_hours = round(lon / 15.0)
    tz_offset_sec = approx_tz_hours * 3600
    gmt_str = format_gmt_offset(tz_offset_sec)

    # Julian Day calculation
    a = (14 - target_date.month) // 12
    y = target_date.year + 4800 - a
    m = target_date.month + 12 * a - 3
    julian_day = target_date.day + ((153 * m + 2) // 5) + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    t = (julian_day - 2451545.0) / 36525.0

    geom_mean_long_sun = (280.46646 + t * (36000.76983 + 0.0003032 * t)) % 360.0
    geom_mean_anom_sun = 357.52911 + t * (35999.05029 - 0.0001537 * t)
    eccent_earth_orbit = 0.016708634 - t * (0.000042037 + 0.0000001267 * t)

    anom_rad = math.radians(geom_mean_anom_sun)
    sun_eq_of_ctr = (math.sin(anom_rad) * (1.914602 - t * (0.004817 + 0.000014 * t)) +
                     math.sin(2 * anom_rad) * (0.019993 - 0.000101 * t) +
                     math.sin(3 * anom_rad) * 0.000289)

    sun_true_long = geom_mean_long_sun + sun_eq_of_ctr
    sun_app_long = sun_true_long - 0.00569 - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * t))
    mean_obliq = 23 + (26 + ((21.448 - t * (46.815 + t * (0.00059 - t * 0.001813)))) / 60) / 60
    obliq_corr = mean_obliq + 0.00256 * math.cos(math.radians(125.04 - 1934.136 * t))
    sin_declin = math.sin(math.radians(obliq_corr)) * math.sin(math.radians(sun_app_long))
    sun_declin = math.degrees(math.asin(sin_declin))

    var_y = math.tan(math.radians(obliq_corr / 2)) ** 2
    geom_rad = math.radians(geom_mean_long_sun)
    eq_of_time = 4 * math.degrees(
        var_y * math.sin(2 * geom_rad) -
        2 * eccent_earth_orbit * math.sin(anom_rad) +
        4 * eccent_earth_orbit * var_y * math.sin(anom_rad) * math.cos(2 * geom_rad) -
        0.5 * (var_y ** 2) * math.sin(4 * geom_rad) -
        1.25 * (eccent_earth_orbit ** 2) * math.sin(2 * anom_rad)
    )

    zenith = 90.8333
    lat_rad = math.radians(lat)
    declin_rad = math.radians(sun_declin)

    cos_ha = (math.cos(math.radians(zenith)) / (math.cos(lat_rad) * math.cos(declin_rad))) - (math.tan(lat_rad) * math.tan(declin_rad))

    is_polar_day = False
    is_polar_night = False

    if cos_ha > 1.0:
        is_polar_night = True
        ha_sunrise = None
    elif cos_ha < -1.0:
        is_polar_day = True
        ha_sunrise = None
    else:
        ha_sunrise = math.degrees(math.acos(cos_ha))

    solar_noon_utc_min = (720 - 4 * lon - eq_of_time) % 1440
    solar_noon_sec = int(solar_noon_utc_min * 60) + tz_offset_sec
    solar_noon_dt = datetime.combine(target_date, datetime.min.time()) + timedelta(seconds=solar_noon_sec % 86400)
    solar_noon_str = solar_noon_dt.strftime("%H:%M")

    if is_polar_day:
        sunrise_str = "ไม่ตก (พระอาทิตย์เที่ยงคืน / Polar Day)"
        sunset_str = "ไม่ตก (พระอาทิตย์เที่ยงคืน / Polar Day)"
        duration_str = "24 ชั่วโมง 00 นาที"
        duration_sec = 86400.0
    elif is_polar_night:
        sunrise_str = "ไม่ขึ้น (คืนขั้วโลก / Polar Night)"
        sunset_str = "ไม่ขึ้น (คืนขั้วโลก / Polar Night)"
        duration_str = "0 ชั่วโมง 00 นาที"
        duration_sec = 0.0
    else:
        sunrise_utc_min = (solar_noon_utc_min - ha_sunrise * 4) % 1440
        sunset_utc_min = (solar_noon_utc_min + ha_sunrise * 4) % 1440

        sunrise_sec = int(sunrise_utc_min * 60) + tz_offset_sec
        sunset_sec = int(sunset_utc_min * 60) + tz_offset_sec

        sunrise_dt = datetime.combine(target_date, datetime.min.time()) + timedelta(seconds=sunrise_sec % 86400)
        sunset_dt = datetime.combine(target_date, datetime.min.time()) + timedelta(seconds=sunset_sec % 86400)

        sunrise_str = sunrise_dt.strftime("%H:%M")
        sunset_str = sunset_dt.strftime("%H:%M")

        duration_min = int(ha_sunrise * 8)
        dur_h = duration_min // 60
        dur_m = duration_min % 60
        duration_str = f"{dur_h} ชั่วโมง {dur_m:02d} นาที"
        duration_sec = float(duration_min * 60)

    return SolarResult(
        date=target_date.isoformat(),
        latitude=lat,
        longitude=lon,
        timezone=f"Offline Estimated ({gmt_str})",
        timezone_abbreviation=gmt_str,
        gmt_offset=gmt_str,
        utc_offset_seconds=tz_offset_sec,
        sunrise=sunrise_str,
        sunset=sunset_str,
        solar_noon=solar_noon_str,
        daylight_duration_text=duration_str,
        daylight_duration_seconds=duration_sec,
        google_maps_url=coords.google_maps_url,
        source="NOAA Solar Algorithm (Offline)",
        cached=False
    )

def fetch_online_open_meteo(coords: Coordinates, target_date: date) -> SolarResult:
    """Fetch solar events and timezone from Open-Meteo API (Forecast or Historical Archive)."""
    date_str = target_date.isoformat()
    today = date.today()

    # If the date is more than 3 days in the past, use the Historical Archive API (available back to 1940)
    if target_date < today - timedelta(days=3):
        base_url = "https://archive-api.open-meteo.com/v1/archive"
        source_label = "Open-Meteo Historical Archive API (Online)"
    else:
        base_url = "https://api.open-meteo.com/v1/forecast"
        source_label = "Open-Meteo API (Online)"

    url = (
        f"{base_url}?"
        f"latitude={coords.latitude}&longitude={coords.longitude}&"
        f"daily=sunrise,sunset,daylight_duration&"
        f"timezone=auto&start_date={date_str}&end_date={date_str}"
    )

    req = urllib.request.Request(url, headers={"User-Agent": "SunRiseSet-Production/2.0"})
    with urllib.request.urlopen(req, timeout=6.0) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    tz_name = data.get("timezone", "UTC")
    tz_abbr = data.get("timezone_abbreviation", "")
    offset_sec = data.get("utc_offset_seconds", 0)
    gmt_str = format_gmt_offset(offset_sec)

    daily = data.get("daily", {})
    sunrise_raw = daily.get("sunrise", [None])[0]
    sunset_raw = daily.get("sunset", [None])[0]
    daylight_sec = daily.get("daylight_duration", [None])[0]

    sunrise_time = sunrise_raw.split("T")[1] if sunrise_raw and "T" in sunrise_raw else "ไม่พบเวลาขึ้น (Polar Day/Night)"
    sunset_time = sunset_raw.split("T")[1] if sunset_raw and "T" in sunset_raw else "ไม่พบเวลาตก (Polar Day/Night)"

    if daylight_sec is not None:
        total_m = int(round(daylight_sec / 60))
        dur_h = total_m // 60
        dur_m = total_m % 60
        duration_str = f"{dur_h} ชั่วโมง {dur_m:02d} นาที"
    else:
        duration_str = "N/A"

    solar_noon_time = None
    if sunrise_raw and sunset_raw and "T" in sunrise_raw and "T" in sunset_raw:
        try:
            t_rise = datetime.fromisoformat(sunrise_raw)
            t_set = datetime.fromisoformat(sunset_raw)
            noon_dt = t_rise + (t_set - t_rise) / 2
            solar_noon_time = noon_dt.strftime("%H:%M")
        except Exception:
            pass

    return SolarResult(
        date=date_str,
        latitude=coords.latitude,
        longitude=coords.longitude,
        timezone=tz_name,
        timezone_abbreviation=tz_abbr if tz_abbr else gmt_str,
        gmt_offset=gmt_str,
        utc_offset_seconds=offset_sec,
        sunrise=sunrise_time,
        sunset=sunset_time,
        solar_noon=solar_noon_time,
        daylight_duration_text=duration_str,
        daylight_duration_seconds=daylight_sec,
        google_maps_url=coords.google_maps_url,
        source=source_label,
        cached=False
    )

def get_solar_times(coords: Coordinates, target_date: Optional[date] = None, use_cache: bool = True) -> SolarResult:
    """
    Get solar times for coordinates. Checks cache first, tries Open-Meteo,
    falls back to NOAA offline calculation.
    """
    if target_date is None:
        target_date = date.today()

    cache_key = f"solar:{coords.latitude:.4f}:{coords.longitude:.4f}:{target_date.isoformat()}"
    if use_cache:
        cached_data = default_cache.get(cache_key)
        if cached_data:
            if not cached_data.get("solar_noon") and cached_data.get("sunrise") and cached_data.get("sunset"):
                try:
                    sr = cached_data["sunrise"]
                    ss = cached_data["sunset"]
                    if ":" in sr and ":" in ss and "ไม่" not in sr:
                        hr_r, mn_r = map(int, sr.split(":")[:2])
                        hr_s, mn_s = map(int, ss.split(":")[:2])
                        min_r = hr_r * 60 + mn_r
                        min_s = hr_s * 60 + mn_s
                        noon_min = (min_r + min_s) // 2
                        cached_data["solar_noon"] = f"{noon_min // 60:02d}:{noon_min % 60:02d}"
                except Exception:
                    pass
            cached_data["cached"] = True
            return SolarResult(**cached_data)

    try:
        result = fetch_online_open_meteo(coords, target_date)
    except Exception as e:
        logger.warning(f"Online solar fetch failed: {e}. Falling back to NOAA algorithm.")
        result = calculate_offline_noaa(coords, target_date)

    if use_cache:
        # Cache for 24 hours
        dict_val = result.to_dict()
        dict_val.pop("address", None)
        default_cache.set(cache_key, dict_val, ttl_seconds=86400)

    return result

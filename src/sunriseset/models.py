"""
Data models and schemas for the SunRiseSet package.
Provides strong type hints, validation, and JSON serialization.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
from datetime import date

@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float

    def __post_init__(self):
        if not isinstance(self.latitude, (int, float)):
            raise TypeError(f"Latitude ต้องเป็นตัวเลข (ได้รับ {type(self.latitude).__name__})")
        if not isinstance(self.longitude, (int, float)):
            raise TypeError(f"Longitude ต้องเป็นตัวเลข (ได้รับ {type(self.longitude).__name__})")
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError(f"Latitude ต้องอยู่ระหว่าง -90.0 ถึง 90.0 (ได้รับ {self.latitude})")
        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError(f"Longitude ต้องอยู่ระหว่าง -180.0 ถึง 180.0 (ได้รับ {self.longitude})")

    @property
    def google_maps_url(self) -> str:
        return f"https://www.google.com/maps?q={self.latitude:.6f},{self.longitude:.6f}"


@dataclass
class AddressInfo:
    road: str = "-"
    subdistrict: str = "-"       # ตำบล / แขวง
    district: str = "-"          # อำเภอ / เขต
    province: str = "-"          # จังหวัด
    postcode: str = "-"
    country: str = "-"
    full_address: str = "-"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SolarResult:
    date: str
    latitude: float
    longitude: float
    timezone: str
    timezone_abbreviation: str
    gmt_offset: str
    utc_offset_seconds: int
    sunrise: str
    sunset: str
    daylight_duration_text: str
    daylight_duration_seconds: Optional[float]
    google_maps_url: str
    address: Optional[AddressInfo] = None
    solar_noon: Optional[str] = None
    source: str = "Unknown"
    cached: bool = False
    report_path: Optional[str] = None
    date_thai: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.address:
            data["address"] = self.address.to_dict()
        return data


@dataclass
class EnvelopeResponse:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

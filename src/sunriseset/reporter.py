"""
Automatic Reporting Module for SunRiseSet.
Generates and saves comprehensive Thai Markdown reports into report/ directory.
Guarantees UTF-8 encoding for both filenames and content, with Windows filesystem safety.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import SolarResult
from .thai_date import to_thai_be_date_str

DEFAULT_REPORT_DIR = "report"

def sanitize_filename(name: str) -> str:
    """
    Sanitize filename for Windows, Linux, and macOS while preserving UTF-8 (Thai characters).
    Removes or replaces illegal Windows characters: < > : " / \ | ? *
    """
    # Replace illegal filename characters with underscore
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Strip whitespace and trailing dots
    sanitized = sanitized.strip().strip('.')
    # Collapse multiple underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized if sanitized else "รายงาน_ไม่ระบุชื่อ"

def generate_markdown_content(data: dict) -> str:
    """Generate professional Thai Markdown report content."""
    addr = data.get("address") or {}
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md_lines = [
        "# ☀️ รายงานข้อมูลเวลาพระอาทิตย์ขึ้น-ตก (Solar Ephemeris Report)",
        "",
        f"> **สร้างเมื่อวันที่-เวลา**: `{now_str}`  ",
        f"> **ระบบประมวลผล**: `SunRiseSet Production Engine v2.0`  ",
        f"> **แหล่งข้อมูล**: `{data.get('source', 'Unknown')}` {'(แคช)' if data.get('cached') else ''}",
        "",
        "---",
        "",
        "## 📍 ข้อมูลตำแหน่งและเขตการปกครอง",
        "",
        "| รายการ | ข้อมูล |",
        "| :--- | :--- |",
        f"| **ถนน (Road)** | {addr.get('road', '-')} |",
        f"| **ตำบล / แขวง (Subdistrict)** | {addr.get('subdistrict', '-')} |",
        f"| **อำเภอ / เขต (District)** | {addr.get('district', '-')} |",
        f"| **จังหวัด (Province)** | {addr.get('province', '-')} |",
        f"| **รหัสไปรษณีย์ (Postcode)** | {addr.get('postcode', '-')} |",
        f"| **ประเทศ (Country)** | {addr.get('country', '-')} |",
        f"| **พิกัด (Latitude, Longitude)** | `{data.get('latitude', 0.0):.6f}, {data.get('longitude', 0.0):.6f}` |",
        f"| **แผนที่ Google Maps** | [คลิกเพื่อเปิดดูพิกัดบน Google Maps]({data.get('google_maps_url', '#')}) |",
        f"| **ที่อยู่เต็ม (Full Address)** | {addr.get('full_address', '-')} |",
        "",
        "---",
        "",
        "## ⏰ ข้อมูลเวลาสุริยะและดาราศาสตร์ (Local Time)",
        "",
        f"- **วันที่คำนวณ**: `{data.get('date_thai') or data.get('date')}`",
        f"- **เขตเวลา (Timezone)**: `{data.get('timezone')}` (**`{data.get('gmt_offset', data.get('timezone_abbreviation'))}`**)",
        f"- **UTC Offset (วินาที)**: `{data.get('utc_offset_seconds')}`",
        "",
        "| ปรากฏการณ์ | เวลาท้องถิ่น | รายละเอียด |",
        "| :--- | :---: | :--- |",
        f"| 🌅 **พระอาทิตย์ขึ้น (Sunrise)** | **`{data.get('sunrise')}` น.** | แสงแรกของวัน ณ ขอบฟ้าท้องถิ่น |",
        f"| 🌇 **พระอาทิตย์ตก (Sunset)** | **`{data.get('sunset')}` น.** | แสงสุดท้ายของวัน ณ ขอบฟ้าท้องถิ่น |",
    ]

    if data.get("solar_noon"):
        md_lines.append(f"| ☀️ **เที่ยงวันสุริยะ (Solar Noon)** | **`{data.get('solar_noon')}` น.** | จุดที่ดวงอาทิตย์อยู่ตำแหน่งสูงสุดบนท้องฟ้า |")

    md_lines.extend([
        f"| ⏱️ **ความยาวช่วงเวลากลางวัน** | **`{data.get('daylight_duration_text')}`** | ระยะเวลาที่ดวงอาทิตย์อยู่เหนือขอบฟ้า |",
        "",
        "> [!NOTE]",
        f"> เวลาทั้งหมดถูกแปลงเป็นเวลาท้องถิ่นของพื้นที่ (`{data.get('gmt_offset', data.get('timezone_abbreviation'))}`) เรียบร้อยแล้ว",
        "",
        "---",
        "*สร้างรายงานอัตโนมัติโดย SunRiseSet — Thai Solar Ephemeris & Geocoding System*"
    ])

    return "\n".join(md_lines) + "\n"

def save_report(
    data: dict,
    output_dir: str = DEFAULT_REPORT_DIR
) -> str:
    """
    Save the calculation report into the report/ directory.
    Uses UTF-8 encoding for both filename and file content.
    Returns the absolute or normalized path of the saved file.
    """
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    addr = data.get("address") or {}
    prov = addr.get("province", "-").replace("จังหวัด", "").strip()
    dist = addr.get("district", "-").replace("อำเภอ", "").replace("เขต", "").strip()

    # Create Thai location identifier
    loc_parts = []
    if prov and prov != "-":
        loc_parts.append(prov)
    if dist and dist != "-":
        loc_parts.append(dist)

    if loc_parts:
        location_label = "_".join(loc_parts)
    else:
        lat = data.get("latitude", 0.0)
        lon = data.get("longitude", 0.0)
        location_label = f"พิกัด_{lat:.4f}_{lon:.4f}"

    raw_date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    be_date_str = to_thai_be_date_str(raw_date)
    time_stamp = datetime.now().strftime("%H%M%S")

    filename = f"รายงานพระอาทิตย์_{be_date_str}_{time_stamp}_{location_label}.md"
    safe_filename = sanitize_filename(filename)

    file_path = target_dir / safe_filename
    content = generate_markdown_content(data)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path.as_posix()

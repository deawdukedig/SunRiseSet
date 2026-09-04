"""
Thai Buddhist Era (พ.ศ.) and Gregorian (ค.ศ.) Date Processing Module.
Supports:
- Automatic conversion of Buddhist Era years (พ.ศ. >= 2400) to Gregorian (ค.ศ. = พ.ศ. - 543)
- Parsing of natural Thai date strings: e.g. "4 กันยายน 2569", "1 ม.ค. 2563", "2569-09-04"
- Formatting dates with Thai month names and Buddhist Era years.
"""

import re
from datetime import date, datetime
from typing import Optional, Union

THAI_MONTHS_FULL = {
    "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4,
    "พฤษภาคม": 5, "มิถุนายน": 6, "กรกฎาคม": 7, "สิงหาคม": 8,
    "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
}

THAI_MONTHS_ABBR = {
    "ม.ค.": 1, "ม.ค": 1, "ก.พ.": 2, "ก.พ": 2, "มี.ค.": 3, "มี.ค": 3,
    "เม.ย.": 4, "เม.ย": 4, "พ.ค.": 5, "พ.ค": 5, "มิ.ย.": 6, "มิ.ย": 6,
    "ก.ค.": 7, "ก.ค": 7, "ส.ค.": 8, "ส.ค": 8, "ก.ย.": 9, "ก.ย": 9,
    "ต.ค.": 10, "ต.ค": 10, "พ.ย.": 11, "พ.ย": 11, "ธ.ค.": 12, "ธ.ค": 12
}

MONTH_NUMBER_TO_THAI = {
    1: "มกราคม", 2: "กุมภาพันธ์", 3: "มีนาคม", 4: "เมษายน",
    5: "พฤษภาคม", 6: "มิถุนายน", 7: "กรกฎาคม", 8: "สิงหาคม",
    9: "กันยายน", 10: "ตุลาคม", 11: "พฤศจิกายน", 12: "ธันวาคม"
}

def convert_year_to_ce(year: int) -> int:
    """If year is in Buddhist Era range (>= 2400), convert to Common Era (CE = BE - 543)."""
    if year >= 2400:
        return year - 543
    return year

def parse_date_input(date_str: str) -> date:
    """
    Parse a date input string in various formats:
    - YYYY-MM-DD (e.g. '2026-09-04' or '2569-09-04')
    - DD/MM/YYYY (e.g. '04/09/2569' or '04/09/2026')
    - Natural Thai: '4 กันยายน 2569', '1 ม.ค. 2563', 'วันที่ 31 ธันวาคม 2525'
    """
    cleaned = date_str.strip()
    # Remove leading words like "วันที่", "วัน", "ปี"
    cleaned = re.sub(r'^(วันที่|วัน|เมื่อวันที่)\s*', '', cleaned).strip()

    # Pattern 1: ISO format YYYY-MM-DD
    match_iso = re.match(r'^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})$', cleaned)
    if match_iso:
        raw_year = int(match_iso.group(1))
        month = int(match_iso.group(2))
        day = int(match_iso.group(3))
        year = convert_year_to_ce(raw_year)
        return date(year, month, day)

    # Pattern 2: DD/MM/YYYY or DD-MM-YYYY
    match_dmy = re.match(r'^(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})$', cleaned)
    if match_dmy:
        day = int(match_dmy.group(1))
        month = int(match_dmy.group(2))
        raw_year = int(match_dmy.group(3))
        year = convert_year_to_ce(raw_year)
        return date(year, month, day)

    # Pattern 3: Natural Thai e.g. "4 กันยายน 2569", "4 ก.ย. 2569", "15 เม.ย. พ.ศ. 2568"
    # Optional "พ.ศ." or "ค.ศ." prefix before or after year
    thai_pattern = re.compile(r'(\d{1,2})\s+([ก-๙\.]+)\s+(?:(?:พ\.?ศ\.?|ค\.?ศ\.?|ปี)\s*)?(\d{4})')
    match_thai = thai_pattern.search(cleaned)
    if match_thai:
        day = int(match_thai.group(1))
        month_name = match_thai.group(2).strip()
        raw_year = int(match_thai.group(3))

        month = THAI_MONTHS_FULL.get(month_name) or THAI_MONTHS_ABBR.get(month_name)
        if not month:
            # Try partial matching for month
            for k, v in THAI_MONTHS_FULL.items():
                if k.startswith(month_name):
                    month = v
                    break

        if month:
            # Check if "ค.ศ." was explicitly mentioned
            if "ค.ศ." in cleaned and raw_year < 2400:
                year = raw_year
            else:
                year = convert_year_to_ce(raw_year)
            return date(year, month, day)

    raise ValueError(f"ไม่สามารถระบุวันที่ได้จาก: '{date_str}' (รองรับ เช่น '2569-09-04', '2026-09-04', '4 กันยายน 2569')")

def format_thai_date(d: date, include_ce: bool = True) -> str:
    """Format a date into Thai format with Buddhist Era (พ.ศ.) and optional CE."""
    be_year = d.year + 543
    month_name = MONTH_NUMBER_TO_THAI.get(d.month, str(d.month))
    base = f"{d.day} {month_name} พ.ศ. {be_year}"
    if include_ce:
        return f"{base} ({d.isoformat()})"
    return base

def to_thai_be_date_str(d: Union[date, datetime, str]) -> str:
    """
    Convert a date object or ISO date string (YYYY-MM-DD) to Buddhist Era YYYY-MM-DD string.
    e.g. date(2026, 9, 4) -> "2569-09-04"
    e.g. "2026-09-04" -> "2569-09-04"
    e.g. "1982-12-31" -> "2525-12-31"
    e.g. "2569-09-04" -> "2569-09-04"
    """
    if isinstance(d, (date, datetime)):
        be_year = d.year + 543 if d.year < 2400 else d.year
        return f"{be_year:04d}-{d.month:02d}-{d.day:02d}"
    elif isinstance(d, str):
        cleaned = d.strip()
        parts = cleaned.split("-")
        if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
            year = int(parts[0])
            be_year = year + 543 if year < 2400 else year
            return f"{be_year:04d}-{int(parts[1]):02d}-{int(parts[2]):02d}"
    return str(d)


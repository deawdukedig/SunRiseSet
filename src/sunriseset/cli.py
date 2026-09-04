"""
AI-Native CLI interface for SunRiseSet.
Complies with AI-Native CLI standards:
- Default structured JSON envelope: {"success": true, "data": ...}
- Standardized exit codes: 0 (Success), 1 (Input Error), 2 (Network/Upstream Error), 3 (Unexpected)
- Human-friendly view with --human flag
- Clean stdout / stderr separation (diagnostics go to stderr)
- Self-description with --brief and --version
"""

import sys
import json
import logging
import argparse
from datetime import datetime, date
from typing import Optional

from .models import Coordinates, EnvelopeResponse
from .geocoding import reverse_geocode, forward_geocode
from .ephemeris import get_solar_times
from .reporter import save_report, DEFAULT_REPORT_DIR
from .thai_date import parse_date_input, format_thai_date

__version__ = "2.0.0"

# Configure console encoding for Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr
    )

def print_human_output(data: dict):
    addr = data.get("address", {})
    print("==================================================")
    print("☀️ ข้อมูลพระอาทิตย์ขึ้น-ตก (Sunrise & Sunset)")
    print("==================================================")
    print(f"📍 พิกัด (Lat, Lon): {data['latitude']:.4f}, {data['longitude']:.4f}")
    print(f"🗺️ Google Maps: {data['google_maps_url']}")
    if addr:
        print("--------------------------------------------------")
        print("🏢 ข้อมูลสถานที่และที่อยู่ (Address Breakdown):")
        print(f"  • ถนน:         {addr.get('road', '-')}")
        print(f"  • ตำบล/แขวง:   {addr.get('subdistrict', '-')}")
        print(f"  • อำเภอ/เขต:    {addr.get('district', '-')}")
        print(f"  • จังหวัด:      {addr.get('province', '-')}")
        print(f"  • ประเทศ:      {addr.get('country', '-')}")
        if addr.get('postcode') and addr.get('postcode') != '-':
            print(f"  • รหัสไปรษณีย์: {addr.get('postcode')}")
        print(f"  • ที่อยู่เต็ม:   {addr.get('full_address', '-')}")
        print("--------------------------------------------------")
    print(f"📅 วันที่: {data.get('date_thai') or data['date']}")
    print(f"🕒 เขตเวลา (Timezone): {data.get('timezone')} ({data.get('gmt_offset', data.get('timezone_abbreviation'))})")
    print(f"🌅 พระอาทิตย์ขึ้น (Sunrise): {data['sunrise']} (เวลาท้องถิ่น)")
    print(f"🌇 พระอาทิตย์ตก (Sunset):  {data['sunset']} (เวลาท้องถิ่น)")
    if data.get("solar_noon"):
        print(f"☀️ เที่ยงวันสุริยะ: {data['solar_noon']} (เวลาท้องถิ่น)")
    print(f"⏱️ ความยาวกลางวัน: {data['daylight_duration_text']}")
    print(f"📡 แหล่งข้อมูล: {data['source']} {'(แคช)' if data.get('cached') else ''}")
    if data.get("report_path"):
        print(f"📁 บันทึกรายงานแล้วที่: {data['report_path']}")
    print("==================================================")

def run(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sunriseset",
        description="SunRiseSet: High-precision Solar Ephemeris & Thai Geocoding CLI"
    )
    parser.add_argument("--lat", type=float, default=None, help="Latitude (-90.0 to 90.0)")
    parser.add_argument("--lon", type=float, default=None, help="Longitude (-180.0 to 180.0)")
    parser.add_argument("--location", "--query", "-q", type=str, default=None,
                        help="Thai location search query (ถนน ตำบล อำเภอ จังหวัด)")
    parser.add_argument("--date", "-d", type=str, default=None,
                        help="Target date (supports YYYY-MM-DD, e.g. 2026-09-04, Buddhist Era e.g. 2569-09-04 or '4 กันยายน 2569', default: today)")
    parser.add_argument("--human", action="store_true",
                        help="Output human-friendly formatted text instead of JSON")
    parser.add_argument("--json", action="store_true", default=False,
                        help="Output JSON (enabled by default unless --human is set)")
    parser.add_argument("--no-cache", action="store_true",
                        help="Bypass local SQLite cache and force live lookup")
    parser.add_argument("--report-dir", type=str, default=DEFAULT_REPORT_DIR,
                        help="Directory to save UTF-8 Markdown reports (default: report)")
    parser.add_argument("--no-report", action="store_true",
                        help="Disable automatic report generation in report/ directory")
    parser.add_argument("--brief", action="store_true",
                        help="Show brief machine card for AI agents")
    parser.add_argument("--version", "-v", action="version", version=f"sunriseset {__version__}")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose debug logs on stderr")

    args = parser.parse_args(argv)
    setup_logging(args.verbose)

    if args.brief:
        brief_info = {
            "name": "sunriseset",
            "version": __version__,
            "description": "Calculates local sunrise/sunset, GMT offset, Google Maps URL, and Thai address hierarchy.",
            "inputs": ["--lat and --lon", "--location <Thai text query>"],
            "output": "Standard JSON envelope with success, data, or error"
        }
        print(json.dumps(brief_info, ensure_ascii=False, indent=2))
        return 0

    # Parse target date
    target_date = date.today()
    if args.date:
        try:
            target_date = parse_date_input(args.date)
        except ValueError as e:
            err = EnvelopeResponse(
                success=False,
                error={"code": "INVALID_DATE", "message": str(e)}
            )
            if args.human:
                print(f"Error: {err.error['message']}", file=sys.stderr)
            else:
                print(json.dumps(err.to_dict(), ensure_ascii=False, indent=2))
            return 1

    # Resolve Coordinates & Address
    coords = None
    addr_info = None
    use_cache = not args.no_cache

    try:
        if args.location:
            coords, addr_info = forward_geocode(args.location, use_cache=use_cache)
        elif args.lat is not None and args.lon is not None:
            coords = Coordinates(latitude=args.lat, longitude=args.lon)
            addr_info = reverse_geocode(coords.latitude, coords.longitude, use_cache=use_cache)
        else:
            err = EnvelopeResponse(
                success=False,
                error={"code": "MISSING_ARGUMENTS", "message": "ต้องระบุ --lat และ --lon หรือระบุ --location"}
            )
            if args.human:
                print(f"Error: {err.error['message']}", file=sys.stderr)
            else:
                print(json.dumps(err.to_dict(), ensure_ascii=False, indent=2))
            return 1
    except (ValueError, TypeError) as e:
        err = EnvelopeResponse(
            success=False,
            error={"code": "INVALID_INPUT", "message": str(e)}
        )
        if args.human:
            print(f"Input Error: {e}", file=sys.stderr)
        else:
            print(json.dumps(err.to_dict(), ensure_ascii=False, indent=2))
        return 1
    except ConnectionError as e:
        err = EnvelopeResponse(
            success=False,
            error={"code": "UPSTREAM_NETWORK_ERROR", "message": str(e)}
        )
        if args.human:
            print(f"Network Error: {e}", file=sys.stderr)
        else:
            print(json.dumps(err.to_dict(), ensure_ascii=False, indent=2))
        return 2

    # Calculate Solar Events
    try:
        solar_res = get_solar_times(coords, target_date, use_cache=use_cache)
        solar_res.address = addr_info
        solar_res.date_thai = format_thai_date(target_date)
        res_dict = solar_res.to_dict()

        # Automatically save report to report/ directory
        if not args.no_report:
            try:
                saved_report_path = save_report(res_dict, output_dir=args.report_dir)
                res_dict["report_path"] = saved_report_path
            except Exception as e:
                logging.warning(f"Could not automatically save report: {e}")

        if args.human:
            print_human_output(res_dict)
        else:
            # Default envelope
            resp = EnvelopeResponse(success=True, data=res_dict)
            print(json.dumps(resp.to_dict(), ensure_ascii=False, indent=2))
        return 0
    except Exception as e:
        err = EnvelopeResponse(
            success=False,
            error={"code": "UNEXPECTED_ERROR", "message": str(e)}
        )
        if args.human:
            print(f"Unexpected Error: {e}", file=sys.stderr)
        else:
            print(json.dumps(err.to_dict(), ensure_ascii=False, indent=2))
        return 3

def main():
    sys.exit(run())

if __name__ == "__main__":
    main()

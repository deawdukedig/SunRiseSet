# ☀️ SunRiseSet — Antigravity Agent Harness
### High-Precision Solar Ephemeris & Thai Administrative Geocoding System

[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-47%20passed-success.svg)](tests/)
[![Technical Docs](https://img.shields.io/badge/docs-OVERVIEW.md-informational.svg)](OVERVIEW.md)
[![OS Independent](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-brightgreen.svg)](README.md)
[![UTF-8](https://img.shields.io/badge/encoding-UTF--8%20100%25-orange.svg)](README.md)

> [!IMPORTANT]
> **ระบบนี้ถูกออกแบบมาเพื่อให้ผู้ใช้เรียกใช้งานผ่าน Google Antigravity Desktop และ Antigravity CLI (`agy`) เป็นหลัก**  
> ผู้ใช้งานสามารถสนทนาถาม-ตอบเป็นภาษาไทยกับ AI Agent ผ่านหน้าต่างแชทของ Antigravity โดยตรง โดย Agent จะจัดการเรียกเครื่องมือคำนวณเวลาสุริยะ ดึงข้อมูลเขตเวลา GMT สร้างลิงก์ Google Maps ปักหมุดพิกัด แจกแจงโครงสร้างที่อยู่ไทย และบันทึกรายงานผลสรุปเป็นไฟล์ Markdown ภาษาไทย (UTF-8) ลงในไดเรกทอรี `report/` ให้โดยอัตโนมัติ

---

## 📑 สารบัญ (Table of Contents)

- [1. ระบบนี้คืออะไรและทำอะไรได้บ้าง (Overview)](#1-ระบบนี้คืออะไรและทำอะไรได้บ้าง-overview)
- [2. ความสามารถเด่นของระบบ (Key Capabilities)](#2-ความสามารถเด่นของระบบ-key-capabilities)
- [3. วิธีการติดตั้งและเริ่มใช้งาน (Installation & Setup)](#3-วิธีการติดตั้งและเริ่มใช้งาน-installation--setup)
  - [วิธีที่ 1: ใช้งานผ่าน Antigravity Desktop (IDE & Desktop App)](#วิธีที่-1-ใช้งานผ่าน-antigravity-desktop-ide--desktop-app)
  - [วิธีที่ 2: ใช้งานผ่าน Antigravity CLI (`agy`)](#วิธีที่-2-ใช้งานผ่าน-antigravity-cli-agy)
  - [วิธีที่ 3: เรียกใช้งานผ่าน CLI Tool โดยตรง](#วิธีที่-3-เรียกใช้งานผ่าน-cli-tool-โดยตรง)
- [4. ตัวอย่างการใช้งานจริงใน Antigravity (Usage Examples)](#4-ตัวอย่างการใช้งานจริงใน-antigravity-usage-examples)
  - [🔹 ตัวอย่างที่ 1: สอบถามด้วยพิกัดตัวเลข (Lat, Lon)](#🔹-ตัวอย่างที่-1-สอบถามด้วยพิกัดตัวเลข-lat-lon)
  - [🔹 ตัวอย่างที่ 2: สอบถามด้วยชื่อสถานที่ / ที่อยู่ไทย](#🔹-ตัวอย่างที่-2-สอบถามด้วยชื่อสถานที่--ถนน-ตำบล-อำเภอ-จังหวัด)
  - [🔹 ตัวอย่างที่ 3: สอบถามด้วยปี พ.ศ. หรือภาษาไทยธรรมชาติ](#🔹-ตัวอย่างที่-3-สอบถามด้วยปี-พศ-หรือภาษาไทยธรรมชาติ)
  - [🔹 ตัวอย่างที่ 4: สอบถามข้อมูลประวัติศาสตร์ในอดีต (Historical Dates)](#🔹-ตัวอย่างที่-4-สอบถามข้อมูลประวัติศาสตร์ในอดีต-historical-dates)
  - [🔹 ตัวอย่างที่ 5: เรียกผ่าน AI-Native CLI Envelope (สำหรับโปรแกรม/สคริปต์)](#🔹-ตัวอย่างที่-5-เรียกผ่าน-ai-native-cli-envelope-สำหรับโปรแกรมสคริปต์)
- [5. ตัวอย่างรายงานผลอัตโนมัติ (Sample Report)](#5-ตัวอย่างรายงานผลอัตโนมัติ-sample-report)
- [6. โครงสร้างระบบ (System Architecture)](#6-โครงสร้างระบบ-system-architecture)
- [7. การทดสอบและรับประกันคุณภาพ (Testing & Quality Assurance)](#7-การทดสอบและรับประกันคุณภาพ-testing--quality-assurance)
- [8. เอกสารเชิงเทคนิคเพื่อการศึกษา (Technical Architecture Overview)](#8-เอกสารเชิงเทคนิคเพื่อการศึกษา-technical-architecture-overview)
- [9. ใบอนุญาต (License)](#9-ใบอนุญาต-license)

---

## 1. ระบบนี้คืออะไรและทำอะไรได้บ้าง (Overview)

**SunRiseSet** เป็น Production-grade AI Agent Harness ที่พัฒนาขึ้นสำหรับแพลตฟอร์ม **Google Antigravity** โดยทำหน้าที่เป็นเครื่องมืออัจฉริยะในการ:
1. **คำนวณเวลาพระอาทิตย์ขึ้น (Sunrise) พระอาทิตย์ตก (Sunset) และเที่ยงวันสุริยะ (Solar Noon)** ด้วยความแม่นยำสูงระดับนาที
2. **แปลงเวลาเป็นเวลาท้องถิ่นจริง (Local Time)** ของพิกัดนั้น พร้อมระบุเขตเวลาสากล เช่น `Asia/Bangkok (GMT+7)`
3. **แปลงพิกัดภูมิศาสตร์และที่อยู่ไทย 2 ทาง (Forward & Reverse Geocoding)** เพื่อแจกแจงโครงสร้างตามการปกครองของไทย (**ถนน, ตำบล/แขวง, อำเภอ/เขต, จังหวัด, ประเทศ และรหัสไปรษณีย์**)
4. **สร้างลิงก์ Google Maps ตรงพิกัด** ช่วยให้ผู้ใช้สามารถคลิกเปิดดูแผนที่ดาวเทียมได้ทันที
5. **รองรับปฏิทินไทย (พุทธศักราช / พ.ศ.) ควบคู่กับสากล (คริสต์ศักราช / ค.ศ.)** รองรับทั้งวันปัจจุบัน วันล่วงหน้าในอนาคต และวันประวัติศาสตร์ย้อนหลังหลายร้อยปี
6. **สร้างและบันทึกรายงานสรุปผลอัตโนมัติ (Automatic Markdown Reporter)** จัดเก็บลงไดเรกทอรี `report/` ในรูปแบบ UTF-8 ทั้งชื่อไฟล์ (ระบุปี พ.ศ.) และเนื้อหาภายใน

---

## 2. ความสามารถเด่นของระบบ (Key Capabilities)

- 🤖 **สนทนาภาษาไทยผ่าน Antigravity 100%**: ถาม-ตอบภาษาไทยได้อย่างเป็นธรรมชาติกับ AI Agent ไม่ต้องเขียนโค้ดหรือจำคำสั่ง
- ☀️ **คำนวณเที่ยงวันสุริยะ (Solar Noon) แม่นยำทุกพิกัด**: ระบุเวลาที่ดวงอาทิตย์ทำมุมเงยสูงสุดบนท้องฟ้าของแต่ละพื้นที่แบบอัตโนมัติ ทั้งโหมดออนไลน์และออฟไลน์
- 📅 **รองรับปี พ.ศ. และ ค.ศ. ทุกรูปแบบ**:
  - รองรับ ISO ด้วยปี พ.ศ. เช่น `2569-09-04` หรือ DMY เช่น `04/09/2569`
  - รองรับข้อความภาษาไทยธรรมชาติ เช่น `"4 กันยายน 2569"`, `"วันที่ 31 ธันวาคม 2525"`, `"1 ม.ค. 2563"`
  - คำนวณปีอธิกสุรทิน (Leap Year) ของ พ.ศ. ได้อย่างถูกต้อง เช่น `29 ก.พ. 2567` (ค.ศ. 2024)
- 🕰️ **คำนวณวันในอดีตได้ไม่จำกัด (Historical Ephemeris)**:
  - **ปี พ.ศ. 2483 ถึงปัจจุบัน (1940+)**: ดึงข้อมูลสภาพอากาศและสุริยะจาก Open-Meteo Historical Archive API
  - **ก่อนปี พ.ศ. 2483 (เช่น วันตั้งกรุงรัตนโกสินทร์ พ.ศ. 2325)**: สลับสู่อัลกอริทึมดาราศาสตร์สากล **NOAA Solar Calculation Algorithm (Offline)** อัตโนมัติโดยไม่มีการล่ม
- 🏢 **แจกแจงโครงสร้างที่อยู่ไทยครบทุกระดับชั้น**:
  - 🛣️ **ถนน (Road)**
  - 🏡 **ตำบล / แขวง (Subdistrict / Tambon)**
  - 🏛️ **อำเภอ / เขต (District / Amphoe)**
  - 🏙️ **จังหวัด (Province / Changwat)**
  - 📮 **รหัสไปรษณีย์ (Postcode)** และประเทศ
- 🗺️ **ลิงก์ปักหมุด Google Maps**: คลิกเปิดตำแหน่งจริงบน Google Maps ได้ทันทีจากข้อความแชท
- 📁 **ระบบบันทึกรายงานอัตโนมัติ (Auto-Save UTF-8 Report)**:
  - สรุปผลเป็นไฟล์ Markdown ภาษาไทยทุกครั้งที่มีการคำนวณ
  - ชื่อไฟล์ระบุปี พ.ศ. วันที่ เวลา และสถานที่ เช่น `รายงานพระอาทิตย์_2569-09-04_162617_กรุงเทพมหานคร_พระนคร.md`
  - เข้ารหัส **UTF-8 100%** ทั้งชื่อไฟล์และเนื้อหา ปลอดภัยบนทุกระบบปฏิบัติการ
- ⚡ **ความเร็วสูงระดับ Production ด้วย SQLite Persistent Caching**:
  - ตอบสนองในเวลา **< 20 มิลลิวินาที** เมื่อมีข้อมูลในแคช
  - ป้องกันการยิง API ซ้ำซ้อน และทำงานแบบ Thread-safe ด้วย WAL mode
- 🌐 **100% OS-Independent**:
  - ทำงานสมบูรณ์แบบทั้งบน **Windows, macOS และ Linux**
  - ใช้มาตรฐาน POSIX Forward Slash ในการจัดการ Path ป้องกันปัญหา Escape Backslash ล้มเหลว

---

## 3. วิธีการติดตั้งและเริ่มใช้งาน (Installation & Setup)

เลือกลักษณะการเปิดใช้งานตามเครื่องมือ Antigravity ที่คุณใช้งาน:

### วิธีที่ 1: ใช้งานผ่าน Antigravity Desktop (IDE & Desktop App)

1. **เปิดโปรเจกต์ใน Antigravity Desktop**:
   - เปิดโปรแกรม **Google Antigravity Desktop**
   - ไปที่เมนู `File` > `Open Folder...` แล้วเลือกโฟลเดอร์:
     ```text
     C:\gemini_code\SunRiseSet
     ```
2. **ติดตั้งไลบรารีของโปรเจกต์ (ดำเนินการครั้งแรก)**:
   - เปิดแถบ **Terminal** (`Ctrl + ~`) ด้านล่างของ Antigravity Desktop แล้วรันคำสั่ง:
     ```powershell
     pip install -e .
     ```
3. **เริ่มต้นใช้งาน**:
   - Antigravity จะตรวจพบไฟล์ข้อกำหนด [AGENTS.md](AGENTS.md) และสกิล [SKILL.md](.agents/skills/sunriseset/SKILL.md) โดยอัตโนมัติ
   - เริ่มต้นพิมพ์คำถามภาษาไทยในช่องแชทด้านขวา (Chat Canvas / Agent Panel) ได้ทันที!

---

### วิธีที่ 2: ใช้งานผ่าน Antigravity CLI (`agy`)

1. **เปิด PowerShell หรือ Command Prompt**:
   - เข้าไปยังโฟลเดอร์โปรเจกต์:
     ```powershell
     cd C:\gemini_code\SunRiseSet
     ```
2. **ติดตั้งไลบรารีของโปรเจกต์ (ดำเนินการครั้งแรก)**:
   ```powershell
   pip install -e .
   ```
3. **เรียกใช้งาน Antigravity CLI**:
   ```powershell
   agy
   ```
4. **เริ่มต้นสนทนา**:
   - หน้าต่างแชทของ Antigravity CLI จะเปิดขึ้นมา พร้อมโหลดกฎของ Agent
   - สามารถพิมพ์สอบถามข้อมูลเวลาพระอาทิตย์ขึ้น-ตกได้ทันที

---

### วิธีที่ 3: เรียกใช้งานผ่าน CLI Tool โดยตรง

สำหรับผู้ที่ต้องการนำไปใช้ใน Automated Pipeline, Cron job, หรือ Shell Script สามารถรันผ่านคำสั่ง Python ได้โดยตรง:

```powershell
# ค้นหาด้วยพิกัด แสดงผลแบบมนุษย์อ่าน
python tools/solar_calc.py --lat 13.7563 --lon 100.5018 --human

# ค้นหาด้วยชื่อสถานที่ ระบุวันที่เป็นปี พ.ศ.
python tools/solar_calc.py --location "เสาชิงช้า พระนคร" --date "2569-09-04" --human

# รับข้อมูลแบบ JSON Envelope สำหรับโปรแกรมภายนอก
python tools/solar_calc.py --location "เชียงใหม่" --date "4 กันยายน 2569"
```

---

## 4. ตัวอย่างการใช้งานจริงใน Antigravity (Usage Examples)

เพียงพิมพ์ข้อความภาษาไทยลงในช่องแชทของ Antigravity Agent:

### 🔹 ตัวอย่างที่ 1: สอบถามด้วยพิกัดตัวเลข (Lat, Lon)
> **ผู้ใช้**: `"ขอเวลาพระอาทิตย์ขึ้น-ตก ที่พิกัด 13.7563, 100.5018 วันนี้หน่อย"`

**Antigravity Agent จะตอบกลับทันที:**

```markdown
### ☀️ ข้อมูลเวลาพระอาทิตย์ขึ้น-ตก (Sunrise & Sunset)

**🏢 ข้อมูลสถานที่และตำแหน่ง:**
- **ถนน**: วงเวียนอนุสาวรีย์ประชาธิปไตย
- **ตำบล / แขวง**: แขวงบวรนิเวศ
- **อำเภอ / เขต**: เขตพระนคร
- **จังหวัด**: กรุงเทพมหานคร
- **ประเทศ**: ประเทศไทย (รหัสไปรษณีย์ 10200)
- **พิกัด (Lat, Lon)**: `13.756300, 100.501800`
- **แผนที่ Google Maps**: 🗺️ [คลิกเพื่อเปิดดูพิกัดบน Google Maps](https://www.google.com/maps?q=13.756300,100.501800)

---

**⏰ ข้อมูลเวลาสุริยะและเขตเวลา (Local Time):**
- **วันที่**: 4 กันยายน พ.ศ. 2569 (2026-09-04)
- **เขตเวลา (Timezone)**: `Asia/Bangkok` (**`GMT+7`**)

| รายการ | เวลาท้องถิ่น | รายละเอียด |
| :--- | :---: | :--- |
| 🌅 **พระอาทิตย์ขึ้น (Sunrise)** | **`06:06` น.** | แสงแรกของวัน ณ พิกัดนี้ |
| ☀️ **เที่ยงวันสุริยะ (Solar Noon)** | **`12:16` น.** | จุดที่ดวงอาทิตย์อยู่ตำแหน่งสูงสุดบนท้องฟ้า (ทำมุมเงยสูงสุด) |
| 🌇 **พระอาทิตย์ตก (Sunset)** | **`18:27` น.** | แสงสุดท้ายของวัน ณ พิกัดนี้ |
| ⏱️ **ความยาวช่วงเวลากลางวัน** | **`12 ชั่วโมง 21 นาที`** | ระยะเวลาที่ดวงอาทิตย์อยู่เหนือขอบฟ้า |

> [!NOTE]
> เวลาทั้งหมดถูกแปลงเป็นเวลาท้องถิ่นของพื้นที่ (`GMT+7`) เรียบร้อยแล้ว

📁 **บันทึกรายงานอัตโนมัติแล้วที่**: `report/รายงานพระอาทิตย์_2569-09-04_154743_กรุงเทพมหานคร_พระนคร.md`
```

---

### 🔹 ตัวอย่างที่ 2: สอบถามด้วยชื่อสถานที่ / ถนน ตำบล อำเภอ จังหวัด
> **ผู้ใช้**: `"ถนนสุขุมวิท พัทยา พระอาทิตย์ตกกี่โมง"`

```markdown
### ☀️ ข้อมูลเวลาพระอาทิตย์ขึ้น-ตก (Sunrise & Sunset)

**🏢 ข้อมูลสถานที่และตำแหน่ง:**
- **ถนน**: ถนนสุขุมวิท
- **ตำบล / แขวง**: ตำบลนาเกลือ
- **อำเภอ / เขต**: อำเภอบางละมุง
- **จังหวัด**: จังหวัดชลบุรี
- **ประเทศ**: ประเทศไทย (รหัสไปรษณีย์ 20150)
- **พิกัด (Lat, Lon)**: `12.966865, 100.910357`
- **แผนที่ Google Maps**: 🗺️ [คลิกเพื่อเปิดดูพิกัดบน Google Maps](https://www.google.com/maps?q=12.966865,100.910357)

---

**⏰ ข้อมูลเวลาสุริยะและเขตเวลา (Local Time):**
- **วันที่**: 4 กันยายน พ.ศ. 2569 (2026-09-04)
- **เขตเวลา (Timezone)**: `Asia/Bangkok` (**`GMT+7`**)

| รายการ | เวลาท้องถิ่น | รายละเอียด |
| :--- | :---: | :--- |
| 🌅 **พระอาทิตย์ขึ้น (Sunrise)** | **`06:05` น.** | แสงแรกของวัน ณ พิกัดนี้ |
| ☀️ **เที่ยงวันสุริยะ (Solar Noon)** | **`12:15` น.** | จุดที่ดวงอาทิตย์อยู่ตำแหน่งสูงสุดบนท้องฟ้า (ทำมุมเงยสูงสุด) |
| 🌇 **พระอาทิตย์ตก (Sunset)** | **`18:25` น.** | แสงสุดท้ายของวัน ณ พิกัดนี้ |
| ⏱️ **ความยาวช่วงเวลากลางวัน** | **`12 ชั่วโมง 20 นาที`** | ระยะเวลาที่ดวงอาทิตย์อยู่เหนือขอบฟ้า |

📁 **บันทึกรายงานอัตโนมัติแล้วที่**: `report/รายงานพระอาทิตย์_2569-09-04_153527_ชลบุรี_บางละมุง.md`
```

---

### 🔹 ตัวอย่างที่ 3: สอบถามด้วยปี พ.ศ. หรือภาษาไทยธรรมชาติ
> **ผู้ใช้**: `"เชียงใหม่ วันที่ 4 กันยายน 2569 พระอาทิตย์ขึ้นกี่โมง"`

Agent จะทำการแปลงวันที่ปี พ.ศ. คำนวณเวลาสุริยะของวันดังกล่าว และบันทึกรายงานที่มีชื่อไฟล์เป็นปี พ.ศ. เช่น `report/รายงานพระอาทิตย์_2569-09-04_161809_เชียงใหม่_เมืองเชียงใหม่.md` ให้อัตโนมัติ

---

### 🔹 ตัวอย่างที่ 4: สอบถามข้อมูลประวัติศาสตร์ในอดีต (Historical Dates)
> **ผู้ใช้**: `"เสาชิงช้า พระนคร วันที่ 31 ธันวาคม 2525 พระอาทิตย์ขึ้นกี่โมง"`

ระบบจะแปลงปี พ.ศ. 2525 เป็น ค.ศ. 1982 ดึงข้อมูลย้อนหลังจาก Historical Archive API และสร้างไฟล์รายงาน `report/รายงานพระอาทิตย์_2525-12-31_162627_กรุงเทพมหานคร_พระนคร.md` ทันที

---

### 🔹 ตัวอย่างที่ 5: เรียกผ่าน AI-Native CLI Envelope (สำหรับโปรแกรม/สคริปต์)
```powershell
python tools/solar_calc.py --lat 13.7563 --lon 100.5018 --date "2569-09-04"
```

**ตัวอย่าง JSON Response Envelope (`Exit Code 0`):**
```json
{
  "success": true,
  "data": {
    "date": "2026-09-04",
    "date_thai": "4 กันยายน พ.ศ. 2569 (2026-09-04)",
    "latitude": 13.7563,
    "longitude": 100.5018,
    "timezone": "Asia/Bangkok",
    "timezone_abbreviation": "GMT+7",
    "gmt_offset": "GMT+7",
    "utc_offset_seconds": 25200,
    "sunrise": "06:06",
    "sunset": "18:27",
    "solar_noon": "12:16",
    "daylight_duration_text": "12 ชั่วโมง 21 นาที",
    "daylight_duration_seconds": 44463.44,
    "google_maps_url": "https://www.google.com/maps?q=13.756300,100.501800",
    "address": {
      "road": "วงเวียนอนุสาวรีย์ประชาธิปไตย",
      "subdistrict": "แขวงบวรนิเวศ",
      "district": "เขตพระนคร",
      "province": "กรุงเทพมหานคร",
      "postcode": "10200",
      "country": "ประเทศไทย",
      "full_address": "วงเวียนอนุสาวรีย์ประชาธิปไตย, แขวงบวรนิเวศ, เขตพระนคร, กรุงเทพมหานคร, 10200, ประเทศไทย"
    },
    "source": "Open-Meteo API (Online)",
    "cached": true,
    "report_path": "report/รายงานพระอาทิตย์_2569-09-04_154743_กรุงเทพมหานคร_พระนคร.md"
  },
  "error": null
}
```

---

## 5. ตัวอย่างรายงานผลอัตโนมัติ (Sample Report)

ทุกครั้งที่ประมวลผล ระบบจะสร้างไฟล์รายงาน Markdown ภาษาไทยลงในโฟลเดอร์ `report/` โดยอัตโนมัติ (เช่น [`รายงานพระอาทิตย์_2569-09-04_162617_กรุงเทพมหานคร_พระนคร.md`](report/))

ตัวอย่างเนื้อหาจริงภายในไฟล์รายงาน:

````markdown
# ☀️ รายงานข้อมูลเวลาพระอาทิตย์ขึ้น-ตก (Solar Ephemeris Report)

> **สร้างเมื่อวันที่-เวลา**: `2026-09-04 16:26:17`  
> **ระบบประมวลผล**: `SunRiseSet Production Engine v2.0`  
> **แหล่งข้อมูล**: `Open-Meteo API (Online) (แคช)`

---

## 📍 ข้อมูลตำแหน่งและเขตการปกครอง

| รายการ | ข้อมูล |
| :--- | :--- |
| **ถนน (Road)** | ถนนบำรุงเมือง |
| **ตำบล / แขวง (Subdistrict)** | แขวงวัดราชบพิธ |
| **อำเภอ / เขต (District)** | เขตพระนคร |
| **จังหวัด (Province)** | กรุงเทพมหานคร |
| **รหัสไปรษณีย์ (Postcode)** | 10200 |
| **ประเทศ (Country)** | ประเทศไทย |
| **พิกัด (Latitude, Longitude)** | `13.751814, 100.501278` |
| **แผนที่ Google Maps** | [คลิกเพื่อเปิดดูพิกัดบน Google Maps](https://www.google.com/maps?q=13.751814,100.501278) |
| **ที่อยู่เต็ม (Full Address)** | เสาชิงช้า, ถนนบำรุงเมือง, ชุมชนตรอกวิสูตร, แขวงวัดราชบพิธ, เขตพระนคร, กรุงเทพมหานคร, 10200, ประเทศไทย |

---

## ⏰ ข้อมูลเวลาสุริยะและดาราศาสตร์ (Local Time)

- **วันที่คำนวณ**: `4 กันยายน พ.ศ. 2569 (2026-09-04)`
- **เขตเวลา (Timezone)**: `Asia/Bangkok` (**`GMT+7`**)
- **UTC Offset (วินาที)**: `25200`

| ปรากฏการณ์ | เวลาท้องถิ่น | รายละเอียด |
| :--- | :---: | :--- |
| 🌅 **พระอาทิตย์ขึ้น (Sunrise)** | **`06:06` น.** | แสงแรกของวัน ณ ขอบฟ้าท้องถิ่น |
| ☀️ **เที่ยงวันสุริยะ (Solar Noon)** | **`12:16` น.** | จุดที่ดวงอาทิตย์อยู่ตำแหน่งสูงสุดบนท้องฟ้า |
| 🌇 **พระอาทิตย์ตก (Sunset)** | **`18:27` น.** | แสงสุดท้ายของวัน ณ ขอบฟ้าท้องถิ่น |
| ⏱️ **ความยาวช่วงเวลากลางวัน** | **`12 ชั่วโมง 21 นาที`** | ระยะเวลาที่ดวงอาทิตย์อยู่เหนือขอบฟ้า |

> [!NOTE]
> เวลาทั้งหมดถูกแปลงเป็นเวลาท้องถิ่นของพื้นที่ (`GMT+7`) เรียบร้อยแล้ว

---
*สร้างรายงานอัตโนมัติโดย SunRiseSet — Thai Solar Ephemeris & Geocoding System*
````

---

## 6. โครงสร้างระบบ (System Architecture)

```text
SunRiseSet/
├── .agents/skills/sunriseset/  # Antigravity Skill Registration
│   └── SKILL.md                # คำสั่งและรูปแบบการทำงานของ Agent
├── .github/workflows/
│   └── ci.yml                  # Multi-OS & Multi-Python CI Matrix
├── .gitattributes              # Line Ending Normalization (LF)
├── .gitignore                  # Git Ignore Rules
├── AGENTS.md                   # กฎและ Operating Contract ของ Agent
├── OVERVIEW.md                 # เอกสารอธิบายการทำงานเชิงเทคนิคและอัลกอริทึมเพื่อการศึกษา
├── README.md                   # เอกสารแนะนำการใช้งานฉบับสมบูรณ์
├── LICENSE                     # MIT License
├── pyproject.toml              # Build & Packaging Spec (PEP 517/518/621)
├── src/sunriseset/             # Core Execution Engine
│   ├── __init__.py             # Public Module Exports
│   ├── models.py               # Strongly-typed Dataclasses & Validations
│   ├── ephemeris.py            # Astronomical Engine (Open-Meteo + NOAA)
│   ├── geocoding.py            # Thai Administrative Geocoder (OSM Nominatim)
│   ├── cache.py                # Thread-safe SQLite Persistent Cache
│   ├── reporter.py             # Automatic UTF-8 Report Generator
│   ├── thai_date.py            # Thai Buddhist Era & Natural Date Parser
│   └── cli.py                  # AI-Native CLI with JSON Envelope
├── tools/
│   └── solar_calc.py           # CLI Wrapper สำหรับ Agent และ Script
├── report/                     # ไดเรกทอรีเก็บรายงานผลอัตโนมัติ (UTF-8)
│   └── .gitkeep
└── tests/                      # 47 Automated Unit & Benchmark Tests
    ├── audit_paths.py          # ตรวจสอบความถูกต้องของลิงก์และ Path ทั้งหมด
    ├── test_models.py          # ทดสอบ Data validation และ models
    ├── test_cache.py           # ทดสอบ SQLite cache & TTL
    ├── test_geocoding.py       # ทดสอบ Reverse & Forward geocoding
    ├── test_ephemeris.py       # ทดสอบการคำนวณสุริยะและเวลาท้องถิ่น
    ├── test_thai_date.py       # ทดสอบการแปลงปี พ.ศ. และภาษาไทยธรรมชาติ
    ├── test_reporter.py        # ทดสอบการสร้างไฟล์รายงานและ UTF-8 encoding
    ├── test_cli.py             # ทดสอบ CLI exit codes และ JSON envelope
    ├── test_solar_calc.py      # ทดสอบ Backward-compatible wrapper
    └── test_benchmark.py       # ทดสอบประสิทธิภาพความเร็วในการทำงาน
```

---

## 7. การทดสอบและรับประกันคุณภาพ (Testing & Quality Assurance)

ระบบมาพร้อมชุดทดสอบอัตโนมัติ **47 รายการ** ครอบคลุมการทำงานทุกส่วน ทั้ง Unit Tests, Fault Injection, Caching, และ Benchmark:

```powershell
python -m unittest discover tests
```

**ผลลัพธ์การทดสอบ:**
```text
Ran 47 tests in 0.35s — OK (ผ่านการทดสอบ 100%)
```

และสามารถรันสคริปต์ตรวจเช็คความถูกต้องของ Path, Import, ลิงก์ Markdown ทั้งหมดในโปรเจกต์ได้ด้วย:
```powershell
python tests/audit_paths.py
```

---

## 8. เอกสารเชิงเทคนิคเพื่อการศึกษา (Technical Architecture Overview)

สำหรับผู้ที่ต้องการศึกษาการทำงานเชิงลึกของระบบ คณิตศาสตร์ทางดาราศาสตร์ หรือการออกแบบ Agent Harness สามารถศึกษาเพิ่มเติมได้จากเอกสาร:

👉 **[📘 OVERVIEW.md — Technical Architecture & Engineering Overview](OVERVIEW.md)**

**หัวข้อที่มีในเอกสารเชิงลึก:**
1. สถาปัตยกรรมระดับภาพรวมและการแบ่งเลเยอร์ (Layered Architecture & Separation of Concerns)
2. คณิตศาสตร์และสมการดาราศาสตร์สุริยะ (NOAA / Jean Meeus Astronomical Algorithms)
3. ตรรกะการแปลงที่อยู่ไทย 5 ระดับจาก OpenStreetMap (Thai Administrative Geocoding)
4. การคำนวณและประมวลผลปฏิทินพุทธศักราช (พ.ศ.) ควบคู่ปีอธิกสุรทิน (Leap Year)
5. การออกแบบฐานข้อมูลแคชความเร็วสูงระดับไมโครวินาที (SQLite WAL Mode)
6. ความเข้ากันได้ข้ามระบบปฏิบัติการและการป้องกันข้อผิดพลาดของ Path
7. ข้อกำหนดสัญญา AI-Native CLI Envelope และ Error Taxonomy

---

## 9. ใบอนุญาต (License)

โปรเจกต์นี้เผยแพร่ภายใต้ใบอนุญาต **[MIT License](LICENSE)** สามารถนำไปใช้งาน พัฒนาต่อยอด หรือประยุกต์ใช้ในองค์กรได้อย่างอิสระ

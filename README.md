# 🌸 ร้านขายดอกไม้ (Flowers Store) - ฐานข้อมูล SQLite

## 📦 ไฟล์ที่สร้างขึ้น

### 1. **flowers_store.db** ✅
   - ฐานข้อมูล SQLite ของระบบร้านขายดอกไม้
   - ขนาด: ประมาณ 8-16 KB
   - สามารถเปิดได้ด้วยโปรแกรมจัดการฐานข้อมูล เช่น DB Browser for SQLite, DBeaver เป็นต้น

### 2. **create_database.py** 📝
   - สคริปต์ Python สำหรับสร้างฐานข้อมูลและเพิ่มข้อมูลตัวอย่าง
   - การทำงาน:
     - สร้างตาราง Categories (5 หมวดหมู่)
     - สร้างตาราง Flowers (5 ชนิดดอกไม้)
     - ตั้งค่า Foreign Key เชื่อมต่อระหว่างตาราง
     - แสดงผลข้อมูลที่เพิ่มเข้ามา

### 3. **DATABASE_SCHEMA.md** 📖
   - เอกสารสำหรับอธิบายโครงสร้างของฐานข้อมูล
   - รายละเอียดคอลัมน์ประเภทข้อมูล และคำอธิบาย
   - ตัวอย่าง SQL Query ต่างๆ
   - ไดอะแกรมความสัมพันธ์ระหว่างตาราง

### 4. **example_usage.py** 🚀
   - ตัวอย่างฟังก์ชัน Python สำหรับการใช้งานฐานข้อมูล
   - ตัวอย่างการค้นหา การจัดเรียง และการสถิติ
   - สามารถปรับแก้เพื่อใช้ในโปรเจกต์ของคุณเอง

---

## 🗂️ โครงสร้างตาราง

### ตาราง 1: **Categories** (ตารางรอง)
จัดหมวดหมู่ของดอกไม้

| คอลัมน์ | ประเภท | รายละเอียด |
|--------|--------|----------|
| category_id | INTEGER (PK, AUTOINCREMENT) | รหัสหมวดหมู่ |
| category_name | TEXT (NOT NULL, UNIQUE) | ชื่อหมวดหมู่ (ไม่ซ้ำกัน) |
| description | TEXT | คำอธิบายหมวดหมู่ |
| created_at | TIMESTAMP | วันที่สร้างข้อมูล |

**ข้อมูลตัวอย่าง 5 รายการ:**
- Rose (ดอกกุหลาบ)
- Tulip (ดอกทิวลิป)
- Sunflower (ดอกทานตะวัน)
- Orchid (ดอกกล้วยไม้)
- Daisy (ดอกเดซี่)

---

### ตาราง 2: **Flowers** (ตารางหลัก)
เก็บข้อมูลดอกไม้ที่จำหน่าย

| คอลัมน์ | ประเภท | รายละเอียด |
|--------|--------|----------|
| flower_id | INTEGER (PK, AUTOINCREMENT) | รหัสดอกไม้ |
| flower_name | TEXT (NOT NULL) | ชื่อดอกไม้ |
| category_id | INTEGER (FK) | อ้างอิงถึง Categories.category_id |
| price | REAL (NOT NULL) | ราคา (บาท) |
| quantity_in_stock | INTEGER (DEFAULT 0) | จำนวนในสต็อก |
| description | TEXT | คำอธิบายดอกไม้ |
| color | TEXT | สีของดอกไม้ |
| created_at | TIMESTAMP | วันที่สร้างข้อมูล |

**ข้อมูลตัวอย่าง 5 รายการ:**
- Red Rose - 150.00 บาท (25 ชั้น)
- White Rose - 150.00 บาท (30 ชั้น)
- Pink Tulip - 120.00 บาท (15 ชั้น)
- Yellow Sunflower - 200.00 บาท (10 ชั้น)
- Purple Orchid - 300.00 บาท (8 ชั้น)

---

## 🔗 ความสัมพันธ์ (Relationship)

```
Categories (1) ──────► Flowers (Many)
   ▲                        ▼
   │                  Foreign Key
   └──── category_id ────────┘
```

**ความสัมพันธ์แบบ One-to-Many (1:N):**
- 1 หมวดหมู่ สามารถมี หลายชนิดดอกไม้
- การลบหมวดหมู่จะต้องลบดอกไม้ที่เกี่ยวข้องก่อน (Foreign Key Constraint)

---

## 📊 สถิติข้อมูล

| รายการ | ค่า |
|--------|-----|
| **จำนวนหมวดหมู่** | 5 หมวดหมู่ |
| **จำนวนดอกไม้** | 5 ชนิด |
| **จำนวนดอกไม้ในสต็อกทั้งหมด** | 88 ชั้น |
| **ราคาต่ำสุด** | 120.00 บาท (Pink Tulip) |
| **ราคาสูงสุด** | 300.00 บาท (Purple Orchid) |
| **ราคาเฉลี่ย** | 184.00 บาท |

---

## 🚀 วิธีการใช้งาน

### 1️⃣ **สร้างฐานข้อมูลใหม่:**
```bash
python create_database.py
```
ผลลัพธ์: สร้างไฟล์ `flowers_store.db` พร้อมข้อมูลตัวอย่าง

### 2️⃣ **รันตัวอย่างการใช้งาน:**
```bash
python example_usage.py
```
ผลลัพธ์: แสดงการค้นหา การสถิติ และตัวอย่างการใช้งานต่างๆ

### 3️⃣ **เปิดฐานข้อมูลด้วย DB Browser:**
1. ดาวน์โหลด DB Browser for SQLite จาก https://sqlitebrowser.org
2. เปิดไฟล์ `flowers_store.db`
3. ดูโครงสร้างตารางและข้อมูล

---

## 💻 SQL Query ตัวอย่าง

### ดูข้อมูล Rose ทั้งหมด:
```sql
SELECT * FROM Flowers 
WHERE category_id = 1;
```

### ค้นหาดอกไม้ที่ราคาสูงกว่า 150 บาท:
```sql
SELECT flower_name, price 
FROM Flowers 
WHERE price > 150
ORDER BY price DESC;
```

### หาดอกไม้ที่มีจำนวนในสต็อกน้อยสุด:
```sql
SELECT flower_name, quantity_in_stock 
FROM Flowers 
ORDER BY quantity_in_stock 
LIMIT 1;
```

### JOIN ดูดอกไม้พร้อมชื่อหมวดหมู่:
```sql
SELECT f.flower_name, c.category_name, f.price 
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id;
```

---

## ✨ คุณสมบัติของฐานข้อมูล

✅ **Primary Key (PK)**: บ่งชี้เรกคอร์ดที่ไม่ซ้ำกัน
✅ **Foreign Key (FK)**: เชื่อมต่อระหว่างตาราง
✅ **NOT NULL Constraint**: ข้อมูลบางอย่างจำเป็นต้องมี
✅ **UNIQUE Constraint**: ชื่อหมวดหมู่ไม่ซ้ำกัน
✅ **AUTOINCREMENT**: ID เพิ่มอัตโนมัติ
✅ **TIMESTAMP**: บันทึกวันเวลาสร้างข้อมูล
✅ **DEFAULT Value**: ค่าเริ่มต้นเป็น 0 หรือ CURRENT_TIMESTAMP

---

## 🎯 ประโยชน์ของการออกแบบนี้

1. **ลดการซ้ำซ้อน (Normalization)**: ข้อมูลหมวดหมู่เก็บเพียงครั้งเดียว
2. **ความสมบูรณ์ของข้อมูล**: Foreign Key ป้องกันข้อมูลที่ไม่ถูกต้อง
3. **ง่ายต่อการจัดการ**: แก้ไขหมวดหมู่เพียงครั้งเดียว ส่งผลให้ทุกดอกไม้เปลี่ยนไป
4. **ความยืดหยุ่น**: เพิ่มดอกไม้หรือหมวดหมู่ใหม่ได้ง่าย
5. **การค้นหาเร็ว**: สำเร็จได้เร็วขึ้นด้วยวิธี Indexing

---

## 📝 หมายเหตุ

- ฐานข้อมูลนี้สร้างขึ้นด้วย Python 3.x
- ต้องมี `sqlite3` module (รวมอยู่ในไลบรารี่มาตรฐาน Python)
- สามารถเพิ่มตารางเพิ่มเติมได้ เช่น `Orders`, `Customers`, `OrderItems` เป็นต้น
- สามารถเพิ่มหมวดหมู่หรือดอกไม้ใหม่ได้โดยแก้ไข `create_database.py`

---

*สร้างเมื่อ: 20 เมษายน 2026*

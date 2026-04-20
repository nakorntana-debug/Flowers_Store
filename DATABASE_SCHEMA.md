# 🌸 Flowers Store Database Schema

## 📋 ภาพรวมฐานข้อมูล
ฐานข้อมูล `flowers_store.db` ถูกสร้างขึ้นมาเพื่อจัดการระบบร้านขายดอกไม้ โดยมีโครงสร้างดังนี้:

---

## 🗂️ ตาราง 1: Categories (ตารางรอง)
ใช้เพื่อจัดหมวดหมู่ของดอกไม้

| ชื่อคอลัมน์ | ประเภทข้อมูล | คำอธิบาย |
|----------|-----------|---------|
| **category_id** | INTEGER (PRIMARY KEY, AUTOINCREMENT) | รหัสประจำตัวของหมวดหมู่ (เพิ่มอัตโนมัติ) |
| **category_name** | TEXT (NOT NULL, UNIQUE) | ชื่อของหมวดหมู่ (ไม่ซ้ำกัน เช่น Rose, Tulip) |
| **description** | TEXT | คำอธิบายรายละเอียดของหมวดหมู่ |
| **created_at** | TIMESTAMP | วันและเวลาที่สร้างข้อมูล (บันทึกอัตโนมัติ) |

### ✏️ ข้อมูลตัวอย่าง (5 รายการ):
```
1 | Rose      | ดอกกุหลาบ ดอกไม้ที่เป็นสัญลักษณ์ของความรักและความหวัง
2 | Tulip     | ดอกทิวลิป ดอกไม้สวยงามมาจากเนเธอร์แลนด์
3 | Sunflower | ดอกทานตะวัน ดอกไม้ขนาดใหญ่ที่เต็มไปด้วยพลัง
4 | Orchid    | ดอกกล้วยไม้ ดอกไม้ที่สง่างามและหรูหรา
5 | Daisy     | ดอกเดซี่ ดอกไม้ขนาดเล็กน่ารักและสดใส
```

---

## 🌸 ตาราง 2: Flowers (ตารางหลัก)
ใช้เพื่อเก็บข้อมูลของดอกไม้ที่จำหน่าย

| ชื่อคอลัมน์ | ประเภทข้อมูล | คำอธิบาย |
|----------|-----------|---------|
| **flower_id** | INTEGER (PRIMARY KEY, AUTOINCREMENT) | รหัสประจำตัวของดอกไม้ (เพิ่มอัตโนมัติ) |
| **flower_name** | TEXT (NOT NULL) | ชื่อของดอกไม้ (เช่น Red Rose, Pink Tulip) |
| **category_id** | INTEGER (NOT NULL) | รหัสอ้างอิงไปยังตาราง Categories (Foreign Key) |
| **price** | REAL (NOT NULL) | ราคาของดอกไม้ (หน่วยเป็นบาท) |
| **quantity_in_stock** | INTEGER (NOT NULL, DEFAULT 0) | จำนวนดอกไม้ในสต็อก (ค่าเริ่มต้นเป็น 0) |
| **description** | TEXT | คำอธิบายรายละเอียดของดอกไม้ |
| **color** | TEXT | สีของดอกไม้ (เช่น Red, White, Pink) |
| **created_at** | TIMESTAMP | วันและเวลาที่สร้างข้อมูล (บันทึกอัตโนมัติ) |

### ✏️ ข้อมูลตัวอย่าง (5 รายการ):
```
1 | Red Rose         | 1 (Rose)     | 150.00 | 25 | ดอกกุหลาบสีแดง สดใสและสวยงาม    | Red
2 | White Rose       | 1 (Rose)     | 150.00 | 30 | ดอกกุหลาบสีขาว สัญลักษณ์ความบริสุทธิ์ | White
3 | Pink Tulip       | 2 (Tulip)    | 120.00 | 15 | ดอกทิวลิปสีชมพู น่ารักและสุภาพ  | Pink
4 | Yellow Sunflower | 3 (Sunflower)| 200.00 | 10 | ดอกทานตะวันสีเหลือง เต็มไปด้วยความสุข | Yellow
5 | Purple Orchid    | 4 (Orchid)   | 300.00 | 8  | ดอกกล้วยไม้สีม่วง หรูหราและหาได้ยาก | Purple
```

---

## 🔗 ความสัมพันธ์ระหว่างตาราง (Foreign Key Relationship)

```
┌─────────────────┐
│   CATEGORIES    │
├─────────────────┤
│ category_id [PK]│◄──────┐
│ category_name   │       │ ONE TO MANY
│ description     │       │ (1 หมวดหมู่ : หลายดอกไม้)
│ created_at      │       │
└─────────────────┘       │
                          │
                    [Foreign Key]
                          │
┌─────────────────────────┴────┐
│        FLOWERS              │
├─────────────────────────────┤
│ flower_id [PK]              │
│ flower_name                 │
│ category_id [FK] ───────────┘
│ price                       │
│ quantity_in_stock           │
│ description                 │
│ color                       │
│ created_at                  │
└─────────────────────────────┘
```

### 📌 ความหมาย:
- **Primary Key (PK)**: ค่าที่ไม่ซ้ำกัน และใช้บ่งชี้ถึงเรกคอร์ดแต่ละรายการ
- **Foreign Key (FK)**: ใช้เชื่อมต่อกับตาราง Categories เพื่อให้รู้ว่าดอกไม้ชนิดนี้เป็นของหมวดหมู่ไหน
- **ONE TO MANY**: หมวดหมู่หนึ่งสามารถมีดอกไม้ได้หลายชนิด

---

## 💾 วิธีการใช้ฐานข้อมูล

### ดูข้อมูลทั้งหมดจากตาราง Categories:
```sql
SELECT * FROM Categories;
```

### ดูข้อมูลทั้งหมดจากตาราง Flowers:
```sql
SELECT * FROM Flowers;
```

### ดูข้อมูล Flowers พร้อมชื่อหมวดหมู่ (JOIN):
```sql
SELECT 
    f.flower_id, 
    f.flower_name, 
    c.category_name, 
    f.price, 
    f.quantity_in_stock, 
    f.color
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id;
```

### ค้นหาดอกไม้ตามหมวดหมู่ (เช่น Rose):
```sql
SELECT f.flower_name, f.price, f.quantity_in_stock
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id
WHERE c.category_name = 'Rose';
```

### หาดอกไม้ที่ราคาสูงสุด:
```sql
SELECT flower_name, price 
FROM Flowers 
ORDER BY price DESC 
LIMIT 1;
```

---

## 📊 สถิติบางประการ

- **จำนวนหมวดหมู่ทั้งหมด**: 5 หมวดหมู่
- **จำนวนดอกไม้ทั้งหมด**: 5 ชนิด
- **ราคาเฉลี่ย**: 184.00 บาท
- **ราคาต่ำสุด**: 120.00 บาท (Pink Tulip)
- **ราคาสูงสุด**: 300.00 บาท (Purple Orchid)
- **จำนวนดอกไม้ในสต็อกทั้งหมด**: 88 ชั้น

---

## 🎯 ประโยชน์ของโครงสร้างนี้

✅ **ลดการซ้ำซ้อนของข้อมูล**: ไม่ต้องเก็บชื่อหมวดหมู่ซ้ำๆ ในทุกแถวของ Flowers
✅ **ง่ายต่อการจัดการ**: สามารถแก้ไขชื่อหมวดหมู่เพียงครั้งเดียวในตาราง Categories
✅ **ความสมบูรณ์ของข้อมูล**: Foreign Key ป้องกันการใส่ category_id ที่ไม่มีอยู่
✅ **ความยืดหยุ่น**: สามารถเพิ่มดอกไม้หรือหมวดหมู่ใหม่ได้ง่าย

---

*ฐานข้อมูลนี้สร้างขึ้นเมื่อวันที่ 20 เมษายน 2026*

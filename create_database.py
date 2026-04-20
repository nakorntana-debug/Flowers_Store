import sqlite3
from datetime import datetime

# สร้างการเชื่อมต่อกับฐานข้อมูล SQLite
db_file = "flowers_store.db"
connection = sqlite3.connect(db_file)
cursor = connection.cursor()

# ลบตารางเก่า (ถ้ามี) เพื่อให้สร้างใหม่
cursor.execute("DROP TABLE IF EXISTS Flowers")
cursor.execute("DROP TABLE IF EXISTS Categories")

# สร้างตาราง Categories (ตารางรอง)
cursor.execute('''
CREATE TABLE Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# สร้างตาราง Flowers (ตารางหลัก)
cursor.execute('''
CREATE TABLE Flowers (
    flower_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flower_name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    price REAL NOT NULL,
    quantity_in_stock INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    color TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
)
''')

# เพิ่มข้อมูลตัวอย่าง - ตาราง Categories
categories_data = [
    ("Rose", "ดอกกุหลาบ ดอกไม้ที่เป็นสัญลักษณ์ของความรักและความหวัง"),
    ("Tulip", "ดอกทิวลิป ดอกไม้สวยงามมาจากเนเธอร์แลนด์"),
    ("Sunflower", "ดอกทานตะวัน ดอกไม้ขนาดใหญ่ที่เต็มไปด้วยพลัง"),
    ("Orchid", "ดอกกล้วยไม้ ดอกไม้ที่สง่างามและหรูหรา"),
    ("Daisy", "ดอกเดซี่ ดอกไม้ขนาดเล็กน่ารักและสดใส")
]

cursor.executemany("INSERT INTO Categories (category_name, description) VALUES (?, ?)", categories_data)

# เพิ่มข้อมูลตัวอย่าง - ตาราง Flowers
flowers_data = [
    ("Red Rose", 1, 150.00, 25, "ดอกกุหลาบสีแดง สดใสและสวยงาม", "Red"),
    ("White Rose", 1, 150.00, 30, "ดอกกุหลาบสีขาว สัญลักษณ์ของความบริสุทธิ์", "White"),
    ("Pink Tulip", 2, 120.00, 15, "ดอกทิวลิปสีชมพู น่ารักและสุภาพ", "Pink"),
    ("Yellow Sunflower", 3, 200.00, 10, "ดอกทานตะวันสีเหลือง เต็มไปด้วยความสุข", "Yellow"),
    ("Purple Orchid", 4, 300.00, 8, "ดอกกล้วยไม้สีม่วง หรูหราและหาได้ยาก", "Purple")
]

cursor.executemany(
    "INSERT INTO Flowers (flower_name, category_id, price, quantity_in_stock, description, color) VALUES (?, ?, ?, ?, ?, ?)",
    flowers_data
)

# บันทึกการเปลี่ยนแปลง
connection.commit()

# แสดงข้อมูลจากตาราง Categories
print("=" * 80)
print("📊 ข้อมูลจากตาราง CATEGORIES (ตารางรอง)")
print("=" * 80)
cursor.execute("SELECT * FROM Categories")
categories = cursor.fetchall()
for cat in categories:
    print(f"ID: {cat[0]}, ชื่อหมวดหมู่: {cat[1]}, คำอธิบาย: {cat[2]}")

print("\n" + "=" * 80)
print("🌸 ข้อมูลจากตาราง FLOWERS (ตารางหลัก)")
print("=" * 80)
cursor.execute('''
    SELECT f.flower_id, f.flower_name, c.category_name, f.price, f.quantity_in_stock, f.color
    FROM Flowers f
    JOIN Categories c ON f.category_id = c.category_id
''')
flowers = cursor.fetchall()
for flower in flowers:
    print(f"ID: {flower[0]}, ชื่อดอก: {flower[1]}, หมวดหมู่: {flower[2]}, ราคา: {flower[3]} บาท, จำนวน: {flower[4]} ชั้น, สี: {flower[5]}")

# ปิดการเชื่อมต่อ
connection.close()

print("\n" + "=" * 80)
print(f"✅ ฐานข้อมูล '{db_file}' สร้างสำเร็จแล้ว!")
print("=" * 80)

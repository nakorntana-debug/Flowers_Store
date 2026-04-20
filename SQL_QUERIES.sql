-- ====================================================================
-- 🌸 Flowers Store Database - SQL Schema & Useful Queries
-- ====================================================================
-- ตัวอักษรสำหรับการใช้งานโดยตรงกับ SQLite

-- ====================================================================
-- 1️⃣ SQL CREATE TABLE STATEMENTS (สำหรับสร้างตารางใหม่)
-- ====================================================================

-- สร้างตาราง Categories
CREATE TABLE Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- สร้างตาราง Flowers
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
);


-- ====================================================================
-- 2️⃣ INSERT DATA STATEMENTS (เพิ่มข้อมูลตัวอย่าง)
-- ====================================================================

-- เพิ่มหมวดหมู่
INSERT INTO Categories (category_name, description) VALUES 
('Rose', 'ดอกกุหลาบ ดอกไม้ที่เป็นสัญลักษณ์ของความรักและความหวัง'),
('Tulip', 'ดอกทิวลิป ดอกไม้สวยงามมาจากเนเธอร์แลนด์'),
('Sunflower', 'ดอกทานตะวัน ดอกไม้ขนาดใหญ่ที่เต็มไปด้วยพลัง'),
('Orchid', 'ดอกกล้วยไม้ ดอกไม้ที่สง่างามและหรูหรา'),
('Daisy', 'ดอกเดซี่ ดอกไม้ขนาดเล็กน่ารักและสดใส');

-- เพิ่มดอกไม้
INSERT INTO Flowers (flower_name, category_id, price, quantity_in_stock, description, color) VALUES 
('Red Rose', 1, 150.00, 25, 'ดอกกุหลาบสีแดง สดใสและสวยงาม', 'Red'),
('White Rose', 1, 150.00, 30, 'ดอกกุหลาบสีขาว สัญลักษณ์ของความบริสุทธิ์', 'White'),
('Pink Tulip', 2, 120.00, 15, 'ดอกทิวลิปสีชมพู น่ารักและสุภาพ', 'Pink'),
('Yellow Sunflower', 3, 200.00, 10, 'ดอกทานตะวันสีเหลือง เต็มไปด้วยความสุข', 'Yellow'),
('Purple Orchid', 4, 300.00, 8, 'ดอกกล้วยไม้สีม่วง หรูหราและหาได้ยาก', 'Purple');


-- ====================================================================
-- 3️⃣ SELECT QUERIES (ค้นหาข้อมูล)
-- ====================================================================

-- 📂 ดูหมวดหมู่ทั้งหมด
SELECT * FROM Categories;

-- 🌸 ดูดอกไม้ทั้งหมด
SELECT * FROM Flowers;

-- 🔗 ดูดอกไม้พร้อมชื่อหมวดหมู่ (JOIN)
SELECT 
    f.flower_id, 
    f.flower_name, 
    c.category_name, 
    f.price, 
    f.quantity_in_stock, 
    f.color
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id
ORDER BY f.flower_id;

-- 🔍 ค้นหาดอกไม้ในหมวดหมู่ Rose
SELECT 
    f.flower_name, 
    f.price, 
    f.quantity_in_stock, 
    f.color
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id
WHERE c.category_name = 'Rose';

-- 💰 ดอกไม้ในช่วงราคา 100-200 บาท
SELECT 
    f.flower_name, 
    f.price, 
    c.category_name
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id
WHERE f.price BETWEEN 100 AND 200
ORDER BY f.price;

-- 👑 ดอกไม้ที่แพงที่สุด
SELECT 
    f.flower_name, 
    f.price, 
    c.category_name, 
    f.description
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id
ORDER BY f.price DESC
LIMIT 1;

-- 💚 ดอกไม้ที่ถูกที่สุด
SELECT 
    f.flower_name, 
    f.price, 
    c.category_name
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id
ORDER BY f.price ASC
LIMIT 1;

-- 📦 ดอกไม้ที่มีสต็อกมากที่สุด
SELECT 
    f.flower_name, 
    f.quantity_in_stock, 
    c.category_name
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id
ORDER BY f.quantity_in_stock DESC;

-- ⚠️ ดอกไม้ที่สต็อกน้อย (น้อยกว่า 10 ชั้น)
SELECT 
    f.flower_name, 
    f.quantity_in_stock, 
    c.category_name
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id
WHERE f.quantity_in_stock < 10
ORDER BY f.quantity_in_stock;

-- 🎨 ดูดอกไม้ตามสี (เช่น Red)
SELECT 
    f.flower_name, 
    f.color, 
    f.price, 
    c.category_name
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id
WHERE f.color = 'Red';

-- ✨ ดูดอกไม้ที่มีคำว่า 'Rose' ในชื่อ (LIKE)
SELECT 
    f.flower_name, 
    f.price, 
    c.category_name
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id
WHERE f.flower_name LIKE '%Rose%';


-- ====================================================================
-- 4️⃣ STATISTICS & AGGREGATION QUERIES (สถิติและการรวมข้อมูล)
-- ====================================================================

-- 📊 จำนวนดอกไม้ทั้งหมด
SELECT COUNT(*) AS 'จำนวนดอกไม้ทั้งหมด' FROM Flowers;

-- 🔢 จำนวนหมวดหมู่
SELECT COUNT(*) AS 'จำนวนหมวดหมู่' FROM Categories;

-- 💵 ราคาเฉลี่ย
SELECT 
    ROUND(AVG(price), 2) AS 'ราคาเฉลี่ย (บาท)'
FROM Flowers;

-- 👑 ราคาสูงสุด
SELECT 
    MAX(price) AS 'ราคาสูงสุด (บาท)'
FROM Flowers;

-- 💚 ราคาต่ำสุด
SELECT 
    MIN(price) AS 'ราคาต่ำสุด (บาท)'
FROM Flowers;

-- 📦 จำนวนดอกไม้ในสต็อกทั้งหมด
SELECT 
    SUM(quantity_in_stock) AS 'จำนวนดอกไม้ในสต็อกทั้งหมด (ชั้น)'
FROM Flowers;

-- 📊 สรุปสถิติทั้งหมด
SELECT 
    COUNT(*) AS 'จำนวนดอกไม้',
    ROUND(AVG(price), 2) AS 'ราคาเฉลี่ย',
    MIN(price) AS 'ราคาต่ำสุด',
    MAX(price) AS 'ราคาสูงสุด',
    SUM(quantity_in_stock) AS 'สต็อกทั้งหมด'
FROM Flowers;

-- 📈 สถิติตามหมวดหมู่
SELECT 
    c.category_name,
    COUNT(f.flower_id) AS 'จำนวนชนิด',
    ROUND(AVG(f.price), 2) AS 'ราคาเฉลี่ย',
    SUM(f.quantity_in_stock) AS 'สต็อกรวม'
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id
GROUP BY c.category_name
ORDER BY COUNT(f.flower_id) DESC;


-- ====================================================================
-- 5️⃣ UPDATE & DELETE STATEMENTS (แก้ไขและลบข้อมูล)
-- ====================================================================

-- ✏️ อัปเดตราคาดอกไม้ (เช่น Red Rose)
UPDATE Flowers 
SET price = 160.00 
WHERE flower_id = 1;

-- ✏️ เพิ่มจำนวนในสต็อก (เช่น White Rose)
UPDATE Flowers 
SET quantity_in_stock = quantity_in_stock + 10 
WHERE flower_id = 2;

-- ✏️ ลดราคาดอกไม้ทั้งหมดในหมวดหมู่ Rose 10%
UPDATE Flowers 
SET price = price * 0.9 
WHERE category_id = 1;

-- ❌ ลบดอกไม้ที่มี ID = 5 (Purple Orchid)
-- DELETE FROM Flowers WHERE flower_id = 5;

-- ❌ ลบหมวดหมู่ (จะเกิด error ถ้ามีดอกไม้ในหมวดหมู่นี้)
-- DELETE FROM Categories WHERE category_id = 5;


-- ====================================================================
-- 6️⃣ ADVANCED QUERIES (การค้นหาขั้นสูง)
-- ====================================================================

-- 🏆 ดอกไม้ที่มีราคามากกว่าราคาเฉลี่ย
SELECT 
    f.flower_name, 
    f.price,
    ROUND((SELECT AVG(price) FROM Flowers), 2) AS 'ราคาเฉลี่ย'
FROM Flowers f
WHERE f.price > (SELECT AVG(price) FROM Flowers)
ORDER BY f.price DESC;

-- 📋 นับจำนวนดอกไม้ในแต่ละหมวดหมู่
SELECT 
    c.category_name,
    COUNT(f.flower_id) AS 'จำนวน'
FROM Categories c
LEFT JOIN Flowers f ON c.category_id = f.category_id
GROUP BY c.category_name;

-- 🎯 หาดอกไม้ที่มีสต็อกเท่ากับสต็อกเฉลี่ย
SELECT 
    f.flower_name,
    f.quantity_in_stock,
    ROUND((SELECT AVG(quantity_in_stock) FROM Flowers), 0) AS 'เฉลี่ย'
FROM Flowers f
WHERE f.quantity_in_stock = (SELECT ROUND(AVG(quantity_in_stock)) FROM Flowers);

-- 💎 ดอกไม้ที่มีคุณค่า = ราคา × จำนวนในสต็อก (สูงสุด)
SELECT 
    f.flower_name,
    f.price,
    f.quantity_in_stock,
    ROUND(f.price * f.quantity_in_stock, 2) AS 'มูลค่ารวม (บาท)'
FROM Flowers f
ORDER BY (f.price * f.quantity_in_stock) DESC;

-- 📊 รายงานรายละเอียดของทุกดอกไม้
SELECT 
    f.flower_id,
    f.flower_name,
    c.category_name,
    f.color,
    f.price,
    f.quantity_in_stock,
    ROUND(f.price * f.quantity_in_stock, 2) AS 'มูลค่า',
    f.description,
    DATE(f.created_at) AS 'วันที่สร้าง'
FROM Flowers f
JOIN Categories c ON f.category_id = c.category_id
ORDER BY f.flower_id;

-- ====================================================================
-- หมายเหตุ:
-- - LIKE: ใช้สำหรับค้นหาข้อความ (%) เป็นตัวแทน
-- - JOIN: เชื่อมตารางสองตารางตามเงื่อนไข
-- - GROUP BY: จัดกลุ่มข้อมูล
-- - ORDER BY: เรียงลำดับข้อมูล (ASC=น้อยไปมาก, DESC=มากไปน้อย)
-- - WHERE: เงื่อนไขในการค้นหา
-- - ROUND: ปัดเศษทศนิยม
-- - DATE: แสดงเฉพาะวันที่ (ไม่มีเวลา)
-- ====================================================================

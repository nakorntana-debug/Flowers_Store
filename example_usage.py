import sqlite3

# ===============================
# 📖 ตัวอย่างการใช้งาน Flowers Store Database
# ===============================

def connect_db(db_name="flowers_store.db"):
    """เชื่อมต่อกับฐานข้อมูล"""
    return sqlite3.connect(db_name)

def display_all_categories(connection):
    """แสดงหมวดหมู่ทั้งหมด"""
    print("\n📂 หมวดหมู่ดอกไม้ทั้งหมด:")
    print("-" * 80)
    cursor = connection.cursor()
    cursor.execute("SELECT category_id, category_name, description FROM Categories")
    for row in cursor.fetchall():
        print(f"[{row[0]}] {row[1]}: {row[2]}")

def display_all_flowers(connection):
    """แสดงดอกไม้ทั้งหมด พร้อมหมวดหมู่"""
    print("\n🌸 ดอกไม้ทั้งหมด:")
    print("-" * 80)
    cursor = connection.cursor()
    cursor.execute('''
        SELECT 
            f.flower_id, 
            f.flower_name, 
            c.category_name, 
            f.price, 
            f.quantity_in_stock, 
            f.color
        FROM Flowers f
        JOIN Categories c ON f.category_id = c.category_id
        ORDER BY f.flower_id
    ''')
    
    for row in cursor.fetchall():
        print(f"[{row[0]}] {row[1]:20} | หมวดหมู่: {row[2]:12} | ราคา: {row[3]:7.2f} บาท | คงเหลือ: {row[4]:3} ชั้น | สี: {row[5]}")

def search_flowers_by_category(connection, category_name):
    """ค้นหาดอกไม้ตามหมวดหมู่"""
    print(f"\n🔍 ค้นหาดอกไม้ในหมวดหมู่ '{category_name}':")
    print("-" * 80)
    cursor = connection.cursor()
    cursor.execute('''
        SELECT f.flower_name, f.price, f.quantity_in_stock, f.color, f.description
        FROM Flowers f
        JOIN Categories c ON f.category_id = c.category_id
        WHERE c.category_name = ?
    ''', (category_name,))
    
    rows = cursor.fetchall()
    if not rows:
        print(f"❌ ไม่พบดอกไม้ในหมวดหมู่ '{category_name}'")
    else:
        for row in rows:
            print(f"• {row[0]} - ราคา: {row[1]:.2f} บาท, คงเหลือ: {row[2]} ชั้น, สี: {row[3]}")
            print(f"  รายละเอียด: {row[4]}\n")

def get_flowers_by_price_range(connection, min_price, max_price):
    """ค้นหาดอกไม้ตามช่วงราคา"""
    print(f"\n💰 ดอกไม้ในช่วงราคา {min_price} - {max_price} บาท:")
    print("-" * 80)
    cursor = connection.cursor()
    cursor.execute('''
        SELECT f.flower_name, f.price, c.category_name, f.quantity_in_stock
        FROM Flowers f
        JOIN Categories c ON f.category_id = c.category_id
        WHERE f.price BETWEEN ? AND ?
        ORDER BY f.price
    ''', (min_price, max_price))
    
    rows = cursor.fetchall()
    if not rows:
        print(f"❌ ไม่พบดอกไม้ในช่วงราคานี้")
    else:
        for row in rows:
            print(f"• {row[0]:20} ({row[2]}) - ราคา: {row[1]:7.2f} บาท, คงเหลือ: {row[3]} ชั้น")

def get_most_expensive_flower(connection):
    """หาดอกไม้ที่แพงที่สุด"""
    print("\n👑 ดอกไม้ที่แพงที่สุด:")
    print("-" * 80)
    cursor = connection.cursor()
    cursor.execute('''
        SELECT f.flower_name, f.price, c.category_name, f.description
        FROM Flowers f
        JOIN Categories c ON f.category_id = c.category_id
        ORDER BY f.price DESC
        LIMIT 1
    ''')
    
    row = cursor.fetchone()
    if row:
        print(f"• {row[0]} ({row[2]}) - ราคา: {row[1]:.2f} บาท")
        print(f"  รายละเอียด: {row[3]}")

def get_stock_statistics(connection):
    """แสดงสถิติการคงเหลือสินค้า"""
    print("\n📊 สถิติการคงเหลือสินค้า:")
    print("-" * 80)
    cursor = connection.cursor()
    
    cursor.execute("SELECT SUM(quantity_in_stock) FROM Flowers")
    total_stock = cursor.fetchone()[0]
    print(f"จำนวนดอกไม้ในสต็อกทั้งหมด: {total_stock} ชั้น")
    
    cursor.execute("SELECT AVG(price) FROM Flowers")
    avg_price = cursor.fetchone()[0]
    print(f"ราคาเฉลี่ย: {avg_price:.2f} บาท")
    
    cursor.execute("SELECT MIN(price), MAX(price) FROM Flowers")
    min_max = cursor.fetchone()
    print(f"ราคาต่ำสุด: {min_max[0]:.2f} บาท")
    print(f"ราคาสูงสุด: {min_max[1]:.2f} บาท")
    
    cursor.execute('''
        SELECT f.flower_name, f.quantity_in_stock
        FROM Flowers f
        ORDER BY f.quantity_in_stock DESC
    ''')
    
    print(f"\nสินค้าที่คงเหลือมากที่สุด:")
    for row in cursor.fetchall():
        print(f"  • {row[0]}: {row[1]} ชั้น")

def add_new_flower(connection, flower_name, category_id, price, quantity, description, color):
    """เพิ่มดอกไม้ใหม่ (ตัวอย่าง)"""
    cursor = connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO Flowers (flower_name, category_id, price, quantity_in_stock, description, color)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (flower_name, category_id, price, quantity, description, color))
        connection.commit()
        print(f"\n✅ เพิ่มดอกไม้ '{flower_name}' สำเร็จ")
    except sqlite3.Error as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")

def update_flower_price(connection, flower_id, new_price):
    """อัปเดตราคาดอกไม้ (ตัวอย่าง)"""
    cursor = connection.cursor()
    try:
        cursor.execute('''
            UPDATE Flowers SET price = ? WHERE flower_id = ?
        ''', (new_price, flower_id))
        connection.commit()
        print(f"\n✅ อัปเดตราคาดอกไม้ ID {flower_id} เป็น {new_price:.2f} บาท")
    except sqlite3.Error as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")

# ===============================
# 🚀 การทำงาน
# ===============================

if __name__ == "__main__":
    # เชื่อมต่อกับฐานข้อมูล
    conn = connect_db()
    
    print("=" * 80)
    print("🌸 ยินดีต้อนรับสู่ระบบจัดการร้านขายดอกไม้")
    print("=" * 80)
    
    # แสดงข้อมูล
    display_all_categories(conn)
    display_all_flowers(conn)
    
    # ตัวอย่างการค้นหาและสถิติ
    search_flowers_by_category(conn, "Rose")
    search_flowers_by_category(conn, "Orchid")
    get_flowers_by_price_range(conn, 100, 200)
    get_most_expensive_flower(conn)
    get_stock_statistics(conn)
    
    # ตัวอย่างการเพิ่มข้อมูล (ไม่ใช้ในการ run ทั่วไป เพราะจะเพิ่มข้อมูลซ้ำ)
    # add_new_flower(conn, "Blue Iris", 1, 180.00, 12, "ดอกไอริสสีฟ้า", "Blue")
    
    # ปิดการเชื่อมต่อ
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ สำเร็จการใช้งาน")
    print("=" * 80)

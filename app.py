from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# ========================================
# 📍 DATABASE CONFIGURATION
# ========================================
# ใช้ os.path เพื่อให้รันได้ทั้ง Windows และ PythonAnywhere
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flowers_store.db')

def get_db_connection():
    """เชื่อมต่อกับฐานข้อมูล SQLite"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ========================================
# 🔧 HELPER FUNCTIONS
# ========================================

def get_all_categories():
    """ดึงข้อมูลหมวดหมู่ทั้งหมด"""
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM Categories ORDER BY category_id').fetchall()
    conn.close()
    return categories

def get_all_flowers():
    """ดึงข้อมูลดอกไม้ทั้งหมด พร้อมชื่อหมวดหมู่"""
    conn = get_db_connection()
    flowers = conn.execute('''
        SELECT f.*, c.category_name 
        FROM Flowers f
        JOIN Categories c ON f.category_id = c.category_id
        ORDER BY f.flower_id DESC
    ''').fetchall()
    conn.close()
    return flowers

def get_flower_by_id(flower_id):
    """ดึงข้อมูลดอกไม้ตาม ID"""
    conn = get_db_connection()
    flower = conn.execute(
        'SELECT * FROM Flowers WHERE flower_id = ?', 
        (flower_id,)
    ).fetchone()
    conn.close()
    return flower

def get_category_by_id(category_id):
    """ดึงข้อมูลหมวดหมู่ตาม ID"""
    conn = get_db_connection()
    category = conn.execute(
        'SELECT * FROM Categories WHERE category_id = ?', 
        (category_id,)
    ).fetchone()
    conn.close()
    return category

def add_flower(flower_name, category_id, price, quantity_in_stock, description, color):
    """เพิ่มดอกไม้ใหม่"""
    try:
        conn = get_db_connection()
        conn.execute(
            '''INSERT INTO Flowers 
               (flower_name, category_id, price, quantity_in_stock, description, color) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (flower_name, category_id, price, quantity_in_stock, description, color)
        )
        conn.commit()
        conn.close()
        return True, "ดอกไม้เพิ่มสำเร็จ!"
    except Exception as e:
        return False, f"เกิดข้อผิดพลาด: {str(e)}"

def update_flower(flower_id, flower_name, category_id, price, quantity_in_stock, description, color):
    """อัปเดตข้อมูลดอกไม้"""
    try:
        conn = get_db_connection()
        conn.execute(
            '''UPDATE Flowers 
               SET flower_name = ?, category_id = ?, price = ?, 
                   quantity_in_stock = ?, description = ?, color = ?
               WHERE flower_id = ?''',
            (flower_name, category_id, price, quantity_in_stock, description, color, flower_id)
        )
        conn.commit()
        conn.close()
        return True, "อัปเดตดอกไม้สำเร็จ!"
    except Exception as e:
        return False, f"เกิดข้อผิดพลาด: {str(e)}"

def delete_flower(flower_id):
    """ลบดอกไม้"""
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM Flowers WHERE flower_id = ?', (flower_id,))
        conn.commit()
        conn.close()
        return True, "ลบดอกไม้สำเร็จ!"
    except Exception as e:
        return False, f"เกิดข้อผิดพลาด: {str(e)}"

def add_category(category_name, description):
    """เพิ่มหมวดหมู่ใหม่"""
    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO Categories (category_name, description) VALUES (?, ?)',
            (category_name, description)
        )
        conn.commit()
        conn.close()
        return True, "หมวดหมู่เพิ่มสำเร็จ!"
    except Exception as e:
        return False, f"เกิดข้อผิดพลาด: {str(e)}"

def update_category(category_id, category_name, description):
    """อัปเดตข้อมูลหมวดหมู่"""
    try:
        conn = get_db_connection()
        conn.execute(
            'UPDATE Categories SET category_name = ?, description = ? WHERE category_id = ?',
            (category_name, description, category_id)
        )
        conn.commit()
        conn.close()
        return True, "อัปเดตหมวดหมู่สำเร็จ!"
    except Exception as e:
        return False, f"เกิดข้อผิดพลาด: {str(e)}"

def delete_category(category_id):
    """ลบหมวดหมู่"""
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM Categories WHERE category_id = ?', (category_id,))
        conn.commit()
        conn.close()
        return True, "ลบหมวดหมู่สำเร็จ!"
    except Exception as e:
        return False, f"เกิดข้อผิดพลาด: {str(e)}"

# ========================================
# 🛣️ ROUTES - HOME & DISPLAY
# ========================================

@app.route('/')
def index():
    """หน้าแรก - แสดงสินค้าและหมวดหมู่"""
    flowers = get_all_flowers()
    categories = get_all_categories()
    
    return render_template('index.html', 
                         page='home',
                         flowers=flowers, 
                         categories=categories)

# ========================================
# 🌸 ROUTES - FLOWERS CRUD
# ========================================

@app.route('/flowers')
def view_flowers():
    """ดูรายชื่อดอกไม้ทั้งหมด"""
    flowers = get_all_flowers()
    return render_template('index.html', 
                         page='view_flowers',
                         flowers=flowers)

@app.route('/flower/add', methods=['GET', 'POST'])
def add_flower_page():
    """หน้าเพิ่มดอกไม้ใหม่"""
    categories = get_all_categories()
    message = None
    message_type = None
    
    if request.method == 'POST':
        flower_name = request.form.get('flower_name')
        category_id = request.form.get('category_id')
        price = request.form.get('price')
        quantity_in_stock = request.form.get('quantity_in_stock')
        description = request.form.get('description')
        color = request.form.get('color')
        
        # Validation
        if not all([flower_name, category_id, price, quantity_in_stock]):
            message = "⚠️ กรุณากรอกข้อมูลให้ครบถ้วน"
            message_type = "error"
        else:
            try:
                success, msg = add_flower(flower_name, int(category_id), float(price), 
                                        int(quantity_in_stock), description, color)
                if success:
                    message = msg
                    message_type = "success"
                    return redirect(url_for('index'))
                else:
                    message = msg
                    message_type = "error"
            except Exception as e:
                message = f"⚠️ เกิดข้อผิดพลาด: {str(e)}"
                message_type = "error"
    
    return render_template('index.html', 
                         page='add_flower',
                         categories=categories,
                         message=message,
                         message_type=message_type)

@app.route('/flower/edit/<int:flower_id>', methods=['GET', 'POST'])
def edit_flower_page(flower_id):
    """หน้าแก้ไขดอกไม้"""
    flower = get_flower_by_id(flower_id)
    categories = get_all_categories()
    message = None
    message_type = None
    
    if not flower:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        flower_name = request.form.get('flower_name')
        category_id = request.form.get('category_id')
        price = request.form.get('price')
        quantity_in_stock = request.form.get('quantity_in_stock')
        description = request.form.get('description')
        color = request.form.get('color')
        
        if not all([flower_name, category_id, price, quantity_in_stock]):
            message = "⚠️ กรุณากรอกข้อมูลให้ครบถ้วน"
            message_type = "error"
        else:
            try:
                success, msg = update_flower(flower_id, flower_name, int(category_id), 
                                           float(price), int(quantity_in_stock), description, color)
                if success:
                    return redirect(url_for('index'))
                else:
                    message = msg
                    message_type = "error"
            except Exception as e:
                message = f"⚠️ เกิดข้อผิดพลาด: {str(e)}"
                message_type = "error"
    
    return render_template('index.html', 
                         page='edit_flower',
                         flower=flower,
                         categories=categories,
                         message=message,
                         message_type=message_type)

@app.route('/flower/delete/<int:flower_id>')
def delete_flower_page(flower_id):
    """ลบดอกไม้"""
    success, msg = delete_flower(flower_id)
    return redirect(url_for('index'))

# ========================================
# 📂 ROUTES - CATEGORIES CRUD
# ========================================

@app.route('/categories')
def view_categories():
    """ดูรายชื่อหมวดหมู่ทั้งหมด"""
    categories = get_all_categories()
    return render_template('index.html', 
                         page='view_categories',
                         categories=categories)

@app.route('/category/add', methods=['GET', 'POST'])
def add_category_page():
    """หน้าเพิ่มหมวดหมู่ใหม่"""
    message = None
    message_type = None
    
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        description = request.form.get('description')
        
        if not category_name:
            message = "⚠️ กรุณากรอกชื่อหมวดหมู่"
            message_type = "error"
        else:
            success, msg = add_category(category_name, description)
            if success:
                message = msg
                message_type = "success"
                return redirect(url_for('index'))
            else:
                message = msg
                message_type = "error"
    
    return render_template('index.html', 
                         page='add_category',
                         message=message,
                         message_type=message_type)

@app.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category_page(category_id):
    """หน้าแก้ไขหมวดหมู่"""
    category = get_category_by_id(category_id)
    message = None
    message_type = None
    
    if not category:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        description = request.form.get('description')
        
        if not category_name:
            message = "⚠️ กรุณากรอกชื่อหมวดหมู่"
            message_type = "error"
        else:
            success, msg = update_category(category_id, category_name, description)
            if success:
                return redirect(url_for('index'))
            else:
                message = msg
                message_type = "error"
    
    return render_template('index.html', 
                         page='edit_category',
                         category=category,
                         message=message,
                         message_type=message_type)

@app.route('/category/delete/<int:category_id>')
def delete_category_page(category_id):
    """ลบหมวดหมู่"""
    success, msg = delete_category(category_id)
    return redirect(url_for('index'))

# ========================================
# 🚀 RUN APP
# ========================================

if __name__ == '__main__':
    print(f"📦 Database Path: {DATABASE_PATH}")
    print(f"✅ Database Exists: {os.path.exists(DATABASE_PATH)}")
    app.run(debug=True, host='0.0.0.0', port=5000)

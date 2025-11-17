from flask import Flask, render_template, request, redirect, url_for, flash, session
import random
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'elegant_diy_jewelry_secret'

# ---------------- FILE UPLOAD CONFIG ----------------
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------- DATABASE ----------------
DB_FILE = 'jewelry.db'

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize tables
def init_db():
    conn = get_db()
    cur = conn.cursor()
    # Users
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Products
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            desc TEXT,
            image TEXT
        )
    ''')
    # Orders
    cur.execute('''
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            status TEXT NOT NULL,
            total REAL NOT NULL,
            tracking_number TEXT NOT NULL
        )
    ''')
    # Order items
    cur.execute('''
        CREATE TABLE IF NOT EXISTS order_items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            qty INTEGER NOT NULL,
            price REAL NOT NULL,
            birthstone TEXT,
            image TEXT,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------- USER ROUTES ----------------
@app.route('/')
def home():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products ORDER BY id")
    all_products = cur.fetchall()
    featured = all_products[:3]
    shop_products = all_products[3:]
    birthstones = {
        'January': 'Garnet', 'February': 'Amethyst', 'March': 'Aquamarine',
        'April': 'Diamond', 'May': 'Emerald', 'June': 'Alexandrite',
        'July': 'Ruby', 'August': 'Peridot', 'September': 'Sapphire',
        'October': 'Opal', 'November': 'Topaz', 'December': 'Turquoise'
    }
    return render_template('home.html', title="KIE DIY Jewelry | Home",
                           featured=featured, products=shop_products,
                           birthstones=birthstones, user=session.get('user'))

@app.route('/about')
def about():
    return render_template('about.html', title="About Us", user=session.get('user'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        if name and email and message:
            flash("Thank you for contacting us! We'll reply soon.", "success")
        else:
            flash("Please fill in all fields.", "danger")
    return render_template('contact.html', title="Contact Us", user=session.get('user'))

# ---------------- SHOP ROUTE (Updated for A+B+C) ----------------
@app.route('/shop')
def shop():
    conn = get_db()
    cur = conn.cursor()

    # Fetch all products
    cur.execute("SELECT * FROM products ORDER BY id")
    products = cur.fetchall()

    # Default order-status data
    latest_order = None
    ordered_products = []
    order_status_by_product = {}

    # If user logged in, get their orders by email
    if 'email' in session:
        user_email = session['email']
        # Latest order
        cur.execute("""
            SELECT * FROM orders
            WHERE email=?
            ORDER BY id DESC LIMIT 1
        """, (user_email,))
        latest_order = cur.fetchone()

        if latest_order:
            # Get product_ids in this latest order
            cur.execute("""
                SELECT product_id FROM order_items
                WHERE order_id=?
            """, (latest_order['id'],))
            ordered_products = [row['product_id'] for row in cur.fetchall()]

            # Map product_id → order status
            for pid in ordered_products:
                order_status_by_product[pid] = latest_order['status']

    return render_template(
        'shop.html',
        title="Shop DIY Jewelry",
        products=products,
        latest_order=latest_order,
        ordered_products=ordered_products,
        order_status_by_product=order_status_by_product,
        user=session.get('user')
    )

# ---------------- CART ROUTES ----------------
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user' not in session:
        flash("❌ You must log in to add items to your cart.", "danger")
        return redirect(url_for('login'))

    cart = session.get('cart', {})
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cur.fetchone()
    if not product:
        flash("Product not found!", "danger")
        return redirect(url_for('shop'))

    key = str(product_id)
    if key in cart:
        cart[key]['qty'] += 1
    else:
        cart[key] = {
            'id': product_id,
            'name': product['name'],
            'price': product['price'],
            'qty': 1,
            'image': product['image']
        }

    session['cart'] = cart
    session.modified = True
    flash("✅ Item added to cart!", "success")
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_dict = session.get('cart', {})
    cart_items = []
    total = 0
    for key, item in cart_dict.items():
        if not isinstance(item, dict):
            continue
        item_total = item['price'] * item['qty']
        cart_items.append({
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'qty': item['qty'],
            'item_total': round(item_total, 2),
            'image': item['image']
        })
        total += item_total
    return render_template('cart.html', cart_items=cart_items, total=round(total, 2), user=session.get('user'))

@app.route('/increase/<int:product_id>')
def increase_item(product_id):
    birthstone = request.args.get('birthstone')
    key = f"{product_id}_{birthstone}" if birthstone else str(product_id)
    cart = session.get('cart', {})
    if key in cart:
        cart[key]['qty'] += 1
        session['cart'] = cart
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/decrease/<int:product_id>')
def decrease_item(product_id):
    birthstone = request.args.get('birthstone')
    key = f"{product_id}_{birthstone}" if birthstone else str(product_id)
    cart = session.get('cart', {})
    if key in cart:
        if cart[key]['qty'] > 1:
            cart[key]['qty'] -= 1
        else:
            del cart[key]
        session['cart'] = cart
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/remove/<int:product_id>')
def remove_item(product_id):
    birthstone = request.args.get('birthstone')
    key = f"{product_id}_{birthstone}" if birthstone else str(product_id)
    cart = session.get('cart', {})
    if key in cart:
        del cart[key]
        session['cart'] = cart
        session.modified = True
    return redirect(url_for('cart'))

# ---------------- CHECKOUT ----------------
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user' not in session:
        flash("❌ You must log in to checkout.", "danger")
        return redirect(url_for('login'))

    cart_dict = session.get('cart', {})
    if not cart_dict:
        flash("Your cart is empty!", "warning")
        return redirect(url_for('shop'))

    cart_items = []
    total = 0
    for key, item in cart_dict.items():
        if not isinstance(item, dict):
            continue
        item_total = item['price'] * item['qty']
        cart_items.append({
            'id': item['id'],
            'name': item['name'],
            'qty': item['qty'],
            'price': item['price'],
            'item_total': round(item_total, 2),
            'image': item['image']
        })
        total += item_total

    if request.method == 'POST':
        fullname = request.form.get('fullname')
        address = request.form.get('address')
        phone = request.form.get('phone')
        if fullname and address and phone:
            tracking_number = "TRK" + str(random.randint(100000, 999999))
            email = session.get('email', '')
            conn = get_db()
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO orders(fullname,address,phone,email,status,total,tracking_number)
                VALUES (?,?,?,?,?,?,?)
            ''', (fullname, address, phone, email, 'Processing', round(total, 2), tracking_number))
            order_id = cur.lastrowid
            for item in cart_items:
                cur.execute('''
                    INSERT INTO order_items(order_id,product_id,product_name,qty,price,image)
                    VALUES (?,?,?,?,?,?)
                ''', (order_id, item['id'], item['name'], item['qty'], item['price'], item['image']))
            conn.commit()
            session.pop('cart', None)
            flash(f"✅ Order placed! Your tracking number is {tracking_number}", "success")
            return redirect(url_for('track_order'))
        else:
            flash("Please fill out all fields!", "danger")

    return render_template('checkout.html', cart_items=cart_items, total=round(total, 2), user=session.get('user'))

# ---------------- TRACK ORDER ----------------
@app.route('/track', methods=['GET', 'POST'])
def track_order():
    if request.method == 'POST':
        tnum = request.form.get('tracking_number', '').upper()
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE UPPER(tracking_number)=?", (tnum,))
        order = cur.fetchone()
        if order:
            cur.execute("SELECT * FROM order_items WHERE order_id=?", (order['id'],))
            items = cur.fetchall()
            return render_template('tracking_result.html', order=order, items=items, tnum=tnum)
        flash("Tracking number not found.", "danger")
    return render_template('track_order.html', user=session.get('user'))

# ---------------- SIGNUP & LOGIN ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users(username,email,password) VALUES (?,?,?)", (username, email, password))
            conn.commit()
            flash("Signup successful! Please login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already registered.", "danger")
    return render_template('signup.html', user=session.get('user'))

ADMIN_EMAIL = "admin@kjewelry.com"
ADMIN_PASSWORD = "Admin123"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        if email == ADMIN_EMAIL.lower() and password == ADMIN_PASSWORD:
            session['admin'] = True
            session.pop('email', None)
            flash("Welcome, Admin!", "success")
            return redirect(url_for('admin_dashboard'))
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()
        if user:
            session['user'] = user['username']
            session['email'] = email
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for('shop'))
        flash("Invalid email or password.", "danger")
    return render_template('login.html', user=session.get('user'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('email', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash("Admin logged out.", "success")
    return redirect(url_for('login'))

# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin'):
        flash("Access denied. Please login as admin.", "danger")
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    search = request.form.get('search', '').lower()
    if search:
        cur.execute(
            "SELECT * FROM orders WHERE LOWER(fullname) LIKE ? OR phone LIKE ? OR tracking_number LIKE ? ORDER BY id DESC",
            (f'%{search}%', f'%{search}%', f'%{search}%'))
    else:
        cur.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cur.fetchall()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    return render_template('admin_dashboard.html', orders=orders, products=products, search=search, user=session.get('user'))

# ---------------- ADMIN ORDER DETAILS ----------------
@app.route('/admin/order/<int:order_id>')
def admin_order_details(order_id):
    if not session.get('admin'):
        flash("Access denied. Please login as admin.", "danger")
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    order = cur.fetchone()
    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for('admin_dashboard'))
    cur.execute("SELECT * FROM order_items WHERE order_id=?", (order_id,))
    items = cur.fetchall()
    return render_template('admin_order_details.html', order=order, items=items, user=session.get('user'))

# ---------------- ADMIN UPDATE ORDER STATUS ----------------
@app.route('/admin/order/<int:order_id>/update', methods=['POST'])
def admin_update_order_status(order_id):
    if not session.get('admin'):
        flash("Access denied. Please login as admin.", "danger")
        return redirect(url_for('login'))

    status = request.form.get('status')
    if status not in ['Processing', 'Shipped', 'Delivered']:
        flash("Invalid status.", "danger")
        return redirect(url_for('admin_dashboard'))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    conn.commit()
    flash("Order status updated!", "success")
    return redirect(url_for('admin_dashboard'))

# ---------------- ADMIN ADD/EDIT/DELETE PRODUCT ----------------
@app.route('/admin/add_product', methods=['GET', 'POST'])
def admin_add_product():
    if not session.get('admin'):
        flash("Access denied. Please login as admin.", "danger")
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        desc = request.form.get('desc')
        file = request.files.get('image')
        if not (name and price and desc and file):
            flash("Please fill out all fields and upload an image.", "danger")
            return redirect(url_for('admin_add_product'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO products(name,price,desc,image) VALUES (?,?,?,?)",
                        (name, float(price), desc, filename))
            conn.commit()
            flash("Product added successfully!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid image file type.", "danger")
            return redirect(url_for('admin_add_product'))
    return render_template('admin_add_product.html')

@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
def admin_edit_product(product_id):
    if not session.get('admin'):
        flash("Access denied. Please login as admin.", "danger")
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cur.fetchone()
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        desc = request.form.get('desc')
        file = request.files.get('image')
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute("UPDATE products SET name=?, price=?, desc=?, image=? WHERE id=?",
                            (name, float(price), desc, filename, product_id))
            else:
                flash("Invalid image file type.", "danger")
                return redirect(url_for('admin_edit_product', product_id=product_id))
        else:
            cur.execute("UPDATE products SET name=?, price=?, desc=? WHERE id=?",
                        (name, float(price), desc, product_id))
        conn.commit()
        flash("✅ Product updated successfully!", "success")
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit_product.html', product=dict(product))

@app.route('/admin/delete_product/<int:product_id>')
def admin_delete_product(product_id):
    if not session.get('admin'):
        flash("Access denied. Please login as admin.", "danger")
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    flash('🗑️ Product deleted successfully!', 'danger')
    return redirect(url_for('admin_dashboard'))

# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True)

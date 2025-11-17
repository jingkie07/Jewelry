import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# ---------------- USERS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

# ---------------- PRODUCTS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    image TEXT
)
""")

# Pre-populate products (only if table is empty)
cursor.execute("SELECT COUNT(*) FROM products")
if cursor.fetchone()[0] == 0:
    products = [
        (1, 'Ring Set', 49.99, 'Elegant DIY rings for any occasion.', 'ring1.jpg'),
        (2, 'Bracelet Set', 59.99, 'Handmade bracelets with unique design.', 'bracelet.jpg'),
        (3, 'Choker 1', 39.99, 'Stylish choker necklace for daily wear.', 'choker1.jpg'),
        (4, 'Choker 2', 42.99, 'Elegant choker set with delicate charms.', 'choker2.jpg'),
        (5, 'Couple Bracelet', 69.99, 'Matching couple bracelets for him and her.', 'couple bracelet.jpg'),
        (6, 'Couple Necklace', 79.99, 'Matching couple necklaces for special moments.', 'couple necklace.jpg'),
        (7, 'Ring Set 2', 44.99, 'Minimalist rings for everyday wear.', 'necklace.jpg'),
        (8, 'Bracelet Set 2', 54.99, 'Classic bracelet set for all occasions.', 'pendant1.jpg'),
        (9, 'Choker Set', 49.99, 'Elegant choker set with unique style.', 'pendant2.jpg'),
        (10, 'Couple Set 2', 89.99, 'Stylish matching jewelry for couples.', 'promise ring.jpg')
    ]
    cursor.executemany("INSERT INTO products (id, name, price, description, image) VALUES (?, ?, ?, ?, ?)", products)

# ---------------- ORDERS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tracking_number TEXT UNIQUE,
    fullname TEXT NOT NULL,
    address TEXT NOT NULL,
    phone TEXT NOT NULL,
    total REAL NOT NULL,
    status TEXT NOT NULL
)
""")

# ---------------- ORDER ITEMS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id)
)
""")

conn.commit()
conn.close()
print("✅ Database, tables, and products preloaded successfully!")

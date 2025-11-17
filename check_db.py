import sqlite3

conn = sqlite3.connect("database.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

products = cur.execute("SELECT * FROM products").fetchall()

print("\n=== PRODUCTS IN DATABASE ===")
for p in products:
    print(dict(p))

conn.close()

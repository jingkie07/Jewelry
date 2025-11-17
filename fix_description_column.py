import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Rename 'description' to 'desc'
cur.execute("ALTER TABLE products RENAME COLUMN description TO desc")

conn.commit()
conn.close()

print("Column renamed successfully!")

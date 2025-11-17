import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("SELECT id, image FROM products")
rows = cur.fetchall()

for pid, img in rows:
    if " " in img:
        new_img = img.replace(" ", "_")
        print(f"Fixing: {img} -> {new_img}")
        cur.execute("UPDATE products SET image = ? WHERE id = ?", (new_img, pid))

conn.commit()
conn.close()

print("Image filenames fixed successfully!")

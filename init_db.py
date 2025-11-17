def populate_products():
    conn = get_db()
    cur = conn.cursor()

    # List of products with name, price, description, image filename
    products = [
        {'name': 'Set 4', 'price': 49.99, 'desc': 'Beautiful jewelry set 4', 'image': 'set4.jpg'},
        {'name': 'Set 3', 'price': 45.99, 'desc': 'Elegant set 3', 'image': 'set3.jpg'},
        {'name': 'Set 2', 'price': 40.99, 'desc': 'Charming set 2', 'image': 'set2.jpg'},
        {'name': 'Set 1', 'price': 39.99, 'desc': 'Classic set 1', 'image': 'set1.jpg'},
        {'name': 'Bracelet', 'price': 25.99, 'desc': 'Stylish bracelet', 'image': 'bracelet.jpg'},
        {'name': 'Choker 1', 'price': 15.99, 'desc': 'Trendy choker 1', 'image': 'choker1.jpg'},
        {'name': 'Choker 2', 'price': 16.99, 'desc': 'Trendy choker 2', 'image': 'choker2.jpg'},
        {'name': 'Couple Bracelet', 'price': 29.99, 'desc': 'Matching couple bracelet', 'image': 'couple_bracelet.jpg'},
        {'name': 'Couple Necklace', 'price': 49.99, 'desc': 'Matching couple necklace', 'image': 'couple_necklace.jpg'},
        {'name': 'Necklace', 'price': 35.99, 'desc': 'Elegant necklace', 'image': 'necklace.jpg'},
        {'name': 'Pendant 1', 'price': 19.99, 'desc': 'Simple pendant 1', 'image': 'pendant1.jpg'},
        {'name': 'Pendant 2', 'price': 21.99, 'desc': 'Simple pendant 2', 'image': 'pendant2.jpg'},
        {'name': 'Promise Ring', 'price': 39.99, 'desc': 'Romantic promise ring', 'image': 'promise_ring.jpg'},
        {'name': 'Promise Ring 1', 'price': 42.99, 'desc': 'Elegant promise ring', 'image': 'promise_ring1.jpg'},
        {'name': 'Ring 1', 'price': 22.99, 'desc': 'Stylish ring', 'image': 'ring1.jpg'},
    ]

    # Insert products if they don't already exist
    for p in products:
        cur.execute("SELECT * FROM products WHERE name=?", (p['name'],))
        if not cur.fetchone():
            cur.execute("INSERT INTO products(name, price, desc, image) VALUES (?,?,?,?)",
                        (p['name'], p['price'], p['desc'], p['image']))

    conn.commit()
    conn.close()
    print("✅ Products populated successfully!")


# Run this once
populate_products()

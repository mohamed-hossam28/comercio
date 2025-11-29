import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Clear existing products to avoid duplicates
cursor.execute("DELETE FROM products;")

products = [
    ('Coat', 70.00, 'images/item1.jpg', 'Clothes', 50, 'Stylish winter coat'),
    ('Jeans', 50.00, 'images/item2.jpg', 'Clothes', 100, 'Comfortable blue jeans'),
    ('Boot', 40.00, 'images/item3.jpg', 'Clothes', 40, 'Leather boots'),
    ('Samsung A72', 900.00, 'images/item4.jpg', 'Electronic', 20, 'Samsung Galaxy A72 Smartphone'),
    ('IWatch', 700.00, 'images/item5.jpg', 'Electronic', 30, 'Apple Watch Series 6'),
    ('Lenovo Laptop', 1500.00, 'images/item6.jpg', 'Electronic', 10, 'High performance laptop'),
    ('Nivdea Shaving gel', 30.00, 'images/item7.jpg', 'Cosmetics', 60, 'Smooth shaving gel'),
    ('Garnier', 40.00, 'images/item8.jpg', 'Cosmetics', 50, 'Hair care product'),
    ('Nail Serum', 15.00, 'images/item9.jpg', 'Cosmetics', 80, 'Nail strengthening serum'),
    ('Barcelona T-Shirt', 15.00, 'images/item10.webp', 'Clothes', 80, 'World\'s Best Club T-Shirt')
]

cursor.executemany("""
INSERT INTO products (name, price, image_url, category, stock_avilabilty, description)
VALUES (?, ?, ?, ?, ?, ?);
""", products)

conn.commit()
print("Products seeded successfully!")
conn.close()
import sqlite3
import os

# Get absolute path to ensure we are using the correct DB
db_path = os.path.abspath("db.sqlite3")
print(f"Connecting to database at: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check existing products
cursor.execute("SELECT COUNT(*) FROM products;")
initial_count = cursor.fetchone()[0]
print(f"Initial product count: {initial_count}")

# Clear existing products to avoid duplicates
print("Clearing existing products...")
cursor.execute("DELETE FROM products;")

products = [
    ('American Eagle hoodie', 30.00, 'images/item12.jpg', 'Clothes', 80, 'Hoodie'),
    ('Jeans', 50.00, 'images/item2.jpg', 'Clothes', 100, 'Comfortable blue jeans'),
    ('Samsung s25 ultra', 600.00, 'images/item13.jpg', 'Electronic', 20, 'smartphone'),
    ('Boot', 40.00, 'images/item3.jpg', 'Clothes', 40, 'Leather boots'),
    ('IWatch', 600.00, 'images/item5.jpg', 'Electronic', 30, 'Apple Watch Series 6'),
    ('Lenovo Laptop', 1200.00, 'images/item6.jpg', 'Electronic', 10, 'High performance laptop'),
    ('Nivdea Shaving gel', 30.00, 'images/item7.jpg', 'Cosmetics', 60, 'Smooth shaving gel'),
    ('Garnier', 40.00, 'images/item8.jpg', 'Cosmetics', 50, 'Hair care product'),
    ('Nail Serum', 15.00, 'images/item9.jpg', 'Cosmetics', 80, 'Nail strengthening serum'),
    ('Coat', 70.00, 'images/item1.jpg', 'Clothes', 50, 'Stylish winter coat'),
    ('Barcelona t-shirt', 15.00, 'images/item10.webp', 'Clothes', 80, 't-shirt'),
    ('Samsung A72', 500.00, 'images/item4.jpg', 'Electronic', 20, 'Samsung Galaxy A72 Smartphone'),
    ('Aula headphone', 130.00, 'images/item14.jpg', 'Electronic', 30, 'headphone'),
    ('Anker airpod', 200.00, 'images/item15.jpg', 'Electronic', 50, 'Airpod'),
    ('American Eagle T-Shirt', 20.00, 'images/item17.jpg', 'Clothes', 50, 'T-Shirt'),
    ('Nivea Deodorant', 17.00, 'images/item20.jpg', 'Cosmetics', 50, 'Deodorant')
    
]

print(f"Inserting {len(products)} products...")
cursor.executemany("""
INSERT INTO products (name, price, image_url, category, stock_avilabilty, description)
VALUES (?, ?, ?, ?, ?, ?);
""", products)

conn.commit()

# Verify insertion
cursor.execute("SELECT COUNT(*) FROM products;")
final_count = cursor.fetchone()[0]
print(f"Final product count: {final_count}")

if final_count == len(products):
    print("SUCCESS: Products seeded successfully!")
else:
    print(f"WARNING: Expected {len(products)} products, but found {final_count}.")

conn.close()
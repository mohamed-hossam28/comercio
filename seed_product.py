import sqlite3
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO products (name, price, image_url, category, stock_avilabilty,description)
VALUES ('Lenovo Laptop', 1500, 'views/images/category1.jpg', 'electronics', 10,'Lenovo Laptop');
""")
conn.commit()
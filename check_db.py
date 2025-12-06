import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

cursor.execute("SELECT name, price FROM products")
rows = cursor.fetchall()

print(f"Found {len(rows)} products:")
for row in rows:
    print(row)

conn.close()

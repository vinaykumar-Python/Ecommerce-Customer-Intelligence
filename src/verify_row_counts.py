import sqlite3

connection = sqlite3.connect("database/ecommerce.db")

tables = [
    "customers",
    "geolocation",
    "orders",
    "order_items",
    "payments",
    "reviews",
    "products",
    "sellers",
    "category_translation"
]

print("\nDATABASE ROW COUNTS")
print("=" * 45)

for table in tables:
    count = connection.execute(
        f'SELECT COUNT(*) FROM "{table}"'
    ).fetchone()[0]

    print(f"{table:<25} {count:>12,}")

connection.close()

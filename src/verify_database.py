import sqlite3

connection = sqlite3.connect("database/ecommerce.db")

tables = connection.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""").fetchall()

print("\nDATABASE TABLES")
print("=" * 35)

for table in tables:
    print(table[0])

print("\nTotal tables:", len(tables))

connection.close()

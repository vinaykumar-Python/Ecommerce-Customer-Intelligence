from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path("database/ecommerce.db")
SQL_PATH = Path("sql/03_customer_purchase_behavior.sql")
OUTPUT_PATH = Path("reports/customer_purchase_behavior.csv")

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as connection:
    result = pd.read_sql_query(query, connection)

result.to_csv(OUTPUT_PATH, index=False)

print("\nCUSTOMER PURCHASE BEHAVIOUR")
print("=" * 65)
print(result.to_string(index=False))

print("\nReport saved to:", OUTPUT_PATH)

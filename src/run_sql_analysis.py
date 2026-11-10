from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path("database/ecommerce.db")
SQL_PATH = Path("sql/01_monthly_sales_performance.sql")
OUTPUT_PATH = Path("reports/monthly_sales_performance.csv")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as connection:
    result = pd.read_sql_query(query, connection)

result.to_csv(OUTPUT_PATH, index=False)

print("\nMONTHLY SALES PERFORMANCE")
print("=" * 85)
print(result.to_string(index=False))

print("\nTotal months analysed:", len(result))
print("Report saved to:", OUTPUT_PATH)

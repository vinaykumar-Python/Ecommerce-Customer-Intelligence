import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "08_delivery_performance.sql"
REPORT_PATH = BASE_DIR / "reports" / "delivery_performance.csv"

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    result = pd.read_sql_query(query, conn)

REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(REPORT_PATH, index=False)

print("\nDELIVERY PERFORMANCE SUMMARY")
print("=" * 85)
print(result.to_string(index=False))

print("\nVALIDATION")
print("=" * 85)

total_orders = int(result.loc[0, "total_delivered_orders"])
on_time = int(result.loc[0, "on_time_orders"])
late = int(result.loc[0, "late_orders"])

print("Delivered orders analysed:", total_orders)
print("On-time + late orders:", on_time + late)
print("Order count reconciles:", total_orders == on_time + late)
print("Missing values:", int(result.isna().sum().sum()))

print("\nReport saved:", REPORT_PATH.relative_to(BASE_DIR))

import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "10_monthly_delivery_performance.sql"
REPORT_PATH = BASE_DIR / "reports" / "monthly_delivery_performance.csv"

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(query, conn)

df.to_csv(REPORT_PATH, index=False)

print("\nMONTHLY DELIVERY PERFORMANCE")
print("=" * 110)
print(df.to_string(index=False))

print("\nVALIDATION")
print("=" * 80)
print("Months analysed:", len(df))
print("Total orders:", df["total_orders"].sum())
print("Late orders:", df["late_orders"].sum())
print("On-time orders:", df["on_time_orders"].sum())
print(
    "Order count reconciles:",
    df["total_orders"].sum()
    == df["late_orders"].sum() + df["on_time_orders"].sum()
)
print("Missing values:", df.isna().sum().sum())
print("Duplicate months:", df["purchase_month"].duplicated().sum())

print("\nREPORT SAVED:", REPORT_PATH.relative_to(BASE_DIR))

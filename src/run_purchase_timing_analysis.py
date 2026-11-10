import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "15_purchase_timing_analysis.sql"
REPORT_PATH = BASE_DIR / "reports" / "purchase_timing_analysis.csv"

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(query, conn)

df.to_csv(REPORT_PATH, index=False)

print("\nPURCHASE TIMING ANALYSIS")
print("=" * 115)
print(df.to_string(index=False))

print("\nVALIDATION")
print("=" * 85)

print("Weekday-hour combinations:", len(df))
print("Total orders:", int(df["total_orders"].sum()))
print("Delivered orders:", int(df["delivered_orders"].sum()))
print("Cancelled orders:", int(df["canceled_orders"].sum()))
print(
    "Delivered product revenue:",
    round(df["delivered_product_revenue"].sum(), 2)
)
print("Missing values:", int(df.isna().sum().sum()))

print("\nREPORT SAVED:", REPORT_PATH.relative_to(BASE_DIR))

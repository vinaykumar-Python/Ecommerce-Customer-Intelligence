import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "14_order_failure_analysis.sql"
REPORT_PATH = BASE_DIR / "reports" / "order_failure_by_state.csv"

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(query, conn)

df.to_csv(REPORT_PATH, index=False)

print("\nORDER FAILURE ANALYSIS BY STATE")
print("=" * 110)
print(df.to_string(index=False))

print("\nVALIDATION")
print("=" * 85)
print("States analysed:", df["customer_state"].nunique())
print("Total orders:", int(df["total_orders"].sum()))
print("Cancelled orders:", int(df["canceled_orders"].sum()))
print("Unavailable orders:", int(df["unavailable_orders"].sum()))
print("Missing values:", int(df.isna().sum().sum()))
print("Duplicate states:", int(df["customer_state"].duplicated().sum()))

print("\nREPORT SAVED:", REPORT_PATH.relative_to(BASE_DIR))

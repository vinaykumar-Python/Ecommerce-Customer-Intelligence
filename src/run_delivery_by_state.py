import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "09_delivery_by_state.sql"
REPORT_PATH = BASE_DIR / "reports" / "delivery_by_state.csv"

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(query, conn)

df.to_csv(REPORT_PATH, index=False)

print("\nSTATE-WISE DELIVERY PERFORMANCE")
print("=" * 110)
print(df.to_string(index=False))

print("\nVALIDATION")
print("=" * 80)
print("Number of states:", df["customer_state"].nunique())
print("Total orders:", df["total_orders"].sum())
print("Missing values:", df.isna().sum().sum())
print("Duplicate states:", df["customer_state"].duplicated().sum())

print("\nREPORT SAVED:", REPORT_PATH.relative_to(BASE_DIR))

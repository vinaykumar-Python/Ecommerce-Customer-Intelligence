import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "13_payment_method_analysis.sql"
REPORT_PATH = BASE_DIR / "reports" / "payment_method_analysis.csv"

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(query, conn)

df.to_csv(REPORT_PATH, index=False)

print("\nPAYMENT METHOD ANALYSIS")
print("=" * 110)
print(df.to_string(index=False))

print("\nVALIDATION")
print("=" * 85)

print("Payment methods analysed:", df["payment_type"].nunique())
print("Total payment value:", round(df["total_payment_value"].sum(), 2))
print("Missing values:", int(df.isna().sum().sum()))
print("Duplicate payment methods:", int(df["payment_type"].duplicated().sum()))
print(
    "Payment percentages:",
    round(df["payment_value_percentage"].sum(), 2)
)

print("\nREPORT SAVED:", REPORT_PATH.relative_to(BASE_DIR))

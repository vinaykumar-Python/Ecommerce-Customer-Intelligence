import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "17_state_customer_revenue_analysis.sql"
REPORT_PATH = BASE_DIR / "reports" / "state_customer_revenue_analysis.csv"

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(query, conn)

df.to_csv(REPORT_PATH, index=False)

print("\nSTATE-WISE CUSTOMER AND REVENUE ANALYSIS")
print("=" * 125)
print(df.to_string(index=False))

print("\nVALIDATION")
print("=" * 90)

print("States analysed:", df["customer_state"].nunique())
print("Unique customers across state groups:", int(df["unique_customers"].sum()))
print("Delivered orders:", int(df["delivered_orders"].sum()))
print("Repeat customers across state groups:", int(df["repeat_customers"].sum()))
print("Product revenue:", round(df["product_revenue"].sum(), 2))
print("Missing values:", int(df.isna().sum().sum()))
print("Duplicate states:", int(df["customer_state"].duplicated().sum()))
print("Revenue share:", round(df["revenue_share_percentage"].sum(), 2))

print("\nREPORT SAVED:", REPORT_PATH.relative_to(BASE_DIR))

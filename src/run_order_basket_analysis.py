import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "16_order_basket_analysis.sql"
REPORT_PATH = BASE_DIR / "reports" / "order_basket_analysis.csv"

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(query, conn)

df.to_csv(REPORT_PATH, index=False)

print("\nORDER BASKET ANALYSIS")
print("=" * 110)
print(df.to_string(index=False))

print("\nVALIDATION")
print("=" * 85)

print("Basket categories:", df["basket_category"].nunique())
print("Total orders:", int(df["total_orders"].sum()))
print("Total units:", int(df["total_units"].sum()))
print(
    "Total product revenue:",
    round(df["total_product_revenue"].sum(), 2)
)
print("Missing values:", int(df.isna().sum().sum()))
print("Duplicate categories:", int(df["basket_category"].duplicated().sum()))
print(
    "Order percentages:",
    round(df["order_percentage"].sum(), 2)
)

print("\nREPORT SAVED:", REPORT_PATH.relative_to(BASE_DIR))

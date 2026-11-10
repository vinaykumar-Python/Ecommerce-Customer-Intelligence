from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path("database/ecommerce.db")
SQL_PATH = Path("sql/06_product_category_performance.sql")

OUTPUT_PATH = Path("reports/product_category_performance.csv")

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as connection:
    category_data = pd.read_sql_query(query, connection)

category_data.to_csv(OUTPUT_PATH, index=False)

print("\nTOP 15 PRODUCT CATEGORIES BY REVENUE")
print("=" * 110)

print(
    category_data.head(15).to_string(index=False)
)

print("\nCATEGORY ANALYSIS SUMMARY")
print("=" * 80)

print("Number of categories:", len(category_data))
print("Total orders across categories:",
      category_data["total_orders"].sum())
print("Total units sold:",
      category_data["units_sold"].sum())
print("Total product revenue:",
      round(category_data["product_revenue"].sum(), 2))
print("Total freight revenue:",
      round(category_data["freight_revenue"].sum(), 2))

print("\nVALIDATION")
print("=" * 80)

print(
    "Product revenue reconciles:",
    round(category_data["product_revenue"].sum(), 2)
    == 13221498.11
)

print(
    "Category names unique:",
    category_data["product_category"].is_unique
)

print(
    "Missing values:",
    category_data.isna().sum().sum()
)

print("\nReport saved:", OUTPUT_PATH)

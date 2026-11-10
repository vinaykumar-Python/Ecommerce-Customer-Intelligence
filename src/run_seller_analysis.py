from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path("database/ecommerce.db")
SQL_PATH = Path("sql/07_seller_performance.sql")
OUTPUT_PATH = Path("reports/seller_performance.csv")

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as connection:
    seller_data = pd.read_sql_query(query, connection)

seller_data.to_csv(OUTPUT_PATH, index=False)

print("\nTOP 15 SELLERS BY PRODUCT REVENUE")
print("=" * 115)

print(
    seller_data.head(15).to_string(index=False)
)

print("\nSELLER ANALYSIS SUMMARY")
print("=" * 80)

print("Number of sellers:", len(seller_data))
print("Total product revenue:",
      round(seller_data["product_revenue"].sum(), 2))
print("Total units sold:",
      seller_data["units_sold"].sum())

print("\nVALIDATION")
print("=" * 80)

print(
    "Revenue reconciles:",
    round(seller_data["product_revenue"].sum(), 2)
    == 13221498.11
)

print(
    "Seller IDs unique:",
    seller_data["seller_id"].is_unique
)

print(
    "Missing values:",
    seller_data.isna().sum().sum()
)

print("\nReports saved:", OUTPUT_PATH)

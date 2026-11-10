from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path("database/ecommerce.db")
SQL_PATH = Path("sql/02_monthly_revenue_growth.sql")
OUTPUT_PATH = Path("reports/monthly_revenue_growth.csv")

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as connection:
    result = pd.read_sql_query(query, connection)

result.to_csv(OUTPUT_PATH, index=False)

print("\nMONTHLY REVENUE GROWTH")
print("=" * 100)
print(result.to_string(index=False))

print("\nOVERALL SALES SUMMARY")
print("=" * 45)

total_orders = result["total_orders"].sum()
total_revenue = result["product_revenue"].sum()
overall_aov = total_revenue / total_orders

print(f"Total delivered orders: {total_orders:,.0f}")
print(f"Total product revenue:  {total_revenue:,.2f}")
print(f"Overall average order value: {overall_aov:,.2f}")

best_month = result.loc[result["product_revenue"].idxmax()]

print(f"\nHighest revenue month: {best_month['sales_month']}")
print(f"Highest monthly revenue: {best_month['product_revenue']:,.2f}")

print("\nReport saved to:", OUTPUT_PATH)

from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path("database/ecommerce.db")
SQL_PATH = Path("sql/04_customer_rfm.sql")
OUTPUT_PATH = Path("reports/customer_rfm.csv")

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as connection:
    rfm = pd.read_sql_query(query, connection)

rfm.to_csv(OUTPUT_PATH, index=False)

print("\nCUSTOMER RFM ANALYSIS")
print("=" * 65)

print("\nFirst 10 customers:")
print(rfm.head(10).to_string(index=False))

print("\nRFM SUMMARY STATISTICS")
print("=" * 65)
print(
    rfm[["recency_days", "frequency", "monetary"]]
    .describe()
    .round(2)
    .to_string()
)

print("\nDATA VALIDATION")
print("=" * 65)
print("Total customer records:", len(rfm))
print("Duplicate customer IDs:", rfm["customer_unique_id"].duplicated().sum())
print("Missing values:", rfm.isnull().sum().sum())
print("Minimum recency days:", rfm["recency_days"].min())
print("Minimum frequency:", rfm["frequency"].min())
print("Minimum monetary value:", rfm["monetary"].min())

print("\nReport saved to:", OUTPUT_PATH)

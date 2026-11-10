import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "11_customer_review_analysis.sql"
REPORT_PATH = BASE_DIR / "reports" / "customer_review_analysis.csv"

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(query, conn)

df.to_csv(REPORT_PATH, index=False)

print("\nCUSTOMER REVIEW ANALYSIS")
print("=" * 90)
print(df.to_string(index=False))

print("\nVALIDATION")
print("=" * 80)

row = df.iloc[0]

classified_reviews = (
    int(row["positive_reviews"])
    + int(row["neutral_reviews"])
    + int(row["negative_reviews"])
)

print("Total reviews:", int(row["total_reviews"]))
print("Classified reviews:", classified_reviews)
print("Review counts reconcile:",
      int(row["total_reviews"]) == classified_reviews)
print("Missing values:", int(df.isna().sum().sum()))

print("\nREPORT SAVED:", REPORT_PATH.relative_to(BASE_DIR))

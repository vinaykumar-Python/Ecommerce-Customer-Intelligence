import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "13_category_review_analysis.sql"
REPORT_PATH = BASE_DIR / "reports" / "category_review_analysis.csv"

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(query, conn)

df.to_csv(REPORT_PATH, index=False)

print("\nPRODUCT CATEGORY CUSTOMER SATISFACTION")
print("=" * 120)
print(df.to_string(index=False))

print("\nTOP 10 CATEGORIES BY AVERAGE REVIEW SCORE")
print("=" * 100)
print(df.sort_values(
    "average_review_score", ascending=False
).head(10).to_string(index=False))

print("\nBOTTOM 10 CATEGORIES BY AVERAGE REVIEW SCORE")
print("=" * 100)
print(df.head(10).to_string(index=False))

print("\nVALIDATION")
print("=" * 85)

print("Categories analysed:", df["category_name"].nunique())
print("Missing values:", int(df.isna().sum().sum()))
print("Duplicate categories:", int(df["category_name"].duplicated().sum()))

print(
    "Review classifications reconcile:",
    (
        df["positive_orders"]
        + df["neutral_orders"]
        + df["negative_orders"]
        == df["reviewed_orders"]
    ).all()
)

print("\nREPORT SAVED:", REPORT_PATH.relative_to(BASE_DIR))

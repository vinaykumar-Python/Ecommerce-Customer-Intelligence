import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "12_delivery_review_relationship.sql"
REPORT_PATH = BASE_DIR / "reports" / "delivery_review_relationship.csv"

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(query, conn)

df.to_csv(REPORT_PATH, index=False)

print("\nDELIVERY VS CUSTOMER SATISFACTION")
print("=" * 110)
print(df.to_string(index=False))

print("\nVALIDATION")
print("=" * 85)

if not df.empty:
    print("Delivery groups:", df["delivery_status"].nunique())
    print("Reviewed orders:", df["reviewed_orders"].sum())
    print("Review records:", df["review_records"].sum())

    classified = (
        df["positive_orders"]
        + df["neutral_orders"]
        + df["negative_orders"]
    )

    print("Order classifications reconcile:",
          (classified == df["reviewed_orders"]).all())

    print("Missing values:", int(df.isna().sum().sum()))
    print("Duplicate delivery groups:",
          int(df["delivery_status"].duplicated().sum()))

print("\nREPORT SAVED:", REPORT_PATH.relative_to(BASE_DIR))

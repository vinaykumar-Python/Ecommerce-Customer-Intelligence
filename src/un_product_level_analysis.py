import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "17_product_level_performance.sql"
OUTPUT_PATH = (
    BASE_DIR / "reports" / "product_level_performance.csv"
)


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    if not SQL_PATH.exists():
        raise FileNotFoundError(f"SQL file not found: {SQL_PATH}")

    query = SQL_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(DB_PATH) as connection:
        df = pd.read_sql_query(query, connection)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\nPRODUCT-LEVEL PERFORMANCE ANALYSIS")
    print("=" * 110)

    print(df.head(20).to_string(index=False))

    print("\nVALIDATION")
    print("=" * 70)

    print(f"Products analysed: {len(df):,}")
    print(f"Total units sold: {df['units_sold'].sum():,}")
    print(f"Total orders represented: {df['total_orders'].sum():,}")
    print(f"Total product revenue: {df['product_revenue'].sum():,.2f}")
    print(f"Missing values: {df.isnull().sum().sum():,}")
    print(f"Duplicate products: {df['product_id'].duplicated().sum():,}")

    print(
        f"Top 10 product revenue share: "
        f"{df.head(10)['product_revenue'].sum() / df['product_revenue'].sum() * 100:.2f}%"
    )

    print(f"\nREPORT SAVED: {OUTPUT_PATH.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
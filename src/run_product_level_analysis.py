import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "ecommerce.db"
SQL_PATH = BASE_DIR / "sql" / "17_product_level_performance.sql"
OUTPUT_PATH = BASE_DIR / "reports" / "product_level_performance.csv"


def main():
    for path in (DB_PATH, SQL_PATH):
        if not path.exists():
            raise FileNotFoundError(f"Required file not found: {path}")

    query = SQL_PATH.read_text(encoding="utf-8-sig")

    with sqlite3.connect(DB_PATH) as connection:
        df = pd.read_sql_query(query, connection)

    if df.empty:
        raise ValueError("The product analysis returned no rows.")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    total_revenue = df["product_revenue"].sum()
    expected_revenue = 13221498.11

    print("\nPRODUCT-LEVEL PERFORMANCE ANALYSIS")
    print("=" * 110)
    print(df.head(20).to_string(index=False))

    print("\nVALIDATION")
    print("=" * 70)
    print(f"Products analysed: {len(df):,}")
    print(f"Total units sold: {df['units_sold'].sum():,}")
    print(f"Product revenue: {total_revenue:,.2f}")
    print(f"Expected product revenue: {expected_revenue:,.2f}")
    print(f"Revenue difference: {total_revenue - expected_revenue:,.2f}")
    print(f"Revenue reconciles: {abs(total_revenue - expected_revenue) < 0.02}")
    print(f"Missing values: {df.isnull().sum().sum():,}")
    print(f"Duplicate product IDs: {df['product_id'].duplicated().sum():,}")

    top_10_share = (
        df.head(10)["product_revenue"].sum() / total_revenue * 100
    )
    print(f"Top 10 products' revenue share: {top_10_share:.2f}%")

    print(f"\nReport saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

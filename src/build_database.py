from pathlib import Path
import sqlite3
import pandas as pd

PROCESSED_DIR = Path("data/processed")
DB_DIR = Path("database")
DB_PATH = DB_DIR / "ecommerce.db"

DB_DIR.mkdir(parents=True, exist_ok=True)

# Map CSV filenames to SQL table names
TABLES = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "payments",
    "olist_order_reviews_dataset.csv": "reviews",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "category_translation"
}

if DB_PATH.exists():
    raise FileExistsError(
        f"{DB_PATH} already exists. Stop and check before rebuilding."
    )

csv_files = list(TABLES.keys())

for filename in csv_files:
    if not (PROCESSED_DIR / filename).exists():
        raise FileNotFoundError(f"Missing processed file: {filename}")

connection = sqlite3.connect(DB_PATH)

try:
    # Improve performance during bulk loading
    connection.execute("PRAGMA journal_mode = WAL")

    print("\n========== DATABASE LOADING ==========")

    for filename, table_name in TABLES.items():
        file_path = PROCESSED_DIR / filename

        print(f"\nLoading {filename} into {table_name}...")

        df = pd.read_csv(file_path, low_memory=False)

        df.to_sql(
            table_name,
            connection,
            if_exists="fail",
            index=False,
            chunksize=50000
        )

        print(f"Loaded {len(df):,} rows.")

    # Create indexes for commonly joined and filtered columns
    indexes = [
        "CREATE INDEX idx_orders_customer ON orders(customer_id)",
        "CREATE INDEX idx_orders_purchase ON orders(order_purchase_timestamp)",
        "CREATE INDEX idx_items_order ON order_items(order_id)",
        "CREATE INDEX idx_items_product ON order_items(product_id)",
        "CREATE INDEX idx_items_seller ON order_items(seller_id)",
        "CREATE INDEX idx_payments_order ON payments(order_id)",
        "CREATE INDEX idx_reviews_order ON reviews(order_id)",
        "CREATE INDEX idx_products_category ON products(product_category_name)",
        "CREATE INDEX idx_geo_zip ON geolocation(geolocation_zip_code_prefix)"
    ]

    for statement in indexes:
        connection.execute(statement)

    connection.commit()

    print("\n========== DATABASE VALIDATION ==========")

    for table_name in TABLES.values():
        count = connection.execute(
            f'SELECT COUNT(*) FROM "{table_name}"'
        ).fetchone()[0]

        print(f"{table_name:<25} {count:>12,} rows")

    print("\nDatabase created successfully!")
    print(f"Location: {DB_PATH.resolve()}")

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()

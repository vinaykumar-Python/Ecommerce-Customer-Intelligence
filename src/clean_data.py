from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
REPORT_DIR = Path("reports")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

cleaning_summary = []

# Date columns that should be converted
DATE_COLUMNS = {
    "olist_orders_dataset.csv": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ],
    "olist_order_items_dataset.csv": [
        "shipping_limit_date"
    ],
    "olist_order_reviews_dataset.csv": [
        "review_creation_date",
        "review_answer_timestamp"
    ]
}

csv_files = sorted(RAW_DIR.glob("*.csv"))

if len(csv_files) != 9:
    raise ValueError(f"Expected 9 CSV files, found {len(csv_files)}")

for file_path in csv_files:
    print(f"\nProcessing: {file_path.name}")

    df = pd.read_csv(file_path, low_memory=False)

    original_rows = len(df)
    original_duplicates = int(df.duplicated().sum())

    # 1. Remove exact duplicate geolocation records only
    if file_path.name == "olist_geolocation_dataset.csv":
        df = df.drop_duplicates().copy()

    # 2. Standardize product column names
    if file_path.name == "olist_products_dataset.csv":
        df = df.rename(columns={
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length"
        })

        # Missing categories are retained as Unknown
        df["product_category_name"] = (
            df["product_category_name"].fillna("Unknown")
        )

    # 3. Convert date columns safely
    for column in DATE_COLUMNS.get(file_path.name, []):
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    # 4. Save cleaned dataset
    output_path = PROCESSED_DIR / file_path.name
    df.to_csv(output_path, index=False)

    cleaning_summary.append({
        "dataset": file_path.name,
        "original_rows": original_rows,
        "cleaned_rows": len(df),
        "removed_exact_duplicates": original_rows - len(df),
        "original_duplicate_count": original_duplicates,
        "remaining_duplicate_count": int(df.duplicated().sum())
    })

    print(f"Original rows: {original_rows:,}")
    print(f"Cleaned rows: {len(df):,}")
    print(f"Saved: {output_path}")

# Save cleaning report
summary_df = pd.DataFrame(cleaning_summary)
summary_df.to_csv(
    REPORT_DIR / "cleaning_summary.csv",
    index=False
)

print("\n" + "=" * 65)
print("DATA CLEANING COMPLETED")
print("=" * 65)
print(summary_df.to_string(index=False))
print(f"\nCleaned files: {PROCESSED_DIR.resolve()}")
print(f"Cleaning report: {(REPORT_DIR / 'cleaning_summary.csv').resolve()}")

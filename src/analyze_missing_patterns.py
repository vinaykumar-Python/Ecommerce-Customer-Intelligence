from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
REPORTS = Path("reports")
REPORTS.mkdir(exist_ok=True)

# 1. Investigate order delivery dates
orders = pd.read_csv(RAW / "olist_orders_dataset.csv")

date_columns = [
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date"
]

print("\n========== ORDER STATUS ANALYSIS ==========")
print(orders["order_status"].value_counts(dropna=False))

for column in date_columns:
    print(f"\nMissing {column} by order status:")
    result = (
        orders.groupby("order_status", dropna=False)[column]
        .apply(lambda x: x.isna().sum())
    )
    print(result)

# 2. Investigate products with missing categories
products = pd.read_csv(RAW / "olist_products_dataset.csv")

print("\n========== PRODUCT MISSING VALUES ==========")

product_columns = [
    "product_category_name",
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty"
]

print("Rows missing product category:", products["product_category_name"].isna().sum())

print(
    "Rows missing all four related fields:",
    products[product_columns].isna().all(axis=1).sum()
)

print("\nProducts missing weight or dimensions:")
physical_columns = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

print(
    products.loc[
        products[physical_columns].isna().any(axis=1),
        ["product_id"] + physical_columns
    ].to_string(index=False)
)

# 3. Investigate optional review text
reviews = pd.read_csv(RAW / "olist_order_reviews_dataset.csv")

print("\n========== REVIEW ANALYSIS ==========")
print("Total reviews:", len(reviews))
print("Missing titles:", reviews["review_comment_title"].isna().sum())
print("Missing messages:", reviews["review_comment_message"].isna().sum())
print("Missing both:", (
    reviews["review_comment_title"].isna()
    & reviews["review_comment_message"].isna()
).sum())

# 4. Save order-status analysis
status_report = []

for column in date_columns:
    grouped = orders.groupby("order_status", dropna=False)[column]

    for status, values in grouped:
        status_report.append({
            "order_status": status,
            "date_column": column,
            "total_orders": len(values),
            "missing_dates": int(values.isna().sum())
        })

pd.DataFrame(status_report).to_csv(
    REPORTS / "order_missing_by_status.csv",
    index=False
)

print("\nAnalysis completed.")
print("Saved: reports/order_missing_by_status.csv")

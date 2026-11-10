from pathlib import Path
import pandas as pd

INPUT_PATH = Path("reports/customer_rfm.csv")
OUTPUT_PATH = Path("reports/customer_rfm_segmented.csv")
SUMMARY_PATH = Path("reports/rfm_segment_summary.csv")

rfm = pd.read_csv(INPUT_PATH)

# Recency: more recent customers receive higher scores.
rfm["R_score"] = pd.qcut(
    rfm["recency_days"],
    q=5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

# Frequency: custom thresholds because 97% of customers
# have only one delivered order.
rfm["F_score"] = pd.cut(
    rfm["frequency"],
    bins=[0, 1, 3, float("inf")],
    labels=[1, 2, 3]
).astype(int)

# Monetary: higher-spending customers receive higher scores.
rfm["M_score"] = pd.qcut(
    rfm["monetary"],
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Combined RFM score.
rfm["RFM_score"] = (
    rfm["R_score"].astype(str)
    + rfm["F_score"].astype(str)
    + rfm["M_score"].astype(str)
)

# Custom customer segments.
def assign_segment(row):
    r = row["R_score"]
    f = row["F_score"]
    m = row["M_score"]

    if r >= 4 and f >= 2 and m >= 4:
        return "Champions"

    elif f >= 2 and r >= 3:
        return "Loyal Customers"

    elif f >= 2 and r <= 2:
        return "At Risk"

    elif f == 1 and r >= 4 and m >= 3:
        return "Potential Loyalists"

    elif f == 1 and r <= 3 and m == 5:
        return "High-Value One-Time Buyers"

    elif f == 1 and r >= 4:
        return "Recent One-Time Buyers"

    else:
        return "Other One-Time Buyers"


rfm["customer_segment"] = rfm.apply(
    assign_segment,
    axis=1
)

# Save customer-level segmentation.
rfm.to_csv(OUTPUT_PATH, index=False)

# Create segment-level summary.
summary = (
    rfm.groupby("customer_segment", observed=True)
    .agg(
        customers=("customer_unique_id", "count"),
        average_recency_days=("recency_days", "mean"),
        average_frequency=("frequency", "mean"),
        average_monetary=("monetary", "mean"),
        total_product_revenue=("monetary", "sum")
    )
    .reset_index()
)

summary["customer_percentage"] = (
    summary["customers"] / len(rfm) * 100
).round(2)

summary = summary.sort_values(
    "customers",
    ascending=False
)

summary[
    [
        "average_recency_days",
        "average_frequency",
        "average_monetary",
        "total_product_revenue"
    ]
] = summary[
    [
        "average_recency_days",
        "average_frequency",
        "average_monetary",
        "total_product_revenue"
    ]
].round(2)

summary.to_csv(SUMMARY_PATH, index=False)

print("\nCUSTOMER SEGMENT SUMMARY")
print("=" * 100)
print(summary.to_string(index=False))

print("\nSEGMENTATION VALIDATION")
print("=" * 65)
print("Total customers:", len(rfm))
print("Segmented customers:", rfm["customer_segment"].notna().sum())
print("Missing segments:", rfm["customer_segment"].isna().sum())
print("Duplicate customer IDs:", rfm["customer_unique_id"].duplicated().sum())
print("Total segment customers:", summary["customers"].sum())
print("Total product revenue:", round(rfm["monetary"].sum(), 2))

print("\nFiles saved:")
print(OUTPUT_PATH)
print(SUMMARY_PATH)


from pathlib import Path
import pandas as pd

RFM_PATH = Path("reports/customer_rfm.csv")

rfm = pd.read_csv(RFM_PATH)

print("\nCUSTOMER ORDER FREQUENCY DISTRIBUTION")
print("=" * 65)

frequency_counts = (
    rfm["frequency"]
    .value_counts()
    .sort_index()
)

frequency_summary = pd.DataFrame({
    "customers": frequency_counts,
    "percentage": (
        frequency_counts / len(rfm) * 100
    ).round(2)
})

print(frequency_summary.to_string())

print("\nFREQUENCY PERCENTILES")
print("=" * 65)

print(
    rfm["frequency"]
    .quantile([0, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 1])
    .to_string()
)

print("\nRECENCY AND MONETARY QUANTILE BOUNDARIES")
print("=" * 65)

for column in ["recency_days", "monetary"]:
    print(f"\n{column}")

    print(
        rfm[column]
        .quantile([0, 0.20, 0.40, 0.60, 0.80, 1])
        .round(2)
        .to_string()
    )

print("\nTotal customers:", len(rfm))

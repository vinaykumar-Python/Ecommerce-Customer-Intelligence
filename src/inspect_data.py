from pathlib import Path
import pandas as pd

# Define project directories
RAW_DIR = Path("data/raw")
REPORT_DIR = Path("reports")

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Find all CSV files
csv_files = sorted(RAW_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV files found in data/raw")

dataset_summary = []
column_details = []
missing_details = []

print(f"\nFound {len(csv_files)} CSV files.\n")

for file_path in csv_files:
    print("=" * 65)
    print(f"Inspecting: {file_path.name}")

    # Load dataset
    df = pd.read_csv(file_path, low_memory=False)

    row_count, column_count = df.shape
    duplicate_count = int(df.duplicated().sum())
    memory_mb = df.memory_usage(deep=True).sum() / (1024 ** 2)

    # Dataset-level summary
    dataset_summary.append({
        "dataset": file_path.name,
        "rows": row_count,
        "columns": column_count,
        "duplicate_rows": duplicate_count,
        "memory_mb": round(memory_mb, 2)
    })

    # Column-level details
    for column in df.columns:
        missing_count = int(df[column].isna().sum())

        column_details.append({
            "dataset": file_path.name,
            "column": column,
            "data_type": str(df[column].dtype),
            "missing_values": missing_count,
            "missing_percentage": round(
                (missing_count / row_count) * 100, 2
            ) if row_count else 0
        })

        if missing_count > 0:
            missing_details.append({
                "dataset": file_path.name,
                "column": column,
                "missing_values": missing_count,
                "missing_percentage": round(
                    (missing_count / row_count) * 100, 2
                ) if row_count else 0
            })

    print(f"Rows: {row_count:,}")
    print(f"Columns: {column_count}")
    print(f"Duplicate rows: {duplicate_count:,}")
    print(f"Memory usage: {memory_mb:.2f} MB")
    print("\nColumn names:")
    print(list(df.columns))

# Save reports
summary_df = pd.DataFrame(dataset_summary)
columns_df = pd.DataFrame(column_details)
missing_df = pd.DataFrame(missing_details)

summary_df.to_csv(REPORT_DIR / "dataset_overview.csv", index=False)
columns_df.to_csv(REPORT_DIR / "column_profile.csv", index=False)
missing_df.to_csv(REPORT_DIR / "missing_values.csv", index=False)

print("\n" + "=" * 65)
print("DATASET INSPECTION COMPLETED")
print("=" * 65)
print(summary_df.to_string(index=False))
print("\nReports saved in:", REPORT_DIR.resolve())

from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path("database/ecommerce.db")
SQL_PATH = Path("sql/05_customer_cohort_retention.sql")

LONG_OUTPUT = Path("reports/cohort_retention_long.csv")
MATRIX_OUTPUT = Path("reports/cohort_retention_matrix.csv")

# Read the SQL query.
query = SQL_PATH.read_text(encoding="utf-8")

# Execute the query against SQLite.
with sqlite3.connect(DB_PATH) as connection:
    cohort_data = pd.read_sql_query(query, connection)

# Save detailed cohort results.
cohort_data.to_csv(LONG_OUTPUT, index=False)

# Convert retention results into a cohort matrix.
retention_matrix = cohort_data.pivot(
    index="cohort_month",
    columns="cohort_index",
    values="retention_rate"
)

retention_matrix.columns = [
    f"Month_{int(column)}"
    for column in retention_matrix.columns
]

retention_matrix.to_csv(MATRIX_OUTPUT)

print("\nCOHORT RETENTION DETAIL")
print("=" * 80)
print(cohort_data.head(20).to_string(index=False))

print("\nCOHORT RETENTION MATRIX (%)")
print("=" * 80)
print(retention_matrix.to_string())

print("\nCOHORT VALIDATION")
print("=" * 80)

print("Number of cohorts:", cohort_data["cohort_month"].nunique())
print("Total cohort customers:",
      cohort_data.loc[
          cohort_data["cohort_index"] == 0,
          "cohort_size"
      ].sum())

print("Month 0 retention always 100%:",
      (cohort_data.loc[
          cohort_data["cohort_index"] == 0,
          "retention_rate"
      ] == 100).all())

print("Retention values between 0 and 100:",
      cohort_data["retention_rate"].between(0, 100).all())

print("Missing values:", cohort_data.isna().sum().sum())

print("\nReports saved:")
print(LONG_OUTPUT)
print(MATRIX_OUTPUT)

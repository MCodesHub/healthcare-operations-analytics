# 1. Import Libraries
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "tableau_ed_encounters.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
FIGURE_DIR = PROJECT_ROOT / "reports" / "figures"


# 2. Load Dataset
df = pd.read_csv(DATA_FILE)


# 3. Inspect Dataset
print("\nFIRST FIVE ROWS")
print(df.head())
print("\nDATASET SHAPE")
print(df.shape)
print("\nCOLUMN NAMES")
print(df.columns.tolist())
print("\nDATASET INFORMATION")
df.info()


# 4. Review Data Types and Summary Statistics
print("\nDATA TYPES")
print(df.dtypes.sort_index())
print("\nNUMERICAL SUMMARY")
print(df.describe().round(2))


# 5. Check Duplicate Rows
duplicate_count = df.duplicated().sum()
print(f"\nDUPLICATE ROWS: {duplicate_count}")


# 6. Check Missing Values
missing_values = df.isna().sum().sort_values(ascending=False)
print("\nMISSING VALUES")
print(missing_values[missing_values > 0] if missing_values.any() else "No missing values found")


# 7. Clean and Prepare Data
df = df.drop_duplicates().copy()
df["arrival_datetime"] = pd.to_datetime(df["arrival_datetime"], errors="coerce")
df = df.dropna(subset=["encounter_id", "arrival_datetime"])

numeric_columns = [
    "age",
    "esi_acuity",
    "wait_minutes",
    "treatment_minutes",
    "length_of_stay_minutes",
    "revisit_72h",
    "satisfaction_score",
]
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")
    df[column] = df[column].fillna(df[column].median())

text_columns = ["facility_name", "service_line", "payer", "disposition"]
for column in text_columns:
    df[column] = df[column].fillna("Unknown").str.strip()

df = df[df["esi_acuity"].between(1, 5)]
df = df[(df["wait_minutes"] >= 0) & (df["length_of_stay_minutes"] >= 0)]

df["arrival_date"] = df["arrival_datetime"].dt.date
df["arrival_hour"] = df["arrival_datetime"].dt.hour
df["month"] = df["arrival_datetime"].dt.to_period("M").astype(str)
df["day_of_week"] = df["arrival_datetime"].dt.day_name()
df["shift"] = pd.cut(
    df["arrival_hour"],
    bins=[-1, 6, 14, 22, 23],
    labels=["Night", "Day", "Evening", "Night"],
    ordered=False,
)
df["wait_target_met"] = (df["wait_minutes"] <= 30).astype(int)


# 8. Exploratory Data Analysis
print("\nOVERALL KEY PERFORMANCE INDICATORS")
print(f"Total encounters: {len(df):,}")
print(f"Average wait: {df['wait_minutes'].mean():.1f} minutes")
print(f"Median length of stay: {df['length_of_stay_minutes'].median():.1f} minutes")
print(f"72-hour revisit rate: {df['revisit_72h'].mean():.1%}")
print(f"Average satisfaction: {df['satisfaction_score'].mean():.2f} out of 5")

long_waits = df[df["wait_minutes"] > 60].sort_values("wait_minutes", ascending=False)
print(f"Encounters with waits over 60 minutes: {len(long_waits):,}")


# 9. Grouping and Aggregation
shift_summary = (
    df.groupby("shift", observed=True)
    .agg(
        encounters=("encounter_id", "count"),
        average_wait_minutes=("wait_minutes", "mean"),
        average_length_of_stay=("length_of_stay_minutes", "mean"),
        revisit_rate=("revisit_72h", "mean"),
    )
    .reset_index()
    .sort_values("average_wait_minutes", ascending=False)
)

facility_summary = (
    df.groupby("facility_name")
    .agg(
        encounters=("encounter_id", "count"),
        average_wait_minutes=("wait_minutes", "mean"),
        median_length_of_stay=("length_of_stay_minutes", "median"),
        revisit_rate=("revisit_72h", "mean"),
    )
    .reset_index()
    .sort_values("average_wait_minutes", ascending=False)
)

service_summary = (
    df.groupby("service_line")
    .agg(
        encounters=("encounter_id", "count"),
        average_wait_minutes=("wait_minutes", "mean"),
        revisit_rate=("revisit_72h", "mean"),
    )
    .reset_index()
    .sort_values("revisit_rate", ascending=False)
)

print("\nWAIT TIMES BY SHIFT")
print(shift_summary.round(2).to_string(index=False))
print("\nFACILITY SUMMARY")
print(facility_summary.round(2).to_string(index=False))


# 10. Create Visualizations
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
plt.style.use("seaborn-v0_8-whitegrid")
chart_color = "#6C2B3B"

wait_by_hour = df.groupby("arrival_hour")["wait_minutes"].mean()
plt.figure(figsize=(10, 5))
plt.plot(wait_by_hour.index, wait_by_hour.values, marker="o", color=chart_color)
plt.title("Average Emergency Department Wait by Arrival Hour")
plt.xlabel("Arrival Hour")
plt.ylabel("Average Wait (Minutes)")
plt.xticks(range(0, 24, 2))
plt.tight_layout()
plt.savefig(FIGURE_DIR / "wait_by_hour.png", dpi=160)
plt.close()

service_chart = service_summary.sort_values("revisit_rate")
plt.figure(figsize=(9, 5))
plt.barh(service_chart["service_line"], service_chart["revisit_rate"] * 100, color=chart_color)
plt.title("72-Hour Revisit Rate by Service Line")
plt.xlabel("Revisit Rate (%)")
plt.ylabel("Service Line")
plt.tight_layout()
plt.savefig(FIGURE_DIR / "revisit_by_service.png", dpi=160)
plt.close()


# 11. Export Processed Data
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_DIR / "ed_encounters_cleaned.csv", index=False)
facility_summary.round(3).to_csv(OUTPUT_DIR / "facility_summary.csv", index=False)
service_summary.round(3).to_csv(OUTPUT_DIR / "service_line_summary.csv", index=False)

print("\nAnalysis complete. Cleaned data, summaries, and charts were exported successfully.")


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# WEBSITE TRAFFIC ANALYSIS
# ==============================

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "website_traffic.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Create output folder if it does not exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# 1. LOAD DATA
# ==============================

print("\n" + "=" * 60)
print("        WEBSITE TRAFFIC ANALYSIS")
print("=" * 60)

try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print("\nERROR: website_traffic.csv not found!")
    print("Please put the CSV file inside the data folder.")
    exit()

print("\nDataset loaded successfully!")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# ==============================
# 2. DATA CLEANING
# ==============================

print("\n" + "-" * 60)
print("DATA CLEANING")
print("-" * 60)

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Remove invalid dates
df = df.dropna(subset=["Date"])

# Remove duplicate records
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# Fill missing numerical values
numeric_columns = [
    "Visitors",
    "PageViews",
    "Conversions",
    "BounceRate",
    "SessionDuration"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
        df[column] = df[column].fillna(df[column].median())

# Fill missing categorical values
for column in ["Source", "Page"]:
    if column in df.columns:
        df[column] = df[column].fillna("Unknown")

print(f"Duplicate rows removed: {duplicates}")
print(f"Final rows after cleaning: {len(df)}")

# ==============================
# 3. BASIC KPIs
# ==============================

total_visitors = int(df["Visitors"].sum())
total_pageviews = int(df["PageViews"].sum())
total_conversions = int(df["Conversions"].sum())

average_daily_visitors = df["Visitors"].mean()
average_pageviews = df["PageViews"].mean()

conversion_rate = (
    total_conversions / total_visitors * 100
    if total_visitors > 0
    else 0
)

average_bounce_rate = df["BounceRate"].mean()
average_session_duration = df["SessionDuration"].mean()

print("\n" + "-" * 60)
print("KEY PERFORMANCE INDICATORS")
print("-" * 60)

print(f"Total Visitors           : {total_visitors:,}")
print(f"Total Page Views         : {total_pageviews:,}")
print(f"Total Conversions        : {total_conversions:,}")
print(f"Average Daily Visitors   : {average_daily_visitors:,.2f}")
print(f"Average Page Views       : {average_pageviews:,.2f}")
print(f"Conversion Rate          : {conversion_rate:.2f}%")
print(f"Average Bounce Rate      : {average_bounce_rate:.2f}%")
print(f"Avg Session Duration     : {average_session_duration:.2f} seconds")

# ==============================
# 4. TRAFFIC SOURCE ANALYSIS
# ==============================

source_analysis = (
    df.groupby("Source")
    .agg(
        Visitors=("Visitors", "sum"),
        PageViews=("PageViews", "sum"),
        Conversions=("Conversions", "sum")
    )
    .sort_values("Visitors", ascending=False)
)

source_analysis["ConversionRate"] = (
    source_analysis["Conversions"]
    / source_analysis["Visitors"]
    * 100
)

print("\n" + "-" * 60)
print("TRAFFIC SOURCE ANALYSIS")
print("-" * 60)

print(source_analysis.round(2))

# Best traffic source
best_source = source_analysis["Visitors"].idxmax()

# ==============================
# 5. PAGE ANALYSIS
# ==============================

page_analysis = (
    df.groupby("Page")
    .agg(
        Visitors=("Visitors", "sum"),
        PageViews=("PageViews", "sum"),
        Conversions=("Conversions", "sum")
    )
    .sort_values("PageViews", ascending=False)
)

print("\n" + "-" * 60)
print("TOP PERFORMING PAGES")
print("-" * 60)

print(page_analysis.head(10))

best_page = page_analysis["PageViews"].idxmax()

# ==============================
# 6. DAILY TRAFFIC
# ==============================

daily_traffic = (
    df.groupby("Date")
    .agg(
        Visitors=("Visitors", "sum"),
        PageViews=("PageViews", "sum"),
        Conversions=("Conversions", "sum")
    )
)

# ==============================
# 7. MONTHLY TRAFFIC
# ==============================

df["Month"] = df["Date"].dt.to_period("M").astype(str)

monthly_traffic = (
    df.groupby("Month")
    .agg(
        Visitors=("Visitors", "sum"),
        PageViews=("PageViews", "sum"),
        Conversions=("Conversions", "sum")
    )
)

print("\n" + "-" * 60)
print("MONTHLY TRAFFIC")
print("-" * 60)

print(monthly_traffic)

# ==============================
# 8. SAVE ANALYSIS FILES
# ==============================

source_analysis.to_csv(
    os.path.join(OUTPUT_DIR, "traffic_source_analysis.csv")
)

page_analysis.to_csv(
    os.path.join(OUTPUT_DIR, "page_analysis.csv")
)

monthly_traffic.to_csv(
    os.path.join(OUTPUT_DIR, "monthly_traffic.csv")
)

# ==============================
# 9. GRAPH - DAILY TRAFFIC
# ==============================

plt.figure(figsize=(12, 6))

plt.plot(
    daily_traffic.index,
    daily_traffic["Visitors"],
    marker="o"
)

plt.title("Daily Website Visitors")
plt.xlabel("Date")
plt.ylabel("Visitors")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "daily_traffic.png"),
    dpi=300
)

plt.close()

# ==============================
# 10. GRAPH - TRAFFIC SOURCES
# ==============================

plt.figure(figsize=(10, 6))

source_analysis["Visitors"].plot(
    kind="bar"
)

plt.title("Visitors by Traffic Source")
plt.xlabel("Traffic Source")
plt.ylabel("Visitors")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "traffic_sources.png"),
    dpi=300
)

plt.close()

# ==============================
# 11. GRAPH - TOP PAGES
# ==============================

top_pages = page_analysis.head(10)

plt.figure(figsize=(10, 6))

top_pages["PageViews"].sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Most Visited Pages")
plt.xlabel("Page Views")
plt.ylabel("Page")

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "top_pages.png"),
    dpi=300
)

plt.close()

# ==============================
# 12. GRAPH - MONTHLY TRAFFIC
# ==============================

plt.figure(figsize=(10, 6))

plt.plot(
    monthly_traffic.index,
    monthly_traffic["Visitors"],
    marker="o"
)

plt.title("Monthly Website Traffic")
plt.xlabel("Month")
plt.ylabel("Visitors")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "monthly_traffic.png"),
    dpi=300
)

plt.close()

# ==============================
# 13. GRAPH - CONVERSIONS
# ==============================

plt.figure(figsize=(10, 6))

plt.bar(
    source_analysis.index,
    source_analysis["Conversions"]
)

plt.title("Conversions by Traffic Source")
plt.xlabel("Traffic Source")
plt.ylabel("Conversions")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "conversions.png"),
    dpi=300
)

plt.close()

# ==============================
# 14. AUTOMATIC INSIGHTS
# ==============================

highest_traffic_day = daily_traffic["Visitors"].idxmax()
highest_traffic_value = daily_traffic["Visitors"].max()

lowest_traffic_day = daily_traffic["Visitors"].idxmin()
lowest_traffic_value = daily_traffic["Visitors"].min()

best_conversion_source = source_analysis["ConversionRate"].idxmax()

print("\n" + "=" * 60)
print("AUTOMATIC INSIGHTS")
print("=" * 60)

print(
    f"\n1. Best traffic source: {best_source}"
)

print(
    f"   It generated {source_analysis.loc[best_source, 'Visitors']:,} visitors."
)

print(
    f"\n2. Most visited page: {best_page}"
)

print(
    f"   It received {page_analysis.loc[best_page, 'PageViews']:,} page views."
)

print(
    f"\n3. Highest traffic day: {highest_traffic_day.date()}"
)

print(
    f"   Visitors: {highest_traffic_value:,}"
)

print(
    f"\n4. Lowest traffic day: {lowest_traffic_day.date()}"
)

print(
    f"   Visitors: {lowest_traffic_value:,}"
)

print(
    f"\n5. Best conversion source: {best_conversion_source}"
)

print(
    f"   Conversion rate: "
    f"{source_analysis.loc[best_conversion_source, 'ConversionRate']:.2f}%"
)

# ==============================
# 15. FINAL MESSAGE
# ==============================

print("\n" + "=" * 60)
print("ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nGenerated files:")
print("✓ traffic_source_analysis.csv")
print("✓ page_analysis.csv")
print("✓ monthly_traffic.csv")
print("✓ daily_traffic.png")
print("✓ traffic_sources.png")
print("✓ top_pages.png")
print("✓ monthly_traffic.png")
print("✓ conversions.png")

print("\nAll files are available inside the outputs folder.")
